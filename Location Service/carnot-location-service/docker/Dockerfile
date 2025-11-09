FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY data ./data
ENV RAW_CSV_PATH=/app/data/raw_data.csv
CMD ["python", "src/stream_simulator.py"]
