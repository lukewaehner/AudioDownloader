import json
import os
import readline  # For tab completion

SETTINGS_FILE = "settings.json"


def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Settings file not found or invalid. Using default settings.")
        return {"download_directory": "downloads"}


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)
        print("Settings updated successfully!")


def path_completion(text, state):
    """
    Enable tab-completion for file paths in the terminal.
    """
    line = readline.get_line_buffer()
    if not line:
        return None

    path = os.path.expanduser(line)
    matches = [
        p
        for p in os.listdir(os.path.dirname(path) or ".")
        if p.startswith(os.path.basename(path))
    ]
    matches = [os.path.join(os.path.dirname(path), m) for m in matches]
    try:
        return matches[state]
    except IndexError:
        return None


def configure_download_directory():
    """
    Prompt the user to set a new download directory with tab completion enabled.
    """
    settings = load_settings()

    # Enable tab completion for paths
    readline.set_completer(path_completion)
    readline.parse_and_bind("tab: complete")

    print("Enter the new download directory (use '~' for home directory):")
    new_dir = input("> ").strip()

    if new_dir:
        # Expand ~ to the full home directory path
        expanded_dir = os.path.expanduser(new_dir)

        if os.path.isdir(expanded_dir):
            settings["download_directory"] = expanded_dir
            save_settings(settings)
            print(f"Download directory updated to: {expanded_dir}")
        else:
            print(f"Invalid directory: {expanded_dir}. Please try again.")
    else:
        print("No changes made.")


def main():
    print("Welcome to the Audio Downloader!")
    print("1. Download YouTube audio")
    print("2. Download Soundcloud audio")
    print("M. Change download directory")

    choice = input("Enter your choice: ").strip()
    if choice == "1":
        from youtube.youtube import (
            download_youtube_audio,
        )  # Import dynamically to avoid circular dependencies

        url = input("Enter the URL: ").strip()
        download_youtube_audio(url)
    elif choice == "2":
        """Soundcloud Downloader Code"""
        from soundcloud.soundcloud import (
            SoundCloudDownloader,
        )  # Import dynamically to avoid circular dependencies

        dl = SoundCloudDownloader(download_path=load_settings()["download_directory"])
        track_url = input(
            "Enter the URL of the Soundcloud Song you want to download "
        ).strip()
        dl.download(track_url)
    elif choice.lower() == "m":
        """Change download directory"""
        configure_download_directory()
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
