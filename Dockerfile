# Use an official Python base image
FROM python:3.10-slim

# Install dependencies and browsers (without google-chrome-stable)
RUN apt-get update && \
    apt-get install -y wget gnupg2 curl unzip xvfb firefox-esr \
    && wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | apt-key add - \
    && echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge.list \
    && apt-get update && apt-get install -y microsoft-edge-stable

# Chrome for Testing - always compatible ChromeDriver (new URLs)
RUN wget -O /tmp/chrome-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/latest/linux64/chrome-linux64.zip && \
    wget -O /tmp/chromedriver-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/latest/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chrome-linux64.zip -d /tmp/ && \
    unzip /tmp/chromedriver-linux64.zip -d /tmp/ && \
    mv /tmp/chrome-linux64/chrome /usr/local/bin/google-chrome && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/google-chrome /usr/local/bin/chromedriver && \
    rm -rf /tmp/chrome-linux64* /tmp/chromedriver-linux64*

# GeckoDriver
RUN GECKODRIVER_VERSION=$(wget -qO- https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep 'tag_name' | cut -d" -f4) && \
    wget -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver

# EdgeDriver
RUN EDGEDRIVER_VERSION=$(wget -qO- https://msedgedriver.azureedge.net/LATEST_STABLE) && \
    wget -O /tmp/edgedriver.zip https://msedgedriver.azureedge.net/$EDGEDRIVER_VERSION/edgedriver_linux64.zip && \
    unzip /tmp/edgedriver.zip -d /tmp/ && \
    mv /tmp/msedgedriver /usr/local/bin/msedgedriver && \
    chmod +x /usr/local/bin/msedgedriver

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

CMD ["python", "main.py"] 