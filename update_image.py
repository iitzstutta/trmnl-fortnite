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
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(STATS_URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tag = soup.find('img', {'class': 'stats-header-avatar'})
        
        if not img_tag or not img_tag.get('src'):
            return None

        img_data = img_tag['src']

        # If it's Base64, strip the header so we just have the raw data
        if "base64," in img_data:
            header, img_data = img_data.split("base64,")
        
        # 1. Convert Base64 text back into actual image bytes
        binary_data = base64.b64decode(img_data)
        img = Image.open(BytesIO(binary_data))

        # 2. Resize (Squish) to fit TRMNL (800x480 is standard)
        # We use LANCZOS to keep it looking high-quality
        img = img.resize((800, 480), Image.Resampling.LANCZOS)

        # 3. Convert to Grayscale (Perfect for E-ink)
        img = img.convert("L")

        # 4. Turn it back into a small Base64 string to send to TRMNL
        buffered = BytesIO()
        img.save(buffered, format="JPEG", quality=85)
        final_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/jpeg;base64,{final_base64}"
            
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def send_to_screen():
    image_url = get_and_process_image()
    
    if not image_url:
        print("Failed to process image.")
        return

    url = f"https://usetrmnl.com/api/custom_plugins/{PLUGIN_UUID}"
    headers = {"Authorization": f"Bearer {TRMNL_API_KEY}", "Content-Type": "application/json"}
    payload = {"merge_variables": {"image_url": image_url}}
    
    print("Success! Image resized and converted.")
    requests.post(url, json=payload, headers=headers)

if __name__ == "__main__":
    send_to_screen()
