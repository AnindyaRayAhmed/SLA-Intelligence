from __future__ import annotations


def generate_insights(kpis: dict, charts: dict) -> dict:
    agent_labels = charts["agent_performance"].get("labels", [])
    agent_breach = charts["agent_performance"].get("breach_pct", [])
    category_labels = charts["category_pareto"].get("labels", [])
    category_breaches = charts["category_pareto"].get("breach_counts", [])
    channel_labels = charts["channel_performance"].get("labels", [])
    channel_sla = charts["channel_performance"].get("sla_pct", [])

    worst_agent = "N/A"
    if agent_labels:
        worst_agent = agent_labels[max(range(len(agent_labels)), key=lambda i: agent_breach[i])]

    top_category = "N/A"
    if category_labels:
        top_category = category_labels[max(range(len(category_labels)), key=lambda i: category_breaches[i])]

    slowest_channel = "N/A"
    if channel_labels:
        slowest_channel = channel_labels[min(range(len(channel_labels)), key=lambda i: channel_sla[i])]

    structured_summary = {
        "total_tickets": kpis.get("total_tickets", 0),
        "sla_compliance_pct": kpis.get("sla_compliance_pct", 0),
        "worst_agent": worst_agent,
        "top_breach_category": top_category,
        "slowest_channel": slowest_channel,
    }

    executive_summary = (
        f"Processed {structured_summary['total_tickets']} tickets with SLA compliance at "
        f"{structured_summary['sla_compliance_pct']}%. "
        f"Largest operational risk is concentrated around agent '{worst_agent}', "
        f"category '{top_category}', and channel '{slowest_channel}'."
    )

    key_problems = [
        f"SLA misses are most concentrated in category '{top_category}'.",
        f"Agent '{worst_agent}' has the highest breach rate and requires coaching or workload balancing.",
        f"Channel '{slowest_channel}' shows the lowest SLA adherence compared to other intake channels.",
    ]

    recommendations = [
        "Introduce priority-based auto-routing for High tickets during peak windows.",
        "Set a real-time alert when first-response SLA utilization exceeds 80% for any queue.",
        "Review staffing by channel and redistribute capacity to the slowest channel immediately.",
    ]

    return {
        "structured_summary": structured_summary,
        "executive_summary": executive_summary,
        "key_problems": key_problems,
        "recommendations": recommendations,
    }
