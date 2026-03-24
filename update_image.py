import requests
import os
from io import BytesIO
from PIL import Image

# Configuration
TRMNL_API_KEY = os.environ.get("TRMNL_API_KEY")
# Using the key you provided directly to make it easier for you
ABSTRACT_API_KEY = "e62edcc5906c4acdb7f4e838d0fa7834"
PLUGIN_UUID = "69e73978-1b63-413e-b213-8d59f077baf5"

# The URL of the Juice WRLD stats card
TARGET_URL = "https://fortnite.gg/stats-card?player=Juice%20WRLD%20%E9%AC%BC"

def get_screenshot():
    try:
        # We call AbstractAPI to take a "picture" of the website for us
        # this bypasses the 403 blocks because Abstract uses a real browser
        api_url = f"https://screenshots.abstractapi.com/v1/?api_key={ABSTRACT_API_KEY}&url={TARGET_URL}"
        
        print("Requesting screenshot from AbstractAPI...")
        response = requests.get(api_url, timeout=30)
        
        if response.status_code != 200:
            print(f"API Error: {response.status_code} - {response.text}")
            return False

        # Process the image bytes
        img = Image.open(BytesIO(response.content))
        
        # Resize to TRMNL 800x480
        img = img.resize((800, 480), Image.Resampling.LANCZOS)
        
        # Convert to Grayscale for e-ink
        img = img.convert("L")

        # Save to the repo
        img.save("display.png")
        print("Screenshot saved successfully as display.png!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def poke_trmnl():
    github_user = "iitzstutta" 
    repo_name = "trmnl-fortnite"
    # The URL TRMNL will use to download our processed image
    raw_url = f"https://raw.githubusercontent.com/{github_user}/{repo_name}/main/display.png"
    
    api_url = f"https://usetrmnl.com/api/custom_plugins/{PLUGIN_UUID}"
    headers = {
        "Authorization": f"Bearer {TRMNL_API_KEY}", 
        "Content-Type": "application/json"
    }
    payload = {"merge_variables": {"image_url": raw_url}}
    
    response = requests.post(api_url, json=payload, headers=headers)
    print(f"TRMNL notified. Status: {response.status_code}")

if __name__ == "__main__":
    if get_screenshot():
        poke_trmnl()
