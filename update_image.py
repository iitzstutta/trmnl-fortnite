import cloudscraper
from bs4 import BeautifulSoup
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

TRMNL_API_KEY = os.environ.get("TRMNL_API_KEY")
PLUGIN_UUID = "69e73978-1b63-413e-b213-8d59f077baf5"
PLAYER_URL = "https://fortnite.gg/stats?player=Juice%20WRLD%20%E9%AC%BC"

def get_stats_and_image():
    try:
        # 1. Bypass Cloudflare using cloudscraper
        scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
        response = scraper.get(PLAYER_URL)
        
        if response.status_code != 200:
            print(f"Bypass failed. Status: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # 2. Grab the Player Avatar
        img_tag = soup.find('img', {'class': 'stats-header-avatar'})
        avatar_url = img_tag['src'] if img_tag else "https://fortnite.gg/img/logo.png"
        if avatar_url.startswith('//'): avatar_url = 'https:' + avatar_url

        # 3. Grab the Stats (Wins, K/D, etc.)
        # We look for the 'value' class which usually holds the numbers
        stats_labels = soup.find_all(class_='stats-profile-label')
        stats_values = soup.find_all(class_='stats-profile-value')
        
        stats_text = ""
        for label, val in zip(stats_labels[:4], stats_values[:4]):
            stats_text += f"{label.text}: {val.text}  "

        # 4. Create a NEW image (800x480) and draw the stats on it
        # This replaces the need for a screenshot!
        img = Image.new('RGB', (800, 480), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Download avatar and paste it
        avatar_resp = scraper.get(avatar_url)
        avatar_img = Image.open(BytesIO(avatar_resp.content)).convert("RGB")
        avatar_img = avatar_img.resize((300, 300))
        img.paste(avatar_img, (50, 50))

        # Add Text (Simple fallback font)
        draw.text((400, 100), "JUICE WRLD STATS", fill=(0,0,0))
        draw.text((400, 150), stats_text, fill=(0,0,0))

        # 5. Final Grayscale conversion
        img = img.convert("L")
        img.save("display.png")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def poke_trmnl():
    github_user = "iitzstutta" 
    repo_name = "trmnl-fortnite"
    raw_url = f"https://raw.githubusercontent.com/{github_user}/{repo_name}/main/display.png"
    
    url = f"https://usetrmnl.com/api/custom_plugins/{PLUGIN_UUID}"
    headers = {"Authorization": f"Bearer {TRMNL_API_KEY}", "Content-Type": "application/json"}
    payload = {"merge_variables": {"image_url": raw_url}}
    
    requests.post(url, json=payload, headers=headers)
    print("TRMNL notified.")

if __name__ == "__main__":
    if get_stats_and_image():
        poke_trmnl()
