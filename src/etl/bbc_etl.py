
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import os
import pathlib

import pandas as pd
from dotenv import load_dotenv

from src.utils.s3 import put_object  # Ensure this uploads to MinIO

# Load environment variables
load_dotenv()

def run_etl():
    raw_dir = pathlib.Path("data/raw")
    
    # Find latest scraped file
    latest_file = max(raw_dir.glob("bbc_tech_*.json"), key=os.path.getctime)
    print(f"🔍 Loading raw data from: {latest_file.name}")

    df_raw = pd.read_json(latest_file)

    # ----------------- BRONZE -----------------
    bronze_dir = pathlib.Path("data/bronze")
    bronze_dir.mkdir(parents=True, exist_ok=True)
    bronze_path = bronze_dir / "bronze.parquet"
    df_raw.to_parquet(bronze_path, index=False)
    print("✅ Bronze data saved.")

    # ----------------- SILVER -----------------
    df_silver = df_raw.drop_duplicates(subset=["title"])
    silver_dir = pathlib.Path("data/silver")
    silver_dir.mkdir(parents=True, exist_ok=True)
    silver_path = silver_dir / "silver.parquet"
    df_silver.to_parquet(silver_path, index=False)
    print("✅ Silver data saved.")

    # ----------------- GOLD -----------------
    df_gold = df_silver[["title", "summary", "link", "published", "content"]]
    gold_dir = pathlib.Path("data/gold")
    gold_dir.mkdir(parents=True, exist_ok=True)
    gold_path = gold_dir / "gold.parquet"
    df_gold.to_parquet(gold_path, index=False)
    print("✅ Gold data saved.")

    # ----------------- Upload to MinIO -----------------
    bucket = os.getenv("MINIO_BUCKET", "data-lake")  # default = data-lake

    put_object(bucket, "bronze/bronze.parquet", str(bronze_path))
    put_object(bucket, "silver/silver.parquet", str(silver_path))
    put_object(bucket, "gold/gold.parquet", str(gold_path))

    print("🚀 All files uploaded to MinIO successfully.")

if __name__ == "__main__":
    run_etl()
