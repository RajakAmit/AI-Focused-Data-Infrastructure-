
---

## 🔧 Technologies Used

- **Airflow** – Task orchestration
- **MinIO** – Object storage (S3-compatible)
- **DuckDB** – In-process analytical DB
- **FastAPI** – REST API for querying
- **SentenceTransformers** – Embedding generation
- **Docker + docker-compose** – For isolated deployment

---

## 🧪 Features

- ✅ Scrapes and stores tech news from BBC
- ✅ Stores raw JSON in MinIO
- ✅ Extracts and embeds articles using sentence transformers
- ✅ Saves metadata and vectors into DuckDB
- ✅ Offers a `/ask` endpoint via FastAPI to query articles using similarity search

---

## ▶️ How to Run

```bash
# Step 1: Clone the repository
git clone https://github.com/RajakAmit/AI-Focused-Data-Infrastructure
cd AI-Focused-Data-Infrastructure

# Step 2: Set up environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Step 3: Run all steps via Makefile
make run_all


# 1. Scrape Data
python src/scraper.py

# 2. Embed and Store
python src/embedder.py

# 3. Start API
uvicorn src.api:app --reload
