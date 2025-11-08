FROM python:3.12-slim-bookworm

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY playlist_rules_generator.py /app/

CMD ["python", "playlist_rules_generator.py"]