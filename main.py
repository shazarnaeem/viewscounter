print("Script started...", flush=True)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
import time
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import random

print("Chrome options set...", flush=True)
# YouTube video URL
url = "https://youtu.be/PwhkuMWqYN0"

def get_free_proxies():
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    proxies = []
    for row in soup.find("table", id="proxylisttable").tbody.find_all("tr"):
        tds = row.find_all("td")
        ip = tds[0].text.strip()
        port = tds[1].text.strip()
        https = tds[6].text.strip()
        if https == "yes":  # Only use HTTPS proxies
            proxies.append(f"{ip}:{port}")
    return proxies

# Paths to WebDrivers (update these paths as needed for your environment)
driver_paths = {
    "chrome": "/usr/local/bin/chromedriver",
    "firefox": "/usr/local/bin/geckodriver",
    "edge": "/usr/local/bin/msedgedriver"
}

browsers = ["chrome", "firefox", "edge"]

# 6 ghante ka duration
end_time = datetime.now() + timedelta(hours=6)
proxies = get_free_proxies()
proxy_index = 0

while datetime.now() < end_time:
    if proxy_index >= len(proxies):
        print("Refreshing proxy list...", flush=True)
        proxies = get_free_proxies()
        proxy_index = 0
    current_proxy = proxies[proxy_index]
    print(f"Using proxy: {current_proxy}", flush=True)
    ip, port = current_proxy.split(":")
    browser_choice = random.choice(browsers)
    print(f"Using browser: {browser_choice}", flush=True)
    driver = None
    try:
        if browser_choice == "chrome":
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument(f'--proxy-server={current_proxy}')
            service = ChromeService(driver_paths["chrome"])
            driver = webdriver.Chrome(service=service, options=chrome_options)
        elif browser_choice == "firefox":
            firefox_options = FirefoxOptions()
            firefox_options.add_argument("--headless")
            firefox_profile = webdriver.FirefoxProfile()
            firefox_profile.set_preference("network.proxy.type", 1)
            firefox_profile.set_preference("network.proxy.http", ip)
            firefox_profile.set_preference("network.proxy.http_port", int(port))
            firefox_profile.set_preference("network.proxy.ssl", ip)
            firefox_profile.set_preference("network.proxy.ssl_port", int(port))
            firefox_profile.update_preferences()
            service = FirefoxService(driver_paths["firefox"])
            driver = webdriver.Firefox(service=service, options=firefox_options, firefox_profile=firefox_profile)
        elif browser_choice == "edge":
            edge_options = EdgeOptions()
            edge_options.add_argument("--headless")
            edge_options.add_argument("--disable-gpu")
            edge_options.add_argument("--no-sandbox")
            edge_options.add_argument("--disable-dev-shm-usage")
            edge_options.add_argument(f'--proxy-server={current_proxy}')
            service = EdgeService(driver_paths["edge"])
            driver = webdriver.Edge(service=service, options=edge_options)
        else:
            print(f"Unknown browser: {browser_choice}", flush=True)
            continue
        print(f"Opening {url}", flush=True)
        driver.get(url)
        time.sleep(60)
        print("Reloading video", flush=True)
        driver.quit()
    except Exception as e:
        print(f"Proxy or browser failed: {current_proxy}, {browser_choice}, Error: {e}", flush=True)
        if driver:
            try:
                driver.quit()
            except:
                pass
    time.sleep(10)
    proxy_index += 1

print("6 ghante complete ho gaye. Script band ho gayi.", flush=True)