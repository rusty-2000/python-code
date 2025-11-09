import os

RAW_CSV_PATH = os.environ.get("RAW_CSV_PATH", os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw_data.csv"))
OUTPUT_CSV_PATH = os.environ.get("OUTPUT_CSV_PATH", os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "output.csv"))

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
REDIS_DB = int(os.environ.get("REDIS_DB", "0"))

# SLEEP_ENABLED=0 during tests to replay instantly
SLEEP_ENABLED = os.environ.get("SLEEP_ENABLED", "1") == "1"
