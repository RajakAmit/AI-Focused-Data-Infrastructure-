
# import json
# import os
# from datetime import datetime

# import feedparser
# import requests
# from bs4 import BeautifulSoup
# from dotenv import load_dotenv
# from minio import Minio

# # Load env
# load_dotenv()

# # Output folder
# RAW_DIR = os.path.join("data", "raw")
# os.makedirs(RAW_DIR, exist_ok=True)

# # RSS feed
# rss_url = os.getenv("RSS_URL", "http://feeds.bbci.co.uk/news/technology/rss.xml")
# feed = feedparser.parse(rss_url)

# def clean_html(html):
#     soup = BeautifulSoup(html, "html.parser")
#     return soup.get_text()

# # MinIO config
# MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
# MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
# MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
# MINIO_BUCKET = os.getenv("MINIO_BUCKET", "data-lake")

# client = Minio(
#     MINIO_ENDPOINT,
#     access_key=MINIO_ACCESS_KEY,
#     secret_key=MINIO_SECRET_KEY,
#     secure=False  # True if using HTTPS
# )

# # Ensure bucket exists
# if not client.bucket_exists(MINIO_BUCKET):
#     client.make_bucket(MINIO_BUCKET)

# # Scrape
# articles = []

# for i, entry in enumerate(feed.entries[:60]):
#     try:
#         response = requests.get(entry.link, timeout=10)
#         soup = BeautifulSoup(response.content, "html.parser")
#         article_body = soup.find("article")
#         text = clean_html(str(article_body)) if article_body else clean_html(response.text)

#         articles.append({
#             "title": entry.title,
#             "summary": entry.summary,
#             "link": entry.link,
#             "published": entry.published,
#             "content": text,
#         })

#         print(f"[{i+1}] Scraped: {entry.title}")
#     except Exception as e:
#         print(f"Error scraping {entry.link}: {e}")

# # Save locally
# timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# filename = f"bbc_tech_{timestamp}.json"
# filepath = os.path.join(RAW_DIR, filename)

# with open(filepath, "w", encoding="utf-8") as f:
#     json.dump(articles, f, indent=2, ensure_ascii=False)

# # Upload to MinIO
# minio_path = f"raw/{filename}"
# client.fput_object(
#     MINIO_BUCKET,
#     minio_path,
#     filepath,
#     content_type="application/json"
# )

# print(f"✅ Uploaded to MinIO: {MINIO_BUCKET}/{minio_path}")


# Add this at the bottom of scrape_bbc_tech.py

def run_scrape():
    import json
    import os
    from datetime import datetime

    import feedparser
    import requests
    from bs4 import BeautifulSoup
    from dotenv import load_dotenv
    from minio import Minio

    load_dotenv()

    RAW_DIR = os.path.join("data", "raw")
    os.makedirs(RAW_DIR, exist_ok=True)

    rss_url = os.getenv("RSS_URL", "http://feeds.bbci.co.uk/news/technology/rss.xml")
    feed = feedparser.parse(rss_url)

    def clean_html(html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text()

    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    MINIO_BUCKET = os.getenv("MINIO_BUCKET", "data-lake")

    client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )

    if not client.bucket_exists(MINIO_BUCKET):
        client.make_bucket(MINIO_BUCKET)

    articles = []

    for i, entry in enumerate(feed.entries[:60]):
        try:
            response = requests.get(entry.link, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            article_body = soup.find("article")
            text = clean_html(str(article_body)) if article_body else clean_html(response.text)

            articles.append({
                "title": entry.title,
                "summary": entry.summary,
                "link": entry.link,
                "published": entry.published,
                "content": text,
            })

            print(f"[{i+1}] Scraped: {entry.title}")
        except Exception as e:
            print(f"Error scraping {entry.link}: {e}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bbc_tech_{timestamp}.json"
    filepath = os.path.join(RAW_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

    minio_path = f"raw/{filename}"
    client.fput_object(
        MINIO_BUCKET,
        minio_path,
        filepath,
        content_type="application/json"
    )
    print(f"✅ Uploaded to MinIO: {MINIO_BUCKET}/{minio_path}")

if __name__ == "__main__":
    run_scrape()
