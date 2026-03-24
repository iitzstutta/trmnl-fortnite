import requests
import os
import sys
from io import BytesIO
from PIL import Image

TRMNL_API_KEY = os.environ.get("TRMNL_API_KEY")
SCREENSHOT_ONE_KEY = "dQfU64rOlaCiYQ" 
PLUGIN_UUID = "69e73978-1b63-413e-b213-8d59f077baf5"
TARGET_URL = "https://fortnite.gg/stats?player=Juice%20WRLD%20%E9%AC%BC"

def get_screenshot():
    try:
        api_url = "https://api.screenshotone.com/take"
        params = {
            "access_key": SCREENSHOT_ONE_KEY,
            "url": TARGET_URL,
            "format": "png",
            "viewport_width": 1280,
            "viewport_height": 720,
            "block_cookie_banners": "true",
            "block_ads": "true",
            "delay": 15, # Increased to 15 seconds to ENSURE stats load
            "selector": ".stats-profile-stats", # Switched selector to just the stat boxes
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "wait_until": "networkidle2" # Wait for all data to finish moving
        }
        
        print(f"Requesting screenshot...")
        response = requests.get(api_url, params=params, timeout=90)
        
        if response.status_code != 200:
            print(f"API Error: {response.status_code}")
            return False

        img = Image.open(BytesIO(response.content))
        img = img.resize((800, 480), Image.Resampling.LANCZOS).convert("L")
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
        sys.exit(1)
