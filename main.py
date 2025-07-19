# main.py

import uvicorn

if __name__ == "__main__":
    # This will run the FastAPI app from src/api/rag_api.py
    # Make sure your working directory is the root of the project
    uvicorn.run("src.api.rag_api:app", host="0.0.0.0", port=8000, reload=True)
