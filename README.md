# AudioDownloader

A Python-based command-line tool for downloading audio from YouTube and SoundCloud platforms. The application provides a simple interactive interface to download high-quality audio files with proper metadata.

## Features

- **YouTube Audio Download**: Download audio from YouTube videos in MP3 format (192kbps quality)
- **SoundCloud Audio Download**: Download tracks from SoundCloud with metadata preservation
- **Configurable Download Directory**: Set custom download locations with tab completion support
- **Progress Tracking**: Visual progress bars for downloads
- **Metadata Support**: Automatic metadata tagging for downloaded files
- **Interactive CLI**: User-friendly command-line interface

## Requirements

- Python 3.6+
- yt-dlp
- requests
- tqdm
- mutagen

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd AudioDownloader
```

2. Install required dependencies:

```bash
pip install yt-dlp requests tqdm mutagen
```

## Usage

Run the main application:

```bash
python main.py
```

The application will present you with the following options:

1. **Download YouTube audio** - Enter a YouTube URL to download the audio
2. **Download Soundcloud audio** - Enter a SoundCloud track URL to download
3. **Change download directory** - Configure where files are saved (supports tab completion)

### Example Usage

1. Start the application:

```bash
python main.py
```

2. Choose option 1 for YouTube or option 2 for SoundCloud

3. Enter the URL when prompted

4. The audio will be downloaded to your configured directory

## Configuration

The application uses a `settings.json` file to store configuration:

```json
{
  "download_directory": "/path/to/your/downloads"
}
```

You can change the download directory through the application menu (option M) or by editing the settings file directly.

## Project Structure

```
AudioDownloader/
├── main.py              # Main application entry point
├── settings.json        # Configuration file
├── youtube/
│   ├── __init__.py
│   └── youtube.py       # YouTube download functionality
└── soundcloud/
    ├── __init__.py
    └── soundcloud.py    # SoundCloud download functionality
```

## Technical Details

### YouTube Downloads

- Uses `yt-dlp` library for reliable YouTube access
- Downloads in MP3 format at 192kbps quality
- Automatically extracts audio from video content

### SoundCloud Downloads

- Uses SoundCloud's API for track resolution
- Downloads original audio quality
- Preserves track metadata (title, artist, genre, date)
- Includes progress tracking with file size information

## Error Handling

The application includes comprehensive error handling for:

- Invalid URLs
- Network connectivity issues
- File system permissions
- API rate limiting
- Corrupted downloads

## License

This project is for educational and personal use only. Please respect the terms of service of YouTube and SoundCloud when using this tool.

## Disclaimer

This tool is intended for downloading content you have the right to download. Users are responsible for complying with copyright laws and platform terms of service.
