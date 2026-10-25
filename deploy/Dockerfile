# Multi-Stage Build for Optimized PrismVortex Container
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --no-cache-dir --prefix=/install .

FROM python:3.11-slim AS runner

WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /install /usr/local

COPY . .

# Non-root user for enhanced runtime security
RUN useradd -m prismuser && chown -R prismuser:prismuser /app
USER prismuser

EXPOSE 8080

CMD ["python", "main.py"]
