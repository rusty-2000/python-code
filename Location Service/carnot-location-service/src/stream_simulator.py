import time
import pandas as pd
from datetime import datetime
from config import RAW_CSV_PATH, SLEEP_ENABLED
from processor import LatestStore, append_audit_row

def main():
    df = pd.read_csv(RAW_CSV_PATH)

    cols = {c.lower(): c for c in df.columns}
    device_col = cols.get('device_fk') or cols.get('device_id') or list(df.columns)[0]
    lat_col = cols.get('latitude') or 'latitude'
    lon_col = cols.get('longitude') or 'longitude'
    ts_col = cols.get('time_stamp') or 'time_stamp'
    sts_col = cols.get('sts') or 'sts'
    speed_col = cols.get('speed') or 'speed'

    # Parsing datetimes
    df[ts_col] = pd.to_datetime(df[ts_col])
    df[sts_col] = pd.to_datetime(df[sts_col])
    df.sort_values(by=sts_col, inplace=True)

    store = LatestStore()
    start_sts = df[sts_col].min()
    wall_start = time.time()

    for _, row in df.iterrows():

        if SLEEP_ENABLED:
            wait = (row[sts_col] - start_sts).total_seconds() - (time.time() - wall_start)
            if wait > 0:
                time.sleep(wait)

        payload = {
            "latitude": float(row[lat_col]),
            "longitude": float(row[lon_col]),
            "time_stamp": row[ts_col],
            "sts": row[sts_col],
            "speed": int(row.get(speed_col, 0)),
        }
        user = str(row[device_col])
        updated = store.upsert_if_newer(user, payload)


        append_audit_row(row[sts_col].isoformat(), user, payload["latitude"], payload["longitude"], row[ts_col].isoformat(), payload["speed"])

        if updated:
            print(f"[UPD] user={user} event_ts={row[ts_col]} sts={row[sts_col]} -> latest updated")
        else:
            print(f"[SKIP] user={user} event_ts={row[ts_col]} older than stored latest")

if __name__ == "__main__":
    main()
