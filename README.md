

# 📱 Samsung Smart Assistant – AI-Powered Samsung Phone Intelligence System

<div align="center">
  <h3>Your Intelligent Samsung Smartphone Companion</h3>
  <p>A Streamlit-powered application that retrieves, analyzes, and explains Samsung phone specifications using RAG , FAISS-based semantic search and Gemini AI.</p>
  <a href="https://drive.google.com/file/d/1zd3r45y6n8vi0RX6xSJMfClH0tVeb75U/view?usp=sharing" target="_blank"><b>🎥 Watch Demo Video</b></a>
</div>

---

## 📑 Table of Contents

* [Core Features](#-core-features)
* [System Architecture](#-system-architecture)
* [Workflow](#-workflow)
* [Technical Components](#-technical-components)
* [Database Setup (PostgreSQL)](#-database-setup-postgresql)
* [Setup Guide](#-setup-guide)
* [Usage](#-usage)
* [Troubleshooting](#-troubleshooting)

---

## 🌟 Core Features

### 🔍 Smart Semantic Phone Lookup

* Search any Samsung model by full or partial name
* Semantic understanding powered by FAISS + Sentence Transformers
* Clean, instant, and context-rich AI responses

### 📊 Intelligent Phone Comparison

* Compare any two Samsung phones
* AI explains differences, pros, and recommendations

### 🔋 Best Battery Recommendation

* Find the best Samsung phone under any budget
* Ranking based on battery capacity extraction

### ⚡ Fast RAG-Based Answering

* Specs converted into vector embeddings
* FAISS retrieves closest matches instantly
* Gemini AI generates human-like summaries

### 🧩 Automatic Fallback System

* If scraping fails → uses backup seed data
* Ensures the app always works

---

## 🏗 System Architecture

```mermaid
graph TD
    A[Frontend: Streamlit UI] --> B[Backend Engine]
    B --> C[Scraper: GSM Arena BD]
    B --> D[RAG Logic]
    B --> E[Comparison Engine]

    C --> F[Structured Spec Builder]
    D --> G[FAISS Vector Store]
    D --> H[Sentence Transformers Embeddings]
    D --> I[Gemini Model API]
    B --> J[PostgreSQL Database]
```

### Backend Stack

* **Frontend:** Streamlit
* **AI Model:** Gemini 2.5 Flash
* **Vector Store:** FAISS
* **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)
* **Database:** PostgreSQL (via SQLAlchemy ORM)
* **Scraping:** BeautifulSoup + Requests

---

## 🔄 Workflow

### 1. Data Collection

* Scraper collects Samsung phones from GSM Arena BD
* Auto-fallback to seed data ensures stability

### 2. Vector Index Building

* Specs transformed into embeddings
* FAISS index created for semantic retrieval

### 3. Query Interpretation

* User queries embedded
* FAISS finds matching phone chunks
* Gemini AI generates the answer

### 4. Comparison & Recommendation

* RAG retrieves both phone specs
* AI generates clean comparison and ranking

---

## 🛠 Technical Components

### 🔍 Semantic Search Example

```python
results = self.index.search(query_embedding, k=3)
```

### 🤖 RAG-Based Answering

```python
response = model.generate_content(
    f"Explain the specs of this phone: {phone_data}"
)
```

### 📊 Comparison Logic

```python
def compare_two(self, p1, p2):
    return self.find_phone(p1), self.find_phone(p2)
```

---

# 🗄 Database Setup (PostgreSQL)

> **You do NOT upload your database to GitHub.**
> Instead, users create it locally using the steps below.

---

## 1️⃣ Install PostgreSQL

Download from:
[https://www.postgresql.org/download/](https://www.postgresql.org/download/)

During installation, note:

* Username (default: `postgres`)
* Password
* Port (default: `5432`)

---

## 2️⃣ Create the Database

Open pgAdmin or terminal:

```sql
CREATE DATABASE samsung_db;
```

---

## 3️⃣ Configure Database URL

Inside `app/db.py`, update your PostgreSQL password:

```python
DATABASE_URL = "postgresql://postgres:YOUR_PASSWORD@localhost:5432/samsung_db"
```

---

## 4️⃣ Create `.env` File

```
GEMINI_API_KEY=your_api_key_here
```

(Never upload `.env` to GitHub.)

---

## 5️⃣ Initialize Tables

Running the app automatically creates all tables:

```bash
streamlit run app/streamlit_app.py
```

---

# 🚀 Setup Guide

### 1. Clone the Repository

```bash
git clone https://github.com/Momit87/samsung-smart-assistant.git
cd samsung-smart-assistant
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run app/streamlit_app.py
```

---

# 🎯 Usage

1. Open the app at `http://localhost:8501`
2. Ask:

   * “Specs of Samsung Galaxy S23 Ultra”
   * “Compare S23 Ultra and A54”
   * “Best battery Samsung phone under $700”
3. View instant AI-generated insights

---

# 🐞 Troubleshooting

### ❌ FAISS Not Found

Install manually:

```bash
pip install faiss-cpu
```

### ❌ Database Connection Error

Check your `DATABASE_URL` inside `db.py`.

### ❌ Gemini API Error

Ensure `.env` contains:

```
GEMINI_API_KEY=your_api_key_here
```

---

<div align="center">
  <h3>✨ Ready to Explore Smartphones the Smart Way?</h3>
  <p><a href="https://drive.google.com/file/d/1zd3r45y6n8vi0RX6xSJMfClH0tVeb75U/view?usp=sharing" target="_blank"><b>🎥 Watch the Project Demo</b></a></p>
</div>

---

