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
        # We use a very specific Header to make the website think we are a real Chrome browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
        response = requests.get(STATS_URL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # FIND THE IMAGE: We look for the avatar specifically inside the stats-header
        img_tag = soup.find('img', {'class': 'stats-header-avatar'})
        
        if img_tag and img_tag.get('src'):
            image_source = img_tag['src']
            print(f"DEBUG: Found Player Image: {image_source[:50]}...")
        else:
            # Fallback if the site blocks the specific avatar
            print("DEBUG: Avatar not found, looking for any large player image...")
            all_imgs = soup.find_all('img')
            # Look for an image that likely contains 'fnbr' or 'outfit' in the link
            image_source = next((i['src'] for i in all_imgs if 'fnbr.co' in i.get('src', '') or 'outfit' in i.get('src', '')), "https://fortnite.gg/img/logo.png")

        # 1. Get the raw bytes of the image
        if "base64," in image_source:
            img_data = image_source.split("base64,")[1]
            binary_data = base64.b64decode(img_data)
        else:
            if image_source.startswith('//'): image_source = 'https:' + image_source
            binary_data = requests.get(image_source).content

        # 2. Open and Format
        img = Image.open(BytesIO(binary_data))
        if img.mode in ("RGBA", "P"): 
            img = img.convert("RGB")
        
        # 3. Resize and Grayscale
        # 800x480 for TRMNL
        img = img.resize((800, 480), Image.Resampling.LANCZOS)
        img = img.convert("L")

        # 4. Save
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
    print(f"Update sent to TRMNL!")

if __name__ == "__main__":
    if process_and_save_image():
        poke_trmnl()
