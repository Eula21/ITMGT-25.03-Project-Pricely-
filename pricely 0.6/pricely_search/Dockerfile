FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    ca-certificates \
    libnss3 \
    libatk-bridge2.0-0 \
    libxss1 \
    libasound2 \
    libatk1.0-0 \
    libgtk-3-0 \
    libdrm2 \
    libxcomposite1 \
    libxrandr2 \
    libgbm1 \
    libxdamage1 \
    libx11-xcb1 \
    libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
## COPY requirements.txt .
# RUN pip install --upgrade pip
## RUN pip install --no-cache-dir -r requirements.txt -i https://mirror.sjtu.edu.cn/pypi/web/simple

COPY requirements.txt .

RUN pip --default-timeout=300 install --no-cache-dir -r requirements.txt -i https://pypi.org/simple
RUN pip install --no-cache-dir playwright
RUN playwright install --with-deps

# Install Playwright browsers
RUN playwright install --with-deps

# Copy project
COPY . .

CMD ["gunicorn", "pricely_search.wsgi:application", "--bind", "0.0.0.0:8000"]
