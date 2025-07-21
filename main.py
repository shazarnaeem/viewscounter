from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime, timedelta

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

# 6 ghante ka duration
end_time = datetime.now() + timedelta(hours=6)

while datetime.now() < end_time:
    print(f"Opening {url}")
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    # Video ko 1 minute tak play hone dein
    time.sleep(60)
    print("Closing browser")
    driver.quit()
    # 10 seconds ka break (optional)
    time.sleep(10)

print("6 ghante complete ho gaye. Script band ho gayi.") 