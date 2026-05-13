# ----------------------
# base image
# ----------------------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code


# ----------------------
# system dependencies
# ----------------------
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*


# ----------------------
# python dependencies (cache効率化)
# ----------------------
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# ----------------------
# app source
# ----------------------
COPY . .


# ----------------------
# non-root user
# ----------------------
RUN useradd -m appuser
USER appuser



#CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT"]