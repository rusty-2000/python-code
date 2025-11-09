from datetime import datetime
from typing import Dict, Any, Optional
import pandas as pd

try:
    import redis  # type: ignore
except Exception:
    redis = None

from config import REDIS_HOST, REDIS_PORT, REDIS_DB, OUTPUT_CSV_PATH

class LatestStore:
    """Latest-state storage. Uses Redis if available, else in-memory dict.
    Stores per user: {lat, lon, time_stamp, sts, speed}
    """
    def __init__(self):
        self._mem: Dict[str, Dict[str, Any]] = {}
        self._redis = None
        if redis is not None:
            try:
                self._redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
                self._redis.ping()
            except Exception:
                self._redis = None

    @staticmethod
    def _to_iso(dt):
        if isinstance(dt, pd.Timestamp):
            return dt.to_pydatetime().isoformat()
        if isinstance(dt, datetime):
            return dt.isoformat()
        return str(dt)

    def upsert_if_newer(self, user: str, payload: Dict[str, Any]) -> bool:
        """Update only if payload['time_stamp'] is newer than stored event time."""
        payload_norm = {k: (self._to_iso(v) if 'time' in k else v) for k, v in payload.items()}
        new_ts = pd.to_datetime(payload_norm["time_stamp"])

        if self._redis:
            key = f"user:{user}"
            existing_ts = self._redis.hget(key, "time_stamp")
            if existing_ts is None or new_ts > pd.to_datetime(existing_ts):
                self._redis.hset(key, mapping=payload_norm)
                return True
            return False
        else:
            rec = self._mem.get(user)
            if rec is None or new_ts > pd.to_datetime(rec["time_stamp"]):
                self._mem[user] = payload_norm
                return True
            return False

def append_audit_row(sts, device_fk, latitude, longitude, time_stamp, speed):
    import os, csv
    os.makedirs(os.path.dirname(OUTPUT_CSV_PATH), exist_ok=True)
    header = ["sts","device_fk","latitude","longitude","time_stamp","speed"]
    write_header = not os.path.exists(OUTPUT_CSV_PATH) or os.path.getsize(OUTPUT_CSV_PATH) == 0
    with open(OUTPUT_CSV_PATH, "a", newline="") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(header)
        w.writerow([sts, device_fk, latitude, longitude, time_stamp, speed])
