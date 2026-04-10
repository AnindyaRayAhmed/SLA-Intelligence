from __future__ import annotations

import pandas as pd

from backend.services.sla import PrioritySLA
from backend.utils.helpers import safe_mean, safe_pct


def compute_metrics(df: pd.DataFrame, sla_config: dict[str, PrioritySLA]) -> tuple[dict, dict, list[dict]]:
    working_df = df.copy()

    working_df["first_response_time"] = (
        (working_df["first_response_at"] - working_df["created_at"]).dt.total_seconds() / 60
    )
    working_df["resolution_time"] = (
        (working_df["resolved_at"] - working_df["created_at"]).dt.total_seconds() / 60
    )

    def first_response_limit(priority: str) -> int:
        return sla_config.get(priority, sla_config.get("Low")).first_response_mins

    def resolution_limit(priority: str) -> int:
        return sla_config.get(priority, sla_config.get("Low")).resolution_mins

    working_df["first_response_breach"] = (
        working_df["first_response_at"].isna()
        | (working_df["first_response_time"] > working_df["priority"].map(first_response_limit))
    )

    working_df["resolution_breach"] = (
        working_df["resolved_at"].isna()
        | (working_df["resolution_time"] > working_df["priority"].map(resolution_limit))
    )

    working_df["overall_breach"] = working_df["first_response_breach"] | working_df["resolution_breach"]
    working_df["sla_met"] = ~working_df["overall_breach"]

    total_tickets = len(working_df)
    sla_met_count = int(working_df["sla_met"].sum())
    breached_count = total_tickets - sla_met_count

    kpis = {
        "total_tickets": total_tickets,
        "sla_compliance_pct": safe_pct(sla_met_count, total_tickets),
        "avg_resolution_mins": safe_mean(working_df["resolution_time"]),
    }

    priority_group = (
        working_df.groupby("priority", dropna=False)["sla_met"]
        .mean()
        .mul(100)
        .round(2)
        .sort_index()
    )

    agent_group = (
        working_df.groupby("agent_name", dropna=False)
        .agg(
            tickets_handled=("ticket_id", "count"),
            avg_resolution_mins=("resolution_time", "mean"),
            breach_pct=("overall_breach", "mean"),
        )
        .reset_index()
    )
    agent_group["avg_resolution_mins"] = agent_group["avg_resolution_mins"].fillna(0).round(2)
    agent_group["breach_pct"] = (agent_group["breach_pct"] * 100).round(2)
    agent_group = agent_group.sort_values(["breach_pct", "tickets_handled"], ascending=[False, False])

    category_group = (
        working_df.groupby("category")["overall_breach"].sum().sort_values(ascending=False).astype(int)
    )
    cumulative = (category_group.cumsum() / category_group.sum() * 100).fillna(0).round(2)

    channel_group = (
        working_df.groupby("channel", dropna=False)
        .agg(sla_pct=("sla_met", "mean"), avg_resolution_mins=("resolution_time", "mean"))
        .reset_index()
    )
    channel_group["sla_pct"] = (channel_group["sla_pct"] * 100).round(2)
    channel_group["avg_resolution_mins"] = channel_group["avg_resolution_mins"].fillna(0).round(2)

    daily_df = working_df.copy()
    daily_df["created_date"] = daily_df["created_at"].dt.date.astype(str)
    daily_group = (
        daily_df.groupby("created_date", dropna=False)
        .agg(total_tickets=("ticket_id", "count"), sla_pct=("sla_met", "mean"))
        .reset_index()
        .sort_values("created_date")
    )
    daily_group["sla_pct"] = (daily_group["sla_pct"] * 100).round(2)

    charts = {
        "sla_compliance": {
            "labels": ["Compliant", "Breached"],
            "values": [sla_met_count, breached_count],
        },
        "sla_by_priority": {
            "labels": priority_group.index.tolist(),
            "values": priority_group.tolist(),
        },
        "agent_performance": {
            "labels": agent_group["agent_name"].tolist(),
            "breach_pct": agent_group["breach_pct"].tolist(),
            "avg_resolution_mins": agent_group["avg_resolution_mins"].tolist(),
            "tickets_handled": agent_group["tickets_handled"].tolist(),
        },
        "category_pareto": {
            "labels": category_group.index.tolist(),
            "breach_counts": category_group.tolist(),
            "cumulative_pct": cumulative.tolist(),
        },
        "time_trend": {
            "labels": daily_group["created_date"].tolist(),
            "sla_pct": daily_group["sla_pct"].tolist(),
            "total_tickets": daily_group["total_tickets"].tolist(),
        },
        "channel_performance": {
            "labels": channel_group["channel"].tolist(),
            "sla_pct": channel_group["sla_pct"].tolist(),
            "avg_resolution_mins": channel_group["avg_resolution_mins"].tolist(),
        },
    }

    table_columns = [
        "ticket_id",
        "agent_name",
        "priority",
        "category",
        "channel",
        "status",
        "first_response_time",
        "resolution_time",
        "first_response_breach",
        "resolution_breach",
        "overall_breach",
    ]
    table_df = working_df[table_columns].copy()
    table_df["first_response_time"] = table_df["first_response_time"].fillna(0).round(2)
    table_df["resolution_time"] = table_df["resolution_time"].fillna(0).round(2)
    table_data = table_df.to_dict(orient="records")

    return kpis, charts, table_data
