# app/rag.py

from app.db import Phone, SessionLocal
from app.faiss_store import FAISSStore

class RAG:
    def __init__(self):
        self.session = SessionLocal()
        self.store = FAISSStore()

        phones = self.session.query(Phone).all()
        for p in phones:
            text = (
                f"Model: {p.model_name}. Release: {p.release_date}. Display: {p.display}. "
                f"Battery: {p.battery}. Camera: {p.camera}. RAM: {p.ram}. "
                f"Storage: {p.storage}. Price: {p.price}."
            )
            self.store.add(
                text=text,
                metadata={
                    "model_name": p.model_name,
                    "release_date": p.release_date,
                    "display": p.display,
                    "battery": p.battery,
                    "camera": p.camera,
                    "ram": p.ram,
                    "storage": p.storage,
                    "price": p.price,
                },
            )

    # ---- semantic-based single phone retrieval ----
    def find_phone(self, query):
        results = self.store.search(query, k=1)
        return results[0] if results else None

    # ---- compare two models semantically ----
    def compare_two(self, p1, p2):
        r1 = self.find_phone(p1)
        r2 = self.find_phone(p2)
        return r1, r2

    # ---- best battery under budget ----
    def best_battery_under(self, price_limit):
        phones = self.session.query(Phone).all()

        def extract_mAh(text):
            import re
            m = re.search(r"(\d+)\s?mAh", str(text))
            return int(m.group(1)) if m else 0

        def extract_price(p):
            try:
                return float(str(p.price).replace("$", "").replace(",", ""))
            except:
                return 999999

        filtered = [p for p in phones if extract_price(p) <= price_limit]
        if not filtered:
            return None

        best = max(filtered, key=lambda x: extract_mAh(x.battery))

        return {
            "model_name": best.model_name,
            "battery": best.battery,
            "price": best.price,
            "display": best.display,
            "camera": best.camera,
            "ram": best.ram,
            "storage": best.storage,
        }
    # ---- phones with best camera ----
    def best_camera(self, top_k=5):
        phones = self.session.query(Phone).all()

        def extract_camera_mp(text):
            import re
            m = re.search(r"(\d+)\s?MP", str(text))
            return int(m.group(1)) if m else 0

        sorted_phones = sorted(phones, key=lambda x: extract_camera_mp(x.camera), reverse=True)
        top_phones = sorted_phones[:top_k]

        results = []
        for p in top_phones:
            results.append({
                "model_name": p.model_name,
                "camera": p.camera,
                "price": p.price,
                "display": p.display,
                "battery": p.battery,
                "ram": p.ram,
                "storage": p.storage,
            })
        return results
    # ---- phones with largest display ----
    def largest_display(self, top_k=5):
        phones = self.session.query(Phone).all()

        def extract_display_size(text):
            import re
            m = re.search(r"(\d+(\.\d+)?)\s?inch", str(text))
            return float(m.group(1)) if m else 0.0

        sorted_phones = sorted(phones, key=lambda x: extract_display_size(x.display), reverse=True)
        top_phones = sorted_phones[:top_k]

        results = []
        for p in top_phones:
            results.append({
                "model_name": p.model_name,
                "display": p.display,
                "price": p.price,
                "battery": p.battery,
                "camera": p.camera,
                "ram": p.ram,
                "storage": p.storage,
            })
        return results
    # ---- phones with highest RAM ----
    def highest_ram(self, top_k=5):
        phones = self.session.query(Phone).all()

        def extract_ram_size(text):
            import re
            m = re.search(r"(\d+)\s?GB", str(text))
            return int(m.group(1)) if m else 0

        sorted_phones = sorted(phones, key=lambda x: extract_ram_size(x.ram), reverse=True)
        top_phones = sorted_phones[:top_k]

        results = []
        for p in top_phones:
            results.append({
                "model_name": p.model_name,
                "ram": p.ram,
                "price": p.price,
                "display": p.display,
                "battery": p.battery,
                "camera": p.camera,
                "storage": p.storage,
            })
        return results
    # ---- phones with largest storage ----
    def largest_storage(self, top_k=5):
        phones = self.session.query(Phone).all()

        def extract_storage_size(text):
            import re
            m = re.search(r"(\d+)\s?GB", str(text))
            return int(m.group(1)) if m else 0

        sorted_phones = sorted(phones, key=lambda x: extract_storage_size(x.storage), reverse=True)
        top_phones = sorted_phones[:top_k]

        results = []
        for p in top_phones:
            results.append({
                "model_name": p.model_name,
                "storage": p.storage,
                "price": p.price,
                "display": p.display,
                "battery": p.battery,
                "camera": p.camera,
                "ram": p.ram,
            })
        return results
   