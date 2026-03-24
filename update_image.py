import requests
import os
import sys
import time
from io import BytesIO
from PIL import Image

# Configuration
TRMNL_API_KEY = os.environ.get("TRMNL_API_KEY")
ABSTRACT_API_KEY = "e62edcc5906c4acdb7f4e838d0fa7834"
PLUGIN_UUID = "69e73978-1b63-413e-b213-8d59f077baf5"

# The URL of the Juice WRLD stats card
TARGET_URL = "https://fortnite.gg/stats-card?player=Juice%20WRLD%20%E9%AC%BC"

def get_screenshot():
    # We're trying the alternate 'screenshot' subdomain which is often more stable
    api_url = "https://screenshot.abstractapi.com/v1/"
    params = {
        "api_key": ABSTRACT_API_KEY,
        "url": TARGET_URL
    }

    for attempt in range(3): # Try 3 times before giving up
        try:
            print(f"Attempt {attempt + 1}: Connecting to AbstractAPI...")
            response = requests.get(api_url, params=params, timeout=30)
            
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img = img.resize((800, 480), Image.Resampling.LANCZOS)
                img = img.convert("L")
                img.save("display.png")
                print("SUCCESS: Image captured!")
                return True
            else:
                print(f"API Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Connection failed: {e}")
            time.sleep(5) # Wait 5 seconds before retrying
            
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
        print("Final attempt failed. Please check if AbstractAPI is down.")
        sys.exit(1)
