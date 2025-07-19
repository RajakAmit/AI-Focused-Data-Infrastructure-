make scrape      # Run web scraper
make etl         # Clean + store data
make embed       # Embed data with SentenceTransformers
make Dags       # Launch FastAPI server

scrape:
	python src/etl/scraper.py

etl:
	python src/etl/transform.py

embed:
	python src/embedding/embedder.py

serve:
	python main.py