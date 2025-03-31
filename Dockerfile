FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

ENV MDB_DATA_BASE_URL="http://mdb-data:8001" 

CMD ["python", "-m", "app.main"]
EXPOSE 8002