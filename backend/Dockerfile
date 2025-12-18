# ...existing code...
FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY netfree-ca-bundle-curl.crt /usr/local/share/ca-certificates/netfree-ca-bundle-curl.crt
RUN update-ca-certificates && \
    mkdir -p /ProgramData/NetFree/CA && \
    ln -sf /usr/local/share/ca-certificates/netfree-ca-bundle-curl.crt /ProgramData/NetFree/CA/netfree-ca-bundle-curl.crt

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Removed SSL_CERT_FILE / REQUESTS_CA_BUNDLE lines per your request

# Install Python dependencies (context is backend/)
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# ...existing code...