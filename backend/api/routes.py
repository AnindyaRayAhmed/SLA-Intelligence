from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.schemas.ticket_schema import UploadResponse
from backend.services.cleaner import clean_dataframe
from backend.services.insights import generate_insights
from backend.services.metrics import compute_metrics
from backend.services.sla import load_sla_config
from backend.utils.helpers import read_uploaded_file

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_tickets(file: UploadFile = File(...)) -> UploadResponse:
    try:
        raw_df = await read_uploaded_file(file)
        clean_result = clean_dataframe(raw_df)

        sla_config_path = Path(__file__).resolve().parents[1] / "config" / "sla.json"
        sla_config = load_sla_config(sla_config_path)

        kpis, charts, table_data = compute_metrics(clean_result.df, sla_config)
        insights = generate_insights(kpis, charts)

        return UploadResponse(
            kpis=kpis,
            charts=charts,
            insights=insights,
            table_data=table_data,
            warnings=clean_result.warnings,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected processing error: {exc}") from exc
