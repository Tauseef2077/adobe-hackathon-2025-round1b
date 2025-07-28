FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && python -m nltk.downloader punkt punkt_tab averaged_perceptron_tagger

COPY app/ app/
COPY input/ input/
COPY output/ output/

CMD ["python", "app/extractor.py"]
