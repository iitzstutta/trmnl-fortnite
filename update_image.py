import requests
import os
import base64
from io import BytesIO
from PIL import Image

TRMNL_API_KEY = os.environ.get("TRMNL_API_KEY")
PLUGIN_UUID = "69e73978-1b63-413e-b213-8d59f077baf5"

# This is the direct link to the generated stats image for that player
IMAGE_URL = "https://fortnite.gg/stats-card?player=Juice%20WRLD%20%E9%AC%BC"

def process_and_save_image():
    try:
        # 1. Download the image
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(IMAGE_URL, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"Failed to download image. Status: {response.status_code}")
            return False

        # 2. Open and Format
        img = Image.open(BytesIO(response.content))
        if img.mode in ("RGBA", "P"): 
            img = img.convert("RGB")
        
        # 3. Resize to 800x480 (TRMNL Standard)
        # This will 'squish' the 1080p image to fit your screen exactly
        img = img.resize((800, 480), Image.Resampling.LANCZOS)
        
        # 4. Convert to Grayscale
        img = img.convert("L")

        # 5. Save locally for GitHub to host
        img.save("display.png")
        print("Successfully saved Juice WRLD stats image!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def poke_trmnl():
    github_user = "iitzstutta" 
    repo_name = "trmnl-fortnite"
    # This link is what TRMNL will use to find the image we just saved
    raw_url = f"https://raw.githubusercontent.com/{github_user}/{repo_name}/main/display.png"
    
    api_url = f"https://usetrmnl.com/api/custom_plugins/{PLUGIN_UUID}"
    headers = {"Authorization": f"Bearer {TRMNL_API_KEY}", "Content-Type": "application/json"}
    payload = {"merge_variables": {"image_url": raw_url}}
    
    requests.post(api_url, json=payload, headers=headers)
    print(f"TRMNL notified to grab: {raw_url}")

if __name__ == "__main__":
    if process_and_save_image():
        poke_trmnl()
