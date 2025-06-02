from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# Add this block right after creating the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"] for more strict security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REWRITE_URL = "http://rewrite:8000/rewrite"
SUMMARIZE_URL = "http://summarize:8000/summarize"

@app.post("/rewrite")
async def rewrite_proxy(request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(REWRITE_URL, json=payload)

    # Debug logging:
    print("Status:", response.status_code)
    print("Raw text:", response.text)

    try:
        return response.json()
    except Exception as e:
        return {
            "error": "Failed to parse JSON",
            "status_code": response.status_code,
            "raw_response": response.text,
            "details": str(e),
        }


@app.post("/summarize")
async def summarize_proxy(request: Request):
    payload = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(SUMMARIZE_URL, json=payload)
    return response.json()
