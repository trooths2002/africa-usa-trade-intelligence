from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    """Simple health-check endpoint for Render"""
    return {"status": "ok"}
