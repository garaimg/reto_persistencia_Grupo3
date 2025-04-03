FROM python:3.8

WORKDIR /app

COPY insert_data.py /app/
COPY dataset/T1.csv /app/dataset/

RUN pip install influxdb-client pandas

CMD ["python", "-u", "/app/insert_data.py"]

