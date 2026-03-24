import requests
import os
from io import BytesIO
from PIL import Image

TRMNL_API_KEY = os.environ.get("TRMNL_API_KEY")
PLUGIN_UUID = "69e73978-1b63-413e-b213-8d59f077baf5"

# We are going to use a 'WSRV' proxy. 
# This service downloads the image FOR us and sends it back. 
# It's great for bypassing 403 blocks.
SOURCE_URL = "https://fortnite.gg/stats-card?player=Juice%20WRLD%20%E9%AC%BC"
PROXY_URL = f"https://wsrv.nl/?url={SOURCE_URL}&output=png"

def process_and_save_image():
    try:
        print(f"Asking Proxy to grab image...")
        response = requests.get(PROXY_URL, timeout=30)
        
        if response.status_code != 200:
            print(f"Proxy also blocked or failed. Status: {response.status_code}")
            return False

        img = Image.open(BytesIO(response.content))
        if img.mode in ("RGBA", "P"): 
            img = img.convert("RGB")
        
        # Resize to 800x480
        img = img.resize((800, 480), Image.Resampling.LANCZOS)
        img = img.convert("L")

        img.save("display.png")
        print("Successfully saved image via Proxy!")
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
    print("TRMNL notified.")

if __name__ == "__main__":
    if process_and_save_image():
        poke_trmnl()
