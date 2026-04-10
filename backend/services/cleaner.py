from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

REQUIRED_COLUMNS = {
    "ticket_id",
    "agent_name",
    "created_at",
    "first_response_at",
    "resolved_at",
    "status",
    "priority",
    "category",
    "channel",
}

COLUMN_MAPPINGS = {
    "agent": "agent_name",
    "agentname": "agent_name",
    "created time": "created_at",
    "createdat": "created_at",
    "first response": "first_response_at",
    "resolved time": "resolved_at",
}

STATUS_MAPPINGS = {
    "closed": "Resolved",
    "done": "Resolved",
    "resolved": "Resolved",
    "open": "Open",
    "pending": "Open",
}


@dataclass
class CleaningResult:
    df: pd.DataFrame
    warnings: list[str]


def _normalize_name(column: str) -> str:
    normalized = (
        column.strip().lower().replace("-", " ").replace("_", " ").replace("  ", " ")
    )
    normalized = " ".join(normalized.split())
    mapped = COLUMN_MAPPINGS.get(normalized, normalized)
    return mapped.replace(" ", "_")


def clean_dataframe(raw_df: pd.DataFrame) -> CleaningResult:
    if raw_df.empty:
        raise ValueError("The uploaded file has no rows.")

    warnings: list[str] = []
    df = raw_df.copy()
    df.columns = [_normalize_name(col) for col in df.columns]

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    df = df[list(REQUIRED_COLUMNS)].copy()

    object_columns = df.select_dtypes(include="object").columns
    for col in object_columns:
        df[col] = df[col].astype(str).str.strip()

    for dt_col in ["created_at", "first_response_at", "resolved_at"]:
        df[dt_col] = pd.to_datetime(df[dt_col], errors="coerce", utc=True)

    invalid_created = df["created_at"].isna().sum()
    if invalid_created:
        warnings.append(f"Dropped {invalid_created} rows with invalid created_at.")
        df = df[df["created_at"].notna()].copy()

    for col in ["priority", "category", "channel", "agent_name"]:
        df[col] = df[col].replace({"": "Unknown"}).fillna("Unknown")

    df["status"] = (
        df["status"].str.lower().map(STATUS_MAPPINGS).fillna(df["status"].str.title())
    )

    missing_resolved = df["resolved_at"].isna().sum()
    missing_first = df["first_response_at"].isna().sum()
    if missing_resolved:
        warnings.append(f"{missing_resolved} tickets have missing resolved_at (treated as open).")
    if missing_first:
        warnings.append(
            f"{missing_first} tickets have missing first_response_at (potential first-response breaches)."
        )

    df["priority"] = df["priority"].str.title()
    df["category"] = df["category"].str.title()
    df["channel"] = df["channel"].str.title()

    return CleaningResult(df=df.reset_index(drop=True), warnings=warnings)
