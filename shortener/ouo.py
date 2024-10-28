from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent

import multiprocessing
import zipfile
import time
import random

def main(pluginfile,proxy_plugin,headless,num1,num2,bnum1,bnum2,r_links,ouo_links):
    def get_random_link():
        return random.choice(ouo_links)

    def random_redirects():
        return random.choice(r_links)

    def random_sleep(first_num,last_num):
        return random.randint(first_num,last_num)

    def bef_quit(first_num,last_num):
        return random.randint(first_num,last_num)
        
    options = webdriver.ChromeOptions()
    options.add_extension(pluginfile)
    ua = UserAgent()
    user_agent = ua.random
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs",prefs)
    if headless:
        options.add_argument("--window-position=-10000,-10000")
        options.add_argument('--headless=new')
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--disable-crash-reporter")
    options.add_argument("--disable-oopr-debug-crash-dump")
    options.add_argument("--no-crash-upload")
    options.add_argument("--disable-low-res-tiling")
    options.add_argument("--silent")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("disable-blink-features")
    options.add_argument(
        "--disable-blink-features=AutomationControlled")
    options.add_experimental_option('excludeSwitches', ['enable-logging',"enable-automation"])
    # options.add_experimental_option("detach", True)
    options.add_extension(proxy_plugin)
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.enable", {})
    driver.execute_cdp_cmd("Network.enable", {})
    blocked_urls = [
        "https://cdn.jsdelivr.net/npm/disable-devtool"
    ]

    driver.execute_cdp_cmd(
        "Network.setBlockedURLs", {"urls": blocked_urls})
    driver.maximize_window()
    driver.execute_cdp_cmd("Page.removeScriptToEvaluateOnNewDocument", {"identifier":"1"})#NOTE: Bypassed all detection using this cdp command
    driver.get(random_redirects())
    time.sleep(.5)
    driver.get(get_random_link())
    time.sleep(random_sleep(num1,num2))
    try:
        WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID, 'btn-main'))).click()
    except:
        driver.quit()
        return
    time.sleep(.3)
    time.sleep(random_sleep(num1,num2))
    time.sleep(random_sleep(num1,num2))
    try:
        WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID, 'btn-main'))).click()
    except:
        driver.quit()
        return
    time.sleep(bef_quit(bnum1,bnum2))
    time.sleep(3)
    driver.quit()
