FROM python:3.12-slim-bookworm AS builder
WORKDIR /app
RUN apt-get -o Acquire::Check-Valid-Until=false update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim-bookworm
WORKDIR /app
RUN apt-get -o Acquire::Check-Valid-Until=false update && apt-get install -y libpq5 && rm -rf /var/lib/apt/lists/*
COPY --from=builder /install /usr/local
COPY . .
EXPOSE 8082
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8082", "--workers", "2"]