"""
Simple health check endpoint for the Africa-USA Trade Intelligence Platform
"""
from fastapi import FastAPI
import uvicorn
import os

app = FastAPI(title="Africa-USA Trade Intelligence Health Check", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Africa-USA Trade Intelligence API", "status": "running"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": __import__('time').time(),
        "service": "Africa-USA Trade Intelligence Platform"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)