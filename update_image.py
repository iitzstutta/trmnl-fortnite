import cloudscraper
from bs4 import BeautifulSoup
import os
from io import BytesIO
from PIL import Image, ImageDraw

TRMNL_API_KEY = os.environ.get("TRMNL_API_KEY")
PLUGIN_UUID = "69e73978-1b63-413e-b213-8d59f077baf5"
PLAYER_URL = "https://fortnite.gg/stats?player=Juice%20WRLD%20%E9%AC%BC"

def get_stats_and_image():
    try:
        # 1. Bypass Cloudflare
        scraper = cloudscraper.create_scraper()
        response = scraper.get(PLAYER_URL)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 2. Get Avatar
        img_tag = soup.find('img', {'class': 'stats-header-avatar'})
        avatar_url = img_tag['src'] if img_tag else "https://fortnite.gg/img/logo.png"
        if avatar_url.startswith('//'): avatar_url = 'https:' + avatar_url

        # 3. Create the TRMNL Canvas (800x480)
        img = Image.new('RGB', (800, 480), color=(255, 255, 255))
        
        # Download and paste the Juice WRLD character
        avatar_resp = scraper.get(avatar_url)
        avatar_img = Image.open(BytesIO(avatar_resp.content)).convert("RGB")
        
        # Resize avatar to fit the left side
        avatar_img = avatar_img.resize((400, 400), Image.Resampling.LANCZOS)
        img.paste(avatar_img, (20, 40))

        # 4. Final conversion to Grayscale
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
    import requests # Ensure requests is available here
    if get_stats_and_image():
        poke_trmnl()
