# Telecom Analytics Pipeline

An end-to-end ETL pipeline for telecom customer analytics built with Kestra workflow orchestration. Automates data ingestion, processing, analysis, and visualization — running on scheduled intervals with zero manual intervention.

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| **Kestra** | Workflow orchestration & scheduling |
| **Python** | Data processing, analytics, charting |
| **PostgreSQL** | Data storage & warehousing |
| **Docker** | Containerized deployment |
| **Pandas** | Data transformation |
| **Matplotlib** | Chart generation |

## Architecture

1. **Ingest Customers** — Fetches 50 customer profiles from RandomUser API
2. **Generate CDRs** — Creates 150-300 realistic call detail records per run
3. **Run Analytics** — Computes daily revenue, call volumes, top customers
4. **Generate Charts** — Produces 4 business-ready visualizations

## Generated Charts

- **revenue_trend.png** — Daily revenue over last 30 days
- **call_type_analysis.png** — Volume & revenue by call type (Local/STD/ISD)
- **top_customers.png** — Top 10 revenue-generating customers
- **hourly_volume.png** — Call distribution by hour of day

## Quick Start

```bash
docker compose up -d
```

Open http://localhost:8080 → Execute `telecom_pipeline` flow

## Schedule

Runs automatically at **6:00 AM** and **6:00 PM** daily.

## What I Learned

- Workflow orchestration with Kestra DAG-based pipelines
- ETL pipeline design (Extract → Transform → Load)
- Python automation for data processing
- PostgreSQL for structured data warehousing
- Docker containerization for reproducible deployments
