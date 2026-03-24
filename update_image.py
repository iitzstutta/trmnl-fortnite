import requests
from bs4 import BeautifulSoup
import os
import base64
from io import BytesIO
from PIL import Image

TRMNL_API_KEY = os.environ.get("TRMNL_API_KEY")
# Ensure this matches your dashboard exactly
PLUGIN_UUID = "69e73978-1b63-413e-b213-8d59f077baf5"
STATS_URL = "https://fortnite.gg/stats?player=Juice%20WRLD%20%E9%AC%BC"

def get_and_process_image():
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(STATS_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        img_tag = soup.find('img', {'class': 'stats-header-avatar'})
        
        if img_tag and img_tag.get('src'):
            image_source = img_tag['src']
        else:
            image_source = "https://fortnite.gg/img/logo.png"

        if "base64," in image_source:
            img_data = image_source.split("base64,")[1]
            binary_data = base64.b64decode(img_data)
        else:
            if image_source.startswith('//'):
                image_source = 'https:' + image_source
            img_response = requests.get(image_source, timeout=10)
            binary_data = img_response.content

        img = Image.open(BytesIO(binary_data))
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Resize to TRMNL standard
        img = img.resize((800, 480), Image.Resampling.LANCZOS)
        img = img.convert("L")

        buffered = BytesIO()
        # We use PNG here as it's sometimes more reliable for Base64 layouts
        img.save(buffered, format="PNG")
        final_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{final_base64}"
            
    except Exception as e:
        print(f"Error: {e}")
        return None

def send_to_screen():
    image_data = get_and_process_image()
    
    if not image_data:
        return

    # THE FIX IS HERE: TRMNL wants the 'merge_variables' inside a 'data' object
    url = f"https://usetrmnl.com/api/custom_plugins/{PLUGIN_UUID}"
    headers = {
        "Authorization": f"Bearer {TRMNL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "merge_variables": {
            "image_url": image_data
        }
    }
    
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    send_to_screen()
