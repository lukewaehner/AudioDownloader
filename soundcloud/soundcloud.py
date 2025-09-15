import os
import requests
from tqdm import tqdm
from mutagen.easyid3 import EasyID3
import uuid


class SoundCloudDownloader:
    def __init__(self, client_id=None, download_path="./downloads"):
        """
        Initialize the downloader.

        :param client_id: Your SoundCloud API client_id. If None, attempts to extract dynamically.
        :param download_path: Path where the tracks will be downloaded.
        """
        self.client_id = client_id or self.generate_client_id()
        self.download_path = download_path
        os.makedirs(self.download_path, exist_ok=True)

    @staticmethod
    def generate_client_id():
        """Generates a random UUID as a temporary client ID."""
        client_id = "YHtBnq6bxM7DhJkIfzrGq3gYrueyLDMM"
        return client_id

    def _fetch(self, url, params=None):
        params = params or {}
        params["client_id"] = self.client_id
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch {url}: {response.text}")
        return response.json()

    def get_track_info(self, track_url):
        api_url = f"https://api.soundcloud.com/resolve"
        params = {"url": track_url}
        resolved = self._fetch(api_url, params)
        if resolved["kind"] != "track":
            raise Exception("Invalid track URL")
        return resolved

    def download_track(self, track_info):
        """Download a track using its track info."""
        title = track_info["title"]
        stream_url = f"{track_info['stream_url']}?client_id={self.client_id}"

        # Prepare file path
        filename = f"{self.sanitize_filename(title)}.mp3"
        filepath = os.path.join(self.download_path, filename)

        # Check if file already exists
        if os.path.exists(filepath):
            print(f"Track already exists: {filepath}")
            return filepath

        # Stream and save the track
        print(f"Downloading: {title}")
        with requests.get(stream_url, stream=True) as response:
            total_size = int(response.headers.get("content-length", 0))
            with (
                open(filepath, "wb") as file,
                tqdm(
                    desc=f"Saving {title}",
                    total=total_size,
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                ) as progress,
            ):
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
                    progress.update(len(chunk))

        print(f"Downloaded: {filepath}")
        return filepath

    def set_metadata(self, filepath, track_info):
        """Set metadata for the downloaded MP3 file."""
        try:
            audio = EasyID3(filepath)
        except Exception:
            from mutagen.mp3 import MP3

            audio = MP3(filepath)
            audio.add_tags()

        audio["title"] = track_info.get("title", "Unknown Title")
        audio["artist"] = track_info.get(
            "user", {}).get("username", "Unknown Artist")
        audio["genre"] = track_info.get("genre", "Unknown Genre")
        audio["date"] = track_info.get("created_at", "").split("T")[0]
        audio.save()
        print(f"Metadata set for {filepath}")

    def sanitize_filename(self, name):
        """Sanitize filenames to remove illegal characters."""
        return "".join(c if c.isalnum() or c in " -_." else "_" for c in name)

    def download(self, track_url):
        """Main function to handle the download process."""
        try:
            track_info = self.get_track_info(track_url)
            filepath = self.download_track(track_info)
            self.set_metadata(filepath, track_info)
        except Exception as e:
            print(f"Error: {e}")
