import requests
import re
import urllib.parse
import sys
import os
import config

def download_panorama(url, output_file="image.jpg"):
    print(f"Resolving URL: {url}")
    session = requests.Session()
    # No headers to allow consent page redirect which we handle
    resp = session.get(url, allow_redirects=True)
    final_url = resp.url
    
    target_url = final_url
    if "consent.google.com" in final_url:
        print("Hit consent page, extracting continue url...")
        parsed = urllib.parse.urlparse(final_url)
        qs = urllib.parse.parse_qs(parsed.query)
        if 'continue' in qs:
            target_url = qs['continue'][0]
    
    # Check for encoded image URL in !6s... pattern
    # Sometimes it's double encoded.
    match = re.search(r'!6s(.*?)!', target_url)
    if not match:
        unquoted_target = urllib.parse.unquote(target_url)
        match = re.search(r'!6s(.*?)!', unquoted_target)

    if not match:
        print("Error: Could not find image URL in the resolved link.")
        return

    image_url_segment = match.group(1)
    
    decoded_url = image_url_segment
    for _ in range(3):
        if decoded_url.startswith("https://") or decoded_url.startswith("http://"):
            break
        decoded_url = urllib.parse.unquote(decoded_url)
    
    if not (decoded_url.startswith("https://") or decoded_url.startswith("http://")):
         print("Error: Failed to decode image URL.")
         return

    base_image_url = decoded_url.split('=')[0]
    
    # Extract resolution (!7iW!8iH)
    unquoted_target = urllib.parse.unquote(target_url)
    width_match = re.search(r'!7i(\d+)', unquoted_target)
    height_match = re.search(r'!8i(\d+)', unquoted_target)
    
    width = width_match.group(1) if width_match else "8192"
    height = height_match.group(1) if height_match else "4096"
    
    print(f"Found panorama dimensions: {width}x{height}")
    
    full_res_url = f"{base_image_url}=w{width}-h{height}-k-no"
    print(f"Downloading from: {full_res_url}")
    
    r = requests.get(full_res_url, stream=True)
    if r.status_code == 200:
        with open(output_file, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                f.write(chunk)
        print(f"Successfully saved to {output_file}")
    else:
        print(f"Failed to download image. Status code: {r.status_code}")

if __name__ == "__main__":
    # Create download directory if it doesn't exist
    download_dir = "download"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"Created directory: {download_dir}")

    # Construct the full output path
    output_path = os.path.join(download_dir, config.IMAGE_NAME)
   
    download_panorama(config.PANO_URL, output_path)