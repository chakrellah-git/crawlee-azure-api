import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from crawler import crawl_site   # <-- your existing crawling code

app = FastAPI()

# Load API key from environment variable only
API_KEY = os.getenv("CRAWLEE_API_KEY")
API_KEY_NAME = "x-api-key"

if not API_KEY:
    raise RuntimeError("Environment variable CRAWLEE_API_KEY is not set")


# ---- Authentication dependency ----
def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized – missing or invalid API key"
        )


# ---- Request model ----
class CrawlRequest(BaseModel):
    url: str


# ---- Protected endpoint ----
@app.post("/crawl")
def crawl_endpoint(request: CrawlRequest, _=Header(None, alias=API_KEY_NAME)):
    verify_api_key(_)

    results = crawl_site(request.url)
    return {
        "source": request.url,
        "documents": results
    }


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Crawlee API running"}
