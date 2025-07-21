print("Script started...", flush=True)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime, timedelta

print("Chrome options set...", flush=True)
# YouTube video URL
url = "https://youtu.be/PwhkuMWqYN0"

# Headless Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ChromeDriver path for Railway Docker
driver_path = "/usr/local/bin/chromedriver"

print("Launching Chrome...", flush=True)
# Start Chrome once
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
print("Chrome launched!", flush=True)

# 6 ghante ka duration
end_time = datetime.now() + timedelta(hours=6)

while datetime.now() < end_time:
    print(f"Opening {url}", flush=True)
    driver.get(url)
    # Video ko 1 minute tak play hone dein
    time.sleep(60)
    print("Reloading video", flush=True)
    time.sleep(10)

driver.quit()
print("6 ghante complete ho gaye. Script band ho gayi.", flush=True)