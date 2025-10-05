FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc libpq-dev
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
