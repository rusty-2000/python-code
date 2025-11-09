# Carnot Location Tracking Service (SDE-2 Assignment)

implementation to maintain **latest location per user** with <2s update time.

## Highlights
- Stream simulation honors **arrival time** `sts`; state is based on **event time** `time_stamp` (handles late arrivals).
- **Redis** as latest-state store (falls back to in-memory if Redis not available).
- Append-only **audit log** at `data/output.csv`.
- (Q1–Q6 + Bonus)** in `docs/design.md`.
- **Docker Compose** to spin up Redis quickly. .

## Run (local)
```bash
python -m venv venv && source venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export RAW_CSV_PATH=./data/raw_data.csv             # place provided CSV here
python src/stream_simulator.py
# Query:
python src/query_service.py --user 25029 --time "2021-10-22 10:10:10"
```

## Run with Docker (Redis)
```bash
docker compose -f docker/docker-compose.yml up -d
```

## Folder Layout
```
carnot-location-service/
├── README.md
├── requirements.txt
├── data/                # raw_data.csv (you add) + output.csv (generated)
├── src/                 # core logic
├── docs/                # design answers
└── docker/              # Docker + Compose for Redis
```
