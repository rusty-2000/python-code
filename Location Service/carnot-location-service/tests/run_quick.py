import os, pandas as pd
from src.config import RAW_CSV_PATH
from src.stream_simulator import main as run

os.environ['SLEEP_ENABLED']='0'
os.environ['RAW_CSV_PATH']= 'tests/sample_test_data.csv'
run()
print('OK')
