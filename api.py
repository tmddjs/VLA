"""FastAPI application exposing the plant layout generator."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from plant_layout import run_layout


class LayoutRequest(BaseModel):
    """Request model for the ``/run-layout`` endpoint."""

    width: float
    height: float
    plants: List[Dict[str, Any]]
    return_image: bool = True


class LayoutResponse(BaseModel):
    placements: List[Dict[str, Any]]
    image_png: Optional[str] = None


app = FastAPI(title="Plant Layout API")


@app.post("/run-layout", response_model=LayoutResponse)
def run_layout_endpoint(req: LayoutRequest) -> LayoutResponse:
    """Generate a plant layout for the given parameters.

    On success the placement list and a base64 encoded PNG image are returned.
    Any error during processing results in a 400 response with the error
    message.
    """

    try:
        placements, image_b64 = run_layout(
            req.width, req.height, req.plants, return_image=req.return_image
        )
    except Exception as exc:  # pragma: no cover - defensive error handling
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return LayoutResponse(placements=placements, image_png=image_b64)


__all__ = ["app"]

