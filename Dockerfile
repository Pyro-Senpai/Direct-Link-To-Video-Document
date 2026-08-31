# ============================================================
# Telegram Direct Link Bot
# Dockerfile
# ============================================================

FROM python:3.12-slim

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Make Python output appear immediately
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app


# ============================================================
# System Dependencies
# ============================================================

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*


# ============================================================
# Python Dependencies
# ============================================================

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# ============================================================
# Copy Project
# ============================================================

COPY . .


# ============================================================
# Create Download Directory
# ============================================================

RUN mkdir -p /app/downloads


# ============================================================
# Start Bot
# ============================================================

CMD ["python", "bot.py"]
