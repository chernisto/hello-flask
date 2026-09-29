# ---- base: runtime dependencies only ----
FROM python:3.13-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- test: adds pytest and runs the suite; the build fails if tests fail ----
FROM base AS test
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY . .
RUN pytest -q

# ---- runtime: no test tools, non-root user ----
FROM base AS runtime
RUN useradd --create-home --uid 10001 appuser
COPY app/ ./app/
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2).status == 200 else 1)"
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app.app:app"]
