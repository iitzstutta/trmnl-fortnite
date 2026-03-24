import requests
from bs4 import BeautifulSoup
import os

# 1. Your ID and Key
TRMNL_API_KEY = os.environ.get("TRMNL_API_KEY")
PLUGIN_UUID = "69e73978-1b63-413e-b213-8d59f077baf5"

# 2. The Website to "Scrape"
STATS_URL = "https://fortnite.gg/stats?player=Juice%20WRLD%20%E9%AC%BC"

def get_fortnite_image():
    try:
        # Ask the website for its content
        response = requests.get(STATS_URL, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for the main character image on fortnite.gg
        # It usually lives in an <img> tag inside the 'stats-header'
        img_tag = soup.find('img', {'class': 'stats-header-avatar'})
        
        if img_tag and img_tag.get('src'):
            img_url = img_tag['src']
            # Make sure it's a full URL
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            return img_url
        
        return None
    except Exception as e:
        print(f"Error finding image: {e}")
        return None

def send_to_screen():
    image_url = get_fortnite_image()
    
    if not image_url:
        print("Could not find the player image on the page.")
        return

    url = f"https://usetrmnl.com/api/custom_plugins/{PLUGIN_UUID}"
    headers = {
        "Authorization": f"Bearer {TRMNL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "merge_variables": {
            "image_url": image_url
        }
    }
    
    print(f"Found image: {image_url}")
    print(f"Sending to TRMNL...")
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status: {response.status_code}")

if __name__ == "__main__":
    send_to_screen()
