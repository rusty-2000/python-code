
This project processes a large CSV file from a given URL, cleans and transforms the data in chunks, and stores the results into a SQLite database. It is optimized for performance and includes error handling and logging.

## Features
* Downloads compressed CSV file (.gz)
* Extracts and reads data in chunks
* Cleans and transforms data
* Stores results into an SQL database
* Handles errors and logs events to `processing.log`

## Tech Stack
* Python 3.8+
* Pandas
* SQLite (via SQLAlchemy)
* Logging

## Setup
### 1. Install Dependencies

pip freeze > requirements.txt



### 2. Run the Script

python process_csv.py


### 3. Database

* The database `processed_data.db` will be created after running in the project directory.
* Table name: `tyroo_data`

## Customize Schema

If the CSV columns are known, edit `schema.sql` and the `clean_transform_chunk` function in `process_csv.py` to reflect appropriate column names and transformations.

## Logs

* Logs are  written in `processing.log`.
