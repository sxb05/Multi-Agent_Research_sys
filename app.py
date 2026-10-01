import logging
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.pipelines.pipeline import research_pipeline

logger = logging.getLogger("research-lab")


class ResearchRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=500)
    num_results: int = Field(default=5, ge=1, le=10)


app = FastAPI(
    title="Research Lab API",
    docs_url=None,
    redoc_url=None,
)
frontend_dist = Path(__file__).parent / "frontend" / "dist"


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/research")
def research(request: ResearchRequest) -> dict[str, Any]:
    topic = request.topic.strip()
    if not topic:
        raise HTTPException(status_code=422, detail="A research topic is required.")

    try:
        return research_pipeline(topic=topic, num_results=request.num_results)
    except Exception as error:
        logger.exception("Research pipeline failed for topic length %d", len(topic))
        raise HTTPException(
            status_code=502,
            detail="The research pipeline is temporarily unavailable. Please try again.",
        ) from error


if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=frontend_dist / "assets"), name="assets")

    @app.get("/{path:path}", include_in_schema=False)
    def frontend(path: str) -> FileResponse:
        requested = frontend_dist / path
        if path and requested.is_file():
            return FileResponse(requested)
        return FileResponse(frontend_dist / "index.html")
