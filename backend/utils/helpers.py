from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pandas as pd
from fastapi import UploadFile

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}


def validate_file_extension(filename: str) -> str:
    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type. Upload CSV or Excel file.")
    return extension


async def read_uploaded_file(file: UploadFile) -> pd.DataFrame:
    extension = validate_file_extension(file.filename or "")
    raw = await file.read()
    if not raw:
        raise ValueError("Uploaded file is empty.")

    if extension == ".csv":
        return pd.read_csv(BytesIO(raw))
    return pd.read_excel(BytesIO(raw))


def safe_pct(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return round((numerator / denominator) * 100, 2)


def safe_mean(series: pd.Series) -> float:
    if series.empty:
        return 0.0
    value = series.dropna().mean()
    if pd.isna(value):
        return 0.0
    return round(float(value), 2)
