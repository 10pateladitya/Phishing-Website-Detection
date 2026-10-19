from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from phishdetector.api.v1.endpoints import router as api_router


app = FastAPI(
    title="PhishDetector API",
    description="API for PhishDetector, a phishing websites detection system.",
    version="1.0.0",
    contact={"name": "Sujeet Gund", "url": "https://github.com/sujeetgund"},
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit/"},
)

@app.get("/", include_in_schema=False)
def root_page():
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["health"], summary="Check API health")
def get_health():
    """
    Check the health of the API.
    """
    return {"status": "healthy"}


app.include_router(api_router, prefix="/api/v1", tags=["v1"])
