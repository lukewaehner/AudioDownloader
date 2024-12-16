import yt_dlp
from main import load_settings


def download_youtube_audio(url):
    settings = load_settings()
    download_directory = settings.get("download_directory", "downloads")

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": f"{download_directory}/%(title)s.%(ext)s",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading audio from YouTube to '{download_directory}'...")
            ydl.download([url])
            print("Download complete!")
    except Exception as e:
        print(f"An error occurred: {e}")
