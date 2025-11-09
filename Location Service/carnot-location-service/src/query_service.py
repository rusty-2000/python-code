import argparse
import pandas as pd
from datetime import datetime
from config import OUTPUT_CSV_PATH

def get_latest(user_id: str, as_of: datetime):
    df = pd.read_csv(OUTPUT_CSV_PATH, parse_dates=["sts","time_stamp"]) if OUTPUT_CSV_PATH else None
    if df is None or df.empty:
        return None
    sdf = df[(df["device_fk"].astype(str) == str(user_id)) & (df["sts"] <= as_of)]
    if sdf.empty:
        return None
    # Latest by event time (time_stamp)
    rec = sdf.sort_values(by="time_stamp", ascending=False).iloc[0]
    return {
        "device_fk": str(rec["device_fk"]),
        "latitude": float(rec["latitude"]),
        "longitude": float(rec["longitude"]),
        "time_stamp": rec["time_stamp"].isoformat(),
        "as_of": as_of.isoformat()
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--user", required=True)
    p.add_argument("--time", required=True, help="YYYY-MM-DD HH:MM:SS")
    args = p.parse_args()
    as_of = pd.to_datetime(args.time)
    ans = get_latest(args.user, as_of)
    print(ans if ans else "{}")  # empty if not found

if __name__ == "__main__":
    main()
