# # Simple dev-friendly image for the FastAPI service
# FROM python:3.11-slim

# RUN apt-get update \
#     && apt-get install -y --no-install-recommends ca-certificates \
#     && rm -rf /var/lib/apt/lists/*

# WORKDIR /app

# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1

# COPY requirements.txt ./
# RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
# COPY . .

# ENV PYTHONPATH="/app"
# EXPOSE 8000

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Simple dev-friendly image for the FastAPI service
FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

COPY netfree-ca-bundle-curl.crt /usr/local/share/ca-certificates/netfree-ca-bundle-curl.crt
RUN update-ca-certificates && \
    mkdir -p /ProgramData/NetFree/CA && \
    ln -sf /usr/local/share/ca-certificates/netfree-ca-bundle-curl.crt /ProgramData/NetFree/CA/netfree-ca-bundle-curl.crt

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Copy all application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]