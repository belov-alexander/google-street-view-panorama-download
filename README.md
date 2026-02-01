# Google Street View Panorama Downloader

A simple Python script to download full-resolution user-contributed panoramas (photospheres) from Google Maps.

## Description

This tool accepts a shortened Google Maps URL (e.g., `https://maps.app.goo.gl/...`), resolves it, and extracts the highest resolution image available. It handles the intermediate Google Consent page redirection and decodes the internal image URLs to fetch the original panorama.

## Installation

1. Clone or download this repository.
2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Open `panorama-download.py` in your text editor.
2. Modify the `pano_url` and `image_name` variables in the `__main__` block at the bottom of the file:

    ```python
    if __name__ == "__main__":
        pano_url = 'https://maps.app.goo.gl/ID_OF_PANORAMA'
        image_name = 'my_panorama.jpg'
        download_panorama(pano_url, image_name)
    ```

3. Run the script:

    ```bash
    python panorama-download.py
    ```

## How it Works

1. **URL Resolution**: Expands the shortened `maps.app.goo.gl` URL.
2. **Consent Handling**: Detects if the response is a Google Consent page and parses the query parameters to find the `continue` URL.
3. **Pattern Matching**: Searches the final URL for the specific pattern (`!6s...`) that contains the encoded image URL.
4. **Decoding**: Iteratively URL-decodes the segment until a valid `https` link is found.
5. **Dimension Extraction**: Finds `!7i` and `!8i` parameters to determine the maximum available width and height (defaulting to 8192x4096 if not found).
6. **Download**: constructs the direct image URL and streams the download to the specified output file.

## Legal Warning & Disclaimer

**Usage of this tool is for educational purposes only.**

By using this software, you agree to comply with Google's Terms of Service. Please be aware of the following:

1. **Copyright**: Panoramas and photospheres are subject to copyright. User-contributed content belongs to the original photographer, while Google-captured street view imagery belongs to Google. You generally do not have the right to use these images for commercial purposes, redistribution, or public display without express permission from the copyright holder.
2. **Terms of Service**: Automated scraping or mass downloading of content from Google Maps typically violates Google's Terms of Service. Using this tool to download data against these terms may result in your IP address being blocked or legal action.
3. **Google Maps/Google Earth Additional Terms**: According to Google's [Additional Terms of Service](https://www.google.com/help/terms_maps/), you may not:
    * systematically retrieve content to create or compile, directly or indirectly, a collection, compilation, database, or directory.
    * use the content with other products or services.

**The author of this script assumes no liability for how you use this tool or for any violation of terms, copyright laws, or other regulations.** Please use responsibly and respect the rights of content creators.
