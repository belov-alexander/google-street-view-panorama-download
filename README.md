# Google Street View Panorama Downloader

A Python utility to download full-resolution user-contributed panoramas (photospheres) from Google Maps.

## Description

This tool resolves shortened Google Maps URLs (e.g., `https://maps.app.goo.gl/...`), handles Google Consent page redirections, and decodes internal image URLs to extract and download the highest resolution panorama available.

## Features

- **URL Resolution**: Automatically expands shortened URLs.
- **High Resolution**: Fetches the maximum available dimensions (up to 8192x4096 or higher where available).
- **Consent Handling**: Bypasses the strict Google Consent redirects.
- **Configurable**: Easy configuration via `config.py`.
- **Organized Output**: Saves files to a dedicated `download/` directory.

## Installation

1. Clone this repository.
2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Open `config.py` in your text editor.
2. Update the configuration variables:

    ```python
    # The Google Maps URL of the panorama
    PANO_URL = 'https://maps.app.goo.gl/...'

    # The output filename
    IMAGE_NAME = 'my_panorama.jpg'
    ```

3. Run the script:

    ```bash
    python panorama-download.py
    ```

The downloaded image will be saved in the `download/` directory, e.g., `download/my_panorama.jpg`.

## How it Works

1. **Resolution**: Expands the initial URL.
2. **extraction**: Parses query parameters to find the deep link.
3. **Decoding**: Decodes the weird `!6s...` patterns to find the real image URL.
4. **Resizing**: Manipulates URL parameters to request the highest resolution (`!7i` width, `!8i` height).
5. **Downloading**: Streams the content to the local disk.

## Legal Warning & Disclaimer

**Usage of this tool is for educational purposes only.**

By using this software, you agree to comply with Google's Terms of Service.

- **Copyright**: Images belong to their respective owners (photographers or Google).
- **Terms**: Automated downloading may violate Google's Terms of Service.
- **Liability**: The author assumes no liability for misuse of this tool. Use responsibly.
