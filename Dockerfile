FROM python:3.11-slim

WORKDIR /app

# 系统依赖（OCR 可选）
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr tesseract-ocr-chi-sim \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV DOCINTEL_SERVER__HOST=0.0.0.0
ENV DOCINTEL_SERVER__PORT=8000

CMD ["python", "-m", "docintel.cli", "serve"]
