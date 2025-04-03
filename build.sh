#!/bin/bash
set -e

# Install Chrome and Python venv
apt-get update
apt-get install -y wget gnupg python3-venv
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
apt-get update
apt-get install -y google-chrome-stable

# We'll let the application handle ChromeDriver installation
# This ensures we get the correct version for the installed Chrome

# Print Chrome version for debugging
echo "Chrome version: $(google-chrome --version)"

# Create a non-root user if it doesn't exist
if ! id -u appuser &>/dev/null; then
    groupadd -r appuser
    useradd -r -g appuser -m -d /home/appuser appuser
fi

# Create and set up virtual environment
if [ ! -d "/app/venv" ]; then
    python3 -m venv /app/venv
    chown -R appuser:appuser /app/venv
fi

# Create webdriver directory with proper permissions
mkdir -p /tmp/webdriver
chown -R appuser:appuser /tmp/webdriver
chmod -R 755 /tmp/webdriver

# Set environment variables
export CHROME_BIN=/usr/bin/google-chrome-stable
export PYTHONUNBUFFERED=1
export WEBDRIVER_MANAGER_PATH=/tmp/webdriver
export PATH="/app/venv/bin:$PATH"

# Install dependencies in the virtual environment
su - appuser -c "cd /app && /app/venv/bin/pip install -r requirements.txt"

# Run the ChromeDriver installer as the non-root user
su - appuser -c "cd /app && /app/venv/bin/python chromedriver_installer.py"
