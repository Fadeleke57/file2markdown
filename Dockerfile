FROM python:3.9.6

WORKDIR /app

# --- native deps ----------------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libfontconfig1 \
        libfreetype6 \
        libx11-6 libxext6 libxrender1 \
        fonts-dejavu-core && \
    rm -rf /var/lib/apt/lists/*
# --------------------------------------------------------------------------

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
