import requests
import os

# 1. Your ID and Key
# This grabs the API Key you saved in GitHub Secrets
TRMNL_API_KEY = os.environ.get("TRMNL_API_KEY")
# Your specific Plugin UUID
PLUGIN_UUID = "69e73978-1b63-413e-b213-8d59f077baf5" 

# 2. The image you want to see (You can change this URL later!)
IMAGE_URL = "https://images.nasa.gov/images/pic_of_the_day.jpg" 

def send_to_screen():
    # This is the "address" of your specific TRMNL plugin
    url = f"https://usetrmnl.com/api/custom_plugins/{PLUGIN_UUID}"
    
    headers = {
        "Authorization": f"Bearer {TRMNL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # This matches the {{ image_url }} tag you put in your TRMNL HTML
    payload = {
        "merge_variables": {
            "image_url": IMAGE_URL
        }
    }
    
    print(f"Sending request to TRMNL...")
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("Success! Your screen should update shortly.")
    else:
        print(f"Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    send_to_screen()
