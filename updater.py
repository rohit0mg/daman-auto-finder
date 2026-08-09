import os
import re
import requests

GIST_TOKEN = os.environ.get("GIST_TOKEN")
GIST_ID = os.environ.get("GIST_ID")
MAIN_SITE = "https://damanclub.in"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36"
}

def find_latest_api():
    try:
        res = requests.get(MAIN_SITE, headers=HEADERS, timeout=10)
        matches = re.findall(r'https?://api\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', res.text)
        if matches:
            return matches[0]
    except Exception as e:
        print("Error scanning main site:", e)
    return None

def update_gist(new_api_url):
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {
        "Authorization": f"token {GIST_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "files": {
            "daman_api.txt": {
                "content": new_api_url
            }
        }
    }
    res = requests.patch(url, json=payload, headers=headers)
    if res.status_code == 200:
        print(f"✅ Gist updated to: {new_api_url}")
    else:
        print("❌ Gist Update Failed:", res.text)

if __name__ == "__main__":
    latest_api = find_latest_api()
    if latest_api:
        update_gist(latest_api)
    else:
        print("⚠️ API not found on main site.")
      
