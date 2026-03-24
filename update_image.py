import requests
from bs4 import BeautifulSoup
import os
import base64
from io import BytesIO
from PIL import Image

TRMNL_API_KEY = os.environ.get("TRMNL_API_KEY")
PLUGIN_UUID = "69e73978-1b63-413e-b213-8d59f077baf5"
# The exact URL for the player
STATS_URL = "https://fortnite.gg/stats?player=Juice%20WRLD%20%E9%AC%BC"

def process_and_save_image():
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(STATS_URL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # New Strategy: Look for the specific 'og:image' meta tag. 
        # This is what social media sites use to show a preview, and it usually contains the player avatar!
        meta_img = soup.find("meta", property="og:image")
        
        if meta_img and meta_img.get("content"):
            image_source = meta_img["content"]
            print(f"Found image via Meta Tag: {image_source}")
        else:
            # Plan C: Look for the first image that mentions 'fnbr' or 'outfit'
            print("Meta tag failed, searching all images...")
            all_imgs = [img.get('src') for img in soup.find_all('img') if img.get('src')]
            image_source = next((s for s in all_imgs if "outfit" in s or "fnbr" in s), None)

        if not image_source:
            print("Still nothing. Using logo as ultimate fallback.")
            image_source = "https://fortnite.gg/img/logo.png"

        # Download and Format
        if image_source.startswith('//'): image_source = 'https:' + image_source
        binary_data = requests.get(image_source).content

        img = Image.open(BytesIO(binary_data))
        if img.mode in ("RGBA", "P"): img = img.convert("RGB")
        
        # Resize to 800x480
        img = img.resize((800, 480), Image.Resampling.LANCZOS)
        img = img.convert("L")

        img.save("display.png")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def poke_trmnl():
    github_user = "iitzstutta" 
    repo_name = "trmnl-fortnite"
    image_url = f"https://raw.githubusercontent.com/{github_user}/{repo_name}/main/display.png"
    
    url = f"https://usetrmnl.com/api/custom_plugins/{PLUGIN_UUID}"
    headers = {"Authorization": f"Bearer {TRMNL_API_KEY}", "Content-Type": "application/json"}
    payload = {"merge_variables": {"image_url": image_url}}
    
    requests.post(url, json=payload, headers=headers)
    print("Update sent to TRMNL!")

if __name__ == "__main__":
    if process_and_save_image():
        poke_trmnl()
