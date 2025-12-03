
import os
from dotenv import load_dotenv
import google.generativeai as genai
import re

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

class DataExtractorAgent:
    def __init__(self, rag):
        self.rag = rag

    def extract(self, question):
        q = question.lower()

        if "compare" in q and "and" in q:
            p1, p2 = re.split(r"compare|and", q)[-2:]
            return {
                "type": "compare",
                "data": self.rag.compare_two(p1.strip(), p2.strip()),
            }

        if "best" in q and "battery" in q:
            m = re.search(r"under\s?\$?(\d+)", q)
            limit = int(m.group(1)) if m else 1000
            return {"type": "best_battery", "data": self.rag.best_battery_under(limit)}

        return {"type": "single", "data": self.rag.find_phone(question)}

class ReviewAgent:
    def generate(self, info):
        result = model.generate_content(
            f"You are a Samsung expert. Provide a clear helpful answer:\n{info}"
        )
        return result.text
