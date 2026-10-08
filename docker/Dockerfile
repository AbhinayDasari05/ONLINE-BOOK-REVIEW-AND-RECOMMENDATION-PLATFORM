# Stage 1: Build & Security Verification
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Minimal Hardened Runtime
FROM python:3.11-slim AS runtime

# Security: Install curl for healthcheck and create dedicated non-root user
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --home-dir /home/appuser --shell /bin/bash --uid 10001 appuser

WORKDIR /home/appuser/app

# Copy dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH

# Copy application source code
COPY --chown=appuser:appuser . /home/appuser/app

# Ensure instance directory is owned by appuser for SQLite write operations
RUN mkdir -p /home/appuser/app/instance \
    && chown -R appuser:appuser /home/appuser/app

# Switch to non-root execution
USER 10001:10001

# Expose internal port
EXPOSE 5000

# Container health probe
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Environment flags for secure production runtime
ENV FLASK_APP=wsgi.py
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["python", "wsgi.py"]
