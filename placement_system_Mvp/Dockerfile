FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# libpq-dev + gcc: needed to build psycopg2-binary's C extension on some platforms
# netcat-openbsd: used by entrypoint.sh to wait for Postgres to accept connections
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
        gcc \
        netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY placement_system_Mvp/ /app/

RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
