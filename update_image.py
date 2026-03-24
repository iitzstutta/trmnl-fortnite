import requests
import os
import base64
from io import BytesIO
from PIL import Image

TRMNL_API_KEY = os.environ.get("TRMNL_API_KEY")
PLUGIN_UUID = "69e73978-1b63-413e-b213-8d59f077baf5"

# The direct link to the card
IMAGE_URL = "https://fortnite.gg/stats-card?player=Juice%20WRLD%20%E9%AC%BC"

def process_and_save_image():
    try:
        # We are using a much more convincing "ID Card" here
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://fortnite.gg/'
        }
        
        print(f"Attempting to download from: {IMAGE_URL}")
        response = requests.get(IMAGE_URL, headers=headers, timeout=20)
        
        if response.status_code != 200:
            print(f"Still blocked! Status: {response.status_code}")
            # If the direct card is blocked, let's try a backup player image
            return False

        img = Image.open(BytesIO(response.content))
        if img.mode in ("RGBA", "P"): 
            img = img.convert("RGB")
        
        img = img.resize((800, 480), Image.Resampling.LANCZOS)
        img = img.convert("L")

        img.save("display.png")
        print("Successfully saved image!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def poke_trmnl():
    github_user = "iitzstutta" 
    repo_name = "trmnl-fortnite"
    raw_url = f"https://raw.githubusercontent.com/{github_user}/{repo_name}/main/display.png"
    
    api_url = f"https://usetrmnl.com/api/custom_plugins/{PLUGIN_UUID}"
    headers = {"Authorization": f"Bearer {TRMNL_API_KEY}", "Content-Type": "application/json"}
    payload = {"merge_variables": {"image_url": raw_url}}
    
    requests.post(api_url, json=payload, headers=headers)
    print(f"TRMNL notified.")

if __name__ == "__main__":
    if process_and_save_image():
        poke_trmnl()
