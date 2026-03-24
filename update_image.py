import requests
from bs4 import BeautifulSoup
import os
import base64
from io import BytesIO
from PIL import Image

TRMNL_API_KEY = os.environ.get("TRMNL_API_KEY")
PLUGIN_UUID = "69e73978-1b63-413e-b213-8d59f077baf5"
STATS_URL = "https://fortnite.gg/stats?player=Juice%20WRLD%20%E9%AC%BC"

def get_and_process_image():
    image_source = None
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        response = requests.get(STATS_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for the specific avatar image
        img_tag = soup.find('img', {'class': 'stats-header-avatar'})
        
        if img_tag and img_tag.get('src'):
            image_source = img_tag['src']
        else:
            # Backup: Just use a high-res Fortnite logo so we can test the resize logic
            print("Could not find player avatar, using backup logo.")
            image_source = "https://fortnite.gg/img/logo.png"

        # Handle Base64 vs URL
        if "base64," in image_source:
            img_data = image_source.split("base64,")[1]
            binary_data = base64.b64decode(img_data)
        else:
            if image_source.startswith('//'):
                image_source = 'https:' + image_source
            img_response = requests.get(image_source, timeout=10)
            binary_data = img_response.content

        # PROCESS THE IMAGE
        img = Image.open(BytesIO(binary_data))
        
        # Convert to RGB if it's a PNG with transparency (prevents errors)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Resize/Squish to 800x480
        img = img.resize((800, 480), Image.Resampling.LANCZOS)
        
        # Convert to Grayscale
        img = img.convert("L")

        # Prep for TRMNL
        buffered = BytesIO()
        img.save(buffered, format="JPEG", quality=85)
        final_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/jpeg;base64,{final_base64}"
            
    except Exception as e:
        print(f"Error details: {e}")
        return None

def send_to_screen():
    image_url = get_and_process_image()
    
    if not image_url:
        print("Everything failed. Check your URL or TRMNL keys.")
        return

    url = f"https://usetrmnl.com/api/custom_plugins/{PLUGIN_UUID}"
    headers = {"Authorization": f"Bearer {TRMNL_API_KEY}", "Content-Type": "application/json"}
    payload = {"merge_variables": {"image_url": image_url}}
    
    response = requests.post(url, json=payload, headers=headers)
    print(f"Sent to TRMNL. Response code: {response.status_code}")

if __name__ == "__main__":
    send_to_screen()
