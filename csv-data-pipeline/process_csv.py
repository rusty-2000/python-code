import os
import gzip
import shutil
import logging
import requests
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from io import BytesIO

# --- CONFIGURATION ---
CSV_URL = "https://tyroo-engineering-assesments.s3.us-west-2.amazonaws.com/Tyroo-dummy-data.csv.gz"
CHUNK_SIZE = 10000
DB_FILE = "processed_data.db"
TABLE_NAME = "tyroo_data"
LOG_FILE = "processing.log"

#  ---LOGGING ---
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')


def download_and_extract_csv(url: str, output_path: str):
    try:
        logging.info("Downloading CSV file...")
        response = requests.get(url)
        response.raise_for_status()
        with gzip.open(BytesIO(response.content), 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        logging.info("CSV downloaded and extracted successfully.")
    except Exception as e:
        logging.error(f"Error Occured while  downloading or extracting CSV: {e}")
        raise


def clean_transform_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
    chunk.dropna(how='all', inplace=True)  # Drop empty rows
    chunk.columns = [col.strip().lower().replace(' ', '_') for col in chunk.columns]
    return chunk


def process_and_store(csv_path: str, db_path: str, table: str):
    try:
        logging.info("Starting CSV processing...")
        engine = create_engine(f"sqlite:///{db_path}")
        chunk_iter = pd.read_csv(csv_path, chunksize=CHUNK_SIZE)
        for i, chunk in enumerate(chunk_iter):
            logging.info(f"Processing chunk {i}...")
            cleaned_chunk = clean_transform_chunk(chunk)
            cleaned_chunk.to_sql(table, con=engine, if_exists='append', index=False)
        logging.info("CSV processing completed successfully.")
    except Exception as e:
        logging.error(f"Error processing and storing data: {e}")
        raise


def main():
    csv_file_path = "data.csv"
    try:
        download_and_extract_csv(CSV_URL, csv_file_path)
        process_and_store(csv_file_path, DB_FILE, TABLE_NAME)
    except Exception as e:
        logging.error("Pipeline failed.", exc_info=True)
    finally:
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)


if __name__ == "__main__":
    main()
