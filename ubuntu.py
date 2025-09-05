import requests
import os
from urllib.parse import urlparse
import hashlib

def get_filename_from_url(url):
    """
    Extract filename from URL or generate a unique one if missing.
    """
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename:
        filename = "downloaded_image.jpg"
    return filename

def is_duplicate(filepath, content):
    """
    Prevent downloading duplicate images by checking file hash.
    """
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, "rb") as f:
        existing_content = f.read()
    
    return hashlib.md5(existing_content).hexdigest() == hashlib.md5(content).hexdigest()

def fetch_image(url):
    """
    Fetch an image from the given URL and save it to Fetched_Images directory.
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs("Fetched_Images", exist_ok=True)

        # Fetch the image with timeout and headers
        headers = {"User-Agent": "UbuntuFetcher/1.0 (Respectful Client)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Respect: Check content type before saving
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ Skipped (Not an image): {url}")
            return

        # Extract filename
        filename = get_filename_from_url(url)
        filepath = os.path.join("Fetched_Images", filename)

        # Check for duplicates
        if is_duplicate(filepath, response.content):
            print(f"⚠ Skipped duplicate: {filename}")
            return

        # Save the image in binary mode
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

def main():
    print("🌍 Welcome to the Ubuntu Image Fetcher 🌍")
    print("A tool for mindfully collecting images from the web\n")

    # Get multiple URLs from user
    urls = input("Enter image URLs (comma-separated): ").split(",")

    for url in urls:
        url = url.strip()
        if url:
            fetch_image(url)

    print("\n✨ Connection strengthened. Community enriched. ✨")

if __name__ == "__main__":
    main()
