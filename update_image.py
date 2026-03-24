import requests
import os
import sys
from io import BytesIO
from PIL import Image

# Configuration
TRMNL_API_KEY = os.environ.get("TRMNL_API_KEY")
ABSTRACT_API_KEY = "e62edcc5906c4acdb7f4e838d0fa7834"
PLUGIN_UUID = "69e73978-1b63-413e-b213-8d59f077baf5"

# The URL of the Juice WRLD stats card
TARGET_URL = "https://fortnite.gg/stats-card?player=Juice%20WRLD%20%E9%AC%BC"

def get_screenshot():
    try:
        # We use the full API string directly here to be safe
        api_url = f"https://screenshots.abstractapi.com/v1/?api_key={ABSTRACT_API_KEY}&url={TARGET_URL}"
        
        print(f"Connecting to AbstractAPI...")
        response = requests.get(api_url, timeout=60) # Increased time to wait
        
        if response.status_code != 200:
            print(f"API Error: {response.status_code} - {response.text}")
            return False

        img = Image.open(BytesIO(response.content))
        img = img.resize((800, 480), Image.Resampling.LANCZOS)
        img = img.convert("L")

        img.save("display.png")
        print("SUCCESS: Image saved to display.png")
        return True
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        return False

if __name__ == "__main__":
    if get_screenshot():
        # Only notify TRMNL if the image actually saved
        github_user = "iitzstutta" 
        repo_name = "trmnl-fortnite"
        raw_url = f"https://raw.githubusercontent.com/{github_user}/{repo_name}/main/display.png"
        
        api_url = f"https://usetrmnl.com/api/custom_plugins/{PLUGIN_UUID}"
        headers = {"Authorization": f"Bearer {TRMNL_API_KEY}", "Content-Type": "application/json"}
        payload = {"merge_variables": {"image_url": raw_url}}
        
        requests.post(api_url, json=payload, headers=headers)
        print("TRMNL notified.")
    else:
        # This tells GitHub the run actually FAILED
        sys.exit(1)
