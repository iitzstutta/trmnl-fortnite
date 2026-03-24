import requests
import os
import sys
from io import BytesIO
from PIL import Image

# Configuration
TRMNL_API_KEY = os.environ.get("TRMNL_API_KEY")
# Your new ScreenshotOne Key
SCREENSHOT_ONE_KEY = "dQfU64rOlaCiYQ" 
PLUGIN_UUID = "69e73978-1b63-413e-b213-8d59f077baf5"

# The URL of the Juice WRLD stats card
TARGET_URL = "https://fortnite.gg/stats-card?player=Juice%20WRLD%20%E9%AC%BC"

def get_screenshot():
    try:
        # ScreenshotOne API URL
        api_url = "https://api.screenshotone.com/take"
        params = {
            "access_key": SCREENSHOT_ONE_KEY,
            "url": TARGET_URL,
            "format": "png",
            "viewport_width": 1280,
            "viewport_height": 720,
            "block_cookie_banners": "true",
            "wait_until": "networkidle0" # Waits for the stats to actually load
        }
        
        print(f"Requesting screenshot from ScreenshotOne...")
        response = requests.get(api_url, params=params, timeout=60)
        
        if response.status_code != 200:
            print(f"API Error: {response.status_code} - {response.text}")
            return False

        img = Image.open(BytesIO(response.content))
        
        # Resize to TRMNL 800x480
        img = img.resize((800, 480), Image.Resampling.LANCZOS)
        
        # Convert to Grayscale
        img = img.convert("L")

        img.save("display.png")
        print("SUCCESS: Image saved to display.png")
        return True
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        return False

if __name__ == "__main__":
    if get_screenshot():
        github_user = "iitzstutta" 
        repo_name = "trmnl-fortnite"
        raw_url = f"https://raw.githubusercontent.com/{github_user}/{repo_name}/main/display.png"
        
        api_url = f"https://usetrmnl.com/api/custom_plugins/{PLUGIN_UUID}"
        headers = {"Authorization": f"Bearer {TRMNL_API_KEY}", "Content-Type": "application/json"}
        payload = {"merge_variables": {"image_url": raw_url}}
        
        requests.post(api_url, json=payload, headers=headers)
        print("TRMNL notified.")
    else:
        # Fails the GitHub action so you know it didn't work
        sys.exit(1)
