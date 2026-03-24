import requests
from bs4 import BeautifulSoup
import os

TRMNL_API_KEY = os.environ.get("TRMNL_API_KEY")
PLUGIN_UUID = "69e73978-1b63-413e-b213-8d59f077baf5"
STATS_URL = "https://fortnite.gg/stats?player=Juice%20WRLD%20%E9%AC%BC"

def get_fortnite_image():
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        response = requests.get(STATS_URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # We search for the image again, but this time we are looking specifically
        # for that "data:image" text you saw when right-clicking.
        img_tag = soup.find('img', {'class': 'stats-header-avatar'})
        
        if img_tag and img_tag.get('src'):
            img_data = img_tag['src']
            # This checks if it's the "Base64" type you found
            if img_data.startswith('data:image'):
                return img_data
            
            # If it's a normal link, we fix it up
            if img_data.startswith('//'):
                return 'https:' + img_data
            return img_data
            
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def send_to_screen():
    image_url = get_fortnite_image()
    
    if not image_url:
        print("Still couldn't find that specific image. Using backup.")
        image_url = "https://fortnite.gg/img/logo.png"

    url = f"https://usetrmnl.com/api/custom_plugins/{PLUGIN_UUID}"
    headers = {"Authorization": f"Bearer {TRMNL_API_KEY}", "Content-Type": "application/json"}
    
    # We send the giant block of image text to TRMNL
    payload = {"merge_variables": {"image_url": image_url}}
    
    print(f"Success! Captured the image data.")
    response = requests.post(url, json=payload, headers=headers)
    print(f"TRMNL Response: {response.status_code}")

if __name__ == "__main__":
    send_to_screen()
