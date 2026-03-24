import requests
import os
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
        # We are using the simplest possible URL for the API
        api_url = "https://screenshots.abstractapi.com/v1/"
        params = {
            "api_key": ABSTRACT_API_KEY,
            "url": TARGET_URL
        }
        
        print(f"Requesting screenshot for {TARGET_URL}...")
        # We use 'params' here which is cleaner and prevents typos
        response = requests.get(api_url, params=params, timeout=30)
        
        if response.status_code != 200:
            print(f"API Error: {response.status_code} - {response.text}")
            return False

        img = Image.open(BytesIO(response.content))
        img = img.resize((800, 480), Image.Resampling.LANCZOS)
        img = img.convert("L")

        img.save("display.png")
        print("Screenshot saved successfully!")
        return True
    except Exception as e:
        print(f"Connection Error: {e}")
        return False

def poke_trmnl():
    github_user = "iitzstutta" 
    repo_name = "trmnl-fortnite"
    raw_url = f"https://raw.githubusercontent.com/{github_user}/{repo_name}/main/display.png"
    
    api_url = f"https://usetrmnl.com/api/custom_plugins/{PLUGIN_UUID}"
    headers = {"Authorization": f"Bearer {TRMNL_API_KEY}", "Content-Type": "application/json"}
    payload = {"merge_variables": {"image_url": raw_url}}
    
    requests.post(api_url, json=payload, headers=headers)
    print("TRMNL notified.")

if __name__ == "__main__":
    if get_screenshot():
        poke_trmnl()
