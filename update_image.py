import requests
from bs4 import BeautifulSoup
import os
import base64
from io import BytesIO
from PIL import Image

TRMNL_API_KEY = os.environ.get("TRMNL_API_KEY")
PLUGIN_UUID = "69e73978-1b63-413e-b213-8d59f077baf5"
STATS_URL = "https://fortnite.gg/stats?player=Juice%20WRLD%20%E9%AC%BC"

def process_and_save_image():
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(STATS_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tag = soup.find('img', {'class': 'stats-header-avatar'})
        
        image_source = img_tag['src'] if img_tag else "https://fortnite.gg/img/logo.png"

        if "base64," in image_source:
            img_data = image_source.split("base64,")[1]
            binary_data = base64.b64decode(img_data)
        else:
            if image_source.startswith('//'): image_source = 'https:' + image_source
            binary_data = requests.get(image_source).content

        img = Image.open(BytesIO(binary_data))
        if img.mode in ("RGBA", "P"): img = img.convert("RGB")
        
        # Resize and Grayscale
        img = img.resize((800, 480), Image.Resampling.LANCZOS)
        img = img.convert("L")

        # SAVE THE IMAGE LOCALLY
        img.save("display.png")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def poke_trmnl():
    # Replace 'YOUR_GITHUB_USERNAME' with your actual GitHub username!
    github_user = "itstutta" # Based on your screenshot
    image_url = f"https://raw.githubusercontent.com/{github_user}/trmnl-fortnite/main/display.png"
    
    url = f"https://usetrmnl.com/api/custom_plugins/{PLUGIN_UUID}"
    headers = {"Authorization": f"Bearer {TRMNL_API_KEY}", "Content-Type": "application/json"}
    payload = {"merge_variables": {"image_url": image_url}}
    
    requests.post(url, json=payload, headers=headers)
    print(f"Told TRMNL to grab image from: {image_url}")

if __name__ == "__main__":
    if process_and_save_image():
        poke_trmnl()
