FROM python:3.9-slim

# Install Chrome dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    libglib2.0-0 \
    libfontconfig1 \
    libxcb1 \
    libxkbcommon0 \
    libxss1 \
    libxrandr2 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxfixes3 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libxshmfence1 \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# We'll use ChromeDriverManager in the application code instead of installing ChromeDriver here
# This ensures we get the correct version for the installed Chrome

# Create a non-root user to run the application
RUN groupadd -r appuser && useradd -r -g appuser -m -d /home/appuser appuser

# Set up working directory
WORKDIR /app

# Create and activate virtual environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary files to reduce image size
COPY app.py .
COPY chromedriver_installer.py .
COPY templates/ ./templates/
COPY requirements.txt .

# Create and set permissions for webdriver directory
RUN mkdir -p /tmp/webdriver \
    && chown -R appuser:appuser /tmp/webdriver \
    && chmod -R 755 /tmp/webdriver

# Set permissions for the application directory
RUN chown -R appuser:appuser /app

# Expose port
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CHROME_BIN=/usr/bin/google-chrome-stable
ENV PYTHONPATH=/app
ENV WEBDRIVER_MANAGER_PATH=/tmp/webdriver

# Switch to non-root user
USER appuser

# Pre-install ChromeDriver
RUN python chromedriver_installer.py

# Set memory limit for the container
ENV GUNICORN_CMD_ARGS="--limit-request-line 4094"

# Run the application with optimized settings
CMD ["/app/venv/bin/gunicorn", \
     "--bind", "0.0.0.0:8080", \
     "--log-level", "debug", \
     "--timeout", "120", \
     "--workers", "1", \
     "--threads", "2", \
     "app:app"]
