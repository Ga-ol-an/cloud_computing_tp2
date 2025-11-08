FROM python:3.12-slim-bookworm

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 50010

CMD ["flask", "run", "--host=0.0.0.0", "--port=50010"]