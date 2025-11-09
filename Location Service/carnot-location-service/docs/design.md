# Design Answers (Q1–Q6 + Bonus)

## 1) Reading CSV with `sts`-based availability
- Load rows, parse datetimes, **sort by `sts`**, and replay with a **relative wait** so that each row becomes available at its `sts` time.
- Implementation: `src/stream_simulator.py`

## 2) Storage choice for IoT streams
- **Redis (HASH per user)** for O(1) writes and <2s latency.
- Persistence via AOF or managed ElastiCache; batch export to data lake (S3/Parquet) for analytics.

## 3) Service logic
- On arrival, compare event time `time_stamp` with stored latest for that user; **update only if newer** (`LatestStore.upsert_if_newer`).
- Append arrival-ordered audit to `data/output.csv` for traceability.

## 4) Query function
- `get_latest(user, time)` filters audit up to `time` and returns the record with the **max `time_stamp`** for that user.
- Implementation: `src/query_service.py`

## 5) Average processing time
- Redis HSET ≈ 1–2 ms; Python overhead ≈ 3–5 ms → **~5–7 ms per event** typical on laptop hardware; comfortably < 2 seconds.

## 6) Bottlenecks & Scaling
| Risk | Impact              | Mitigation |
|------|---------------------|------------|
| Single Redis node | Memory & throughput | Redis **Cluster**, partition by user id |
| Single consumer | Backlog in spikes   | Kafka + **consumer group** (N consumers) |
| CSV audit growth | Slow queries        | Move audit to **Parquet on S3**, or TimescaleDB/ClickHouse for time-range queries |
| Network/serialization | CPU burn            | Use batched writes / Redis pipelining |
| Observability | Unknown lag         | Expose metrics (ingest lag, update latency), alarms on SLO breach |

## Bonus) ON/OFF trigger upload service
- **Trigger topic** (Kafka/MQTT) writes `ON/OFF` per user, mirror state in Redis (`user:<id>:status`).
- **Scheduler** (Celery beat / EventBridge) ticks every 2s, fetches active users from Redis, reads latest state, uploads batch to destination.
- Idempotent uploads keyed by `(user, window_start)`; backoff + retry.
