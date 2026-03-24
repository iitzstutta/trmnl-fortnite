import requests
from bs4 import BeautifulSoup
import os

TRMNL_API_KEY = os.environ.get("TRMNL_API_KEY")
PLUGIN_UUID = "69e73978-1b63-413e-b213-8d59f077baf5"
STATS_URL = "https://fortnite.gg/stats?player=Juice%20WRLD%20%E9%AC%BC"

def get_fortnite_image():
    try:
        # We pretend to be a real web browser so the site doesn't block us
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.31'}
        response = requests.get(STATS_URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Strategy 1: Look for the big avatar image
        img = soup.find('img', {'class': 'stats-header-avatar'})
        
        # Strategy 2: If that fails, look for any image in the header
        if not img:
            header = soup.find('div', {'class': 'stats-header'})
            if header:
                img = header.find('img')

        if img and img.get('src'):
            img_url = img['src']
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            return img_url
        
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def send_to_screen():
    image_url = get_fortnite_image()
    
    if not image_url:
        # If we still can't find it, we'll use a backup Fortnite logo so your screen isn't blank
        print("Could not find player image, using backup logo.")
        image_url = "https://fortnite.gg/img/logo.png"

    url = f"https://usetrmnl.com/api/custom_plugins/{PLUGIN_UUID}"
    headers = {"Authorization": f"Bearer {TRMNL_API_KEY}", "Content-Type": "application/json"}
    payload = {"merge_variables": {"image_url": image_url}}
    
    print(f"Sending this image to TRMNL: {image_url}")
    requests.post(url, json=payload, headers=headers)

if __name__ == "__main__":
    send_to_screen()
