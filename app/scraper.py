
import requests
import time
from bs4 import BeautifulSoup
from app.db import Phone, SessionLocal
from app.seed_data import SEED_DATA

BASE_URL = "https://www.gsmarena.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def safe_get(url, retries=3):
    for _ in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=8)
            if r.status_code == 200:
                return r.text
        except:
            pass
        time.sleep(1)
    return None

def scrape_samsung_list():
    html = safe_get(f"{BASE_URL}/samsung-phones-9.php")
    if html is None:
        return []
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("div.makers ul li a") or []
    phones = []
    for item in items[:25]:
        name = item.text.strip()
        url = BASE_URL + "/" + item["href"]
        phones.append((name, url))
    return phones

def scrape_specs(name, url):
    html = safe_get(url)
    if html is None:
        return {"model_name": name, "battery": "Unknown"}
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.select("table")

    def extract(section):
        for t in tables:
            if section.lower() in t.get_text().lower():
                return t.get_text(separator=" ", strip=True)
        return "Unknown"

    return {
        "model_name": name,
        "release_date": extract("launch"),
        "display": extract("display"),
        "battery": extract("battery"),
        "camera": extract("camera"),
        "ram": extract("memory"),
        "storage": extract("internal"),
        "price": extract("price"),
    }

def save_seed_data():
    session = SessionLocal()
    count = 0
    for p in SEED_DATA:
        session.add(
            Phone(
                model_name=p["model_name"],
                release_date=p["release_date"],
                display=p["display_size"],
                battery=p["battery"],
                camera=p["camera_main"],
                ram=p["ram"],
                storage=p["storage"],
                price=str(p["price_usd"]),
            )
        )
        count += 1
    session.commit()
    session.close()
    return count

def run_scraper(use_backup=False):
    session = SessionLocal()

    if use_backup:
        return save_seed_data()

    phones = scrape_samsung_list()
    if not phones:
        return save_seed_data()

    for name, url in phones:
        specs = scrape_specs(name, url)
        session.add(Phone(**specs))

    session.commit()
    session.close()
    return len(phones)

