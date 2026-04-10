const charts = {};
let currentTableData = [];

const uploadForm = document.getElementById("uploadForm");
const fileInput = document.getElementById("fileInput");
const statusMessage = document.getElementById("statusMessage");
const warningList = document.getElementById("warningList");
const searchInput = document.getElementById("searchInput");
const filterSelect = document.getElementById("filterSelect");

uploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  warningList.innerHTML = "";
  const file = fileInput.files[0];
  if (!file) {
    setStatus("Please choose a CSV or Excel file.", true);
    return;
  }

  setStatus("Processing file...", false);

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("/upload", { method: "POST", body: formData });
    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail || "Failed to process file.");
    }

    renderKpis(payload.kpis);
    renderCharts(payload.charts);
    renderInsights(payload.insights);
    currentTableData = payload.table_data || [];
    renderTable(currentTableData);
    renderWarnings(payload.warnings || []);
    setStatus("Analysis complete.", false);
  } catch (error) {
    setStatus(error.message || "Unexpected error.", true);
  }
});

searchInput.addEventListener("input", () => renderTable(currentTableData));
filterSelect.addEventListener("change", () => renderTable(currentTableData));

function setStatus(message, isError) {
  statusMessage.textContent = message;
  statusMessage.style.color = isError ? "#ef4444" : "#8b949e";
}

function renderWarnings(warnings) {
  warningList.innerHTML = "";
  warnings.forEach((warning) => {
    const li = document.createElement("li");
    li.textContent = warning;
    warningList.appendChild(li);
  });
}

function renderKpis(kpis) {
  document.getElementById("kpiTotal").textContent = kpis.total_tickets ?? "-";
  document.getElementById("kpiSla").textContent = `${kpis.sla_compliance_pct ?? 0}%`;
  document.getElementById("kpiResolution").textContent = `${kpis.avg_resolution_mins ?? 0} mins`;
}

function upsertChart(key, config) {
  if (charts[key]) charts[key].destroy();
  charts[key] = new Chart(document.getElementById(key), config);
}

function renderCharts(data) {
  upsertChart("slaComplianceChart", {
    type: "doughnut",
    data: { labels: data.sla_compliance.labels, datasets: [{ data: data.sla_compliance.values, backgroundColor: ["#22c55e", "#ef4444"] }] },
  });

  upsertChart("slaPriorityChart", {
    type: "bar",
    data: { labels: data.sla_by_priority.labels, datasets: [{ label: "SLA %", data: data.sla_by_priority.values, backgroundColor: "#3b82f6" }] },
    options: { scales: { y: { beginAtZero: true, max: 100 } } }
  });

  upsertChart("agentPerformanceChart", {
    type: "bar",
    data: { labels: data.agent_performance.labels, datasets: [{ label: "Breach %", data: data.agent_performance.breach_pct, backgroundColor: "#ef4444" }] },
    options: { indexAxis: "y", scales: { x: { beginAtZero: true, max: 100 } } }
  });

  upsertChart("categoryParetoChart", {
    data: {
      labels: data.category_pareto.labels,
      datasets: [
        { type: "bar", label: "Breaches", data: data.category_pareto.breach_counts, backgroundColor: "#f59e0b", yAxisID: "y" },
        { type: "line", label: "Cumulative %", data: data.category_pareto.cumulative_pct, borderColor: "#22c55e", yAxisID: "y1" }
      ]
    },
    options: { scales: { y: { beginAtZero: true }, y1: { beginAtZero: true, max: 100, position: "right", grid: { drawOnChartArea: false } } } }
  });

  upsertChart("timeTrendChart", {
    type: "line",
    data: { labels: data.time_trend.labels, datasets: [{ label: "SLA %", data: data.time_trend.sla_pct, borderColor: "#22c55e" }] },
    options: { scales: { y: { beginAtZero: true, max: 100 } } }
  });

  upsertChart("channelPerformanceChart", {
    type: "bar",
    data: { labels: data.channel_performance.labels, datasets: [{ label: "SLA %", data: data.channel_performance.sla_pct, backgroundColor: "#8b5cf6" }] },
    options: { scales: { y: { beginAtZero: true, max: 100 } } }
  });
}

function renderInsights(insights) {
  const target = document.getElementById("insightsContent");
  const problems = (insights.key_problems || []).map((x) => `<li>${x}</li>`).join("");
  const recs = (insights.recommendations || []).map((x) => `<li>${x}</li>`).join("");

  target.innerHTML = `
    <p><strong>Executive Summary:</strong> ${insights.executive_summary || "N/A"}</p>
    <p><strong>Key Problems</strong></p>
    <ul>${problems}</ul>
    <p><strong>Actionable Recommendations</strong></p>
    <ul>${recs}</ul>
  `;
}

function renderTable(rows) {
  const query = (searchInput.value || "").toLowerCase();
  const filter = filterSelect.value;
  const tbody = document.querySelector("#ticketTable tbody");
  tbody.innerHTML = "";

  rows
    .filter((row) => {
      const isBreached = row.overall_breach;
      const filterMatch = filter === "all" || (filter === "breached" && isBreached) || (filter === "compliant" && !isBreached);
      const text = Object.values(row).join(" ").toLowerCase();
      return filterMatch && text.includes(query);
    })
    .forEach((row) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${row.ticket_id}</td>
        <td>${row.agent_name}</td>
        <td>${row.priority}</td>
        <td>${row.category}</td>
        <td>${row.channel}</td>
        <td>${row.status}</td>
        <td>${row.first_response_time}</td>
        <td>${row.resolution_time}</td>
        <td class="${row.overall_breach ? "status-breach" : "status-ok"}">${row.overall_breach ? "Breached" : "Compliant"}</td>
      `;
      tbody.appendChild(tr);
    });
}
