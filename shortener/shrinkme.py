from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent
import requests
import time
import random
from wit import Wit
import uuid
import os

def main(pluginfile, proxy_plugin, headless, num1, num2, bnum1, bnum2, r_links, ouo_links,wit_key):
    def get_random_link():
        return random.choice(ouo_links)

    def random_redirects():
        return random.choice(r_links)

    def random_sleep(first_num, last_num):
        return random.randint(first_num, last_num)

    def bef_quit(first_num, last_num):
        return random.randint(first_num, last_num)

    options = webdriver.ChromeOptions()
    options.add_extension(pluginfile)
    ua = UserAgent()
    user_agent = ua.random
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
    options.add_experimental_option('excludeSwitches', ['enable-logging', "enable-automation"])
    # options.add_experimental_option("detach", True)
    options.add_extension(proxy_plugin)
    prefs = {
        "download_restrictions": 3,
    }
    options.add_experimental_option(
        "prefs", prefs
    )
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.enable", {})
    driver.execute_cdp_cmd("Network.enable", {})
    blocked_urls = [
        "https://cdn.jsdelivr.net/npm/disable-devtool"
    ]

    driver.execute_cdp_cmd(
        "Network.setBlockedURLs", {"urls": blocked_urls})
    driver.maximize_window()
    driver.execute_cdp_cmd("Page.removeScriptToEvaluateOnNewDocument",
                           {"identifier": "1"})  # NOTE: Bypassed all detection using this cdp command
    driver.get(random_redirects())
    time.sleep(5)
    driver.get(get_random_link())
    time.sleep(5)
    time.sleep(random_sleep(num1, num2))
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, ".g-recaptcha > div:nth-child(1) > div:nth-child(1) > iframe:nth-child(1)")))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span#recaptcha-anchor"))).click()
    driver.switch_to.default_content()
    time.sleep(random_sleep(7,9))
    try:
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "/html/body/div[3]/div[4]/iframe")))
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[2]/button"))).click()
    except:
        pass
    
    while True:
        # Use try to check if the element exists or not
        try:
            # Get audio's link
            try:
                t = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'rc-audiochallenge-tdownload')))
                t = t.find_element(By.TAG_NAME, 'a')
                t = t.get_attribute('href')
            except:
                t = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, 'audio-source'))
                )
                t = t.get_attribute('src')
            unique_id = str(uuid.uuid4())
            audio = f'audio_{unique_id}.mp3'

            # Download audio file
            r = requests.get(t, allow_redirects=True)
            open(audio, 'wb').write(r.content)

            def transcribe_audio_to_text(audio_file_path, wit_token):
                client = Wit(access_token=wit_token)

                with open(audio_file_path, 'rb') as audio_file:
                    response = client.speech(audio_file, {'Content-Type': 'audio/mpeg'})

                return response.get('text', '')

            transcription = transcribe_audio_to_text(audio, wit_key)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'audio-response'))).send_keys(
                transcription)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'verify-button-holder'))).click()
            os.remove(audio)
        except Exception as e:
            # If the app doesn't find the element, it means we are done!
            break

    driver.switch_to.default_content()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'invisibleCaptchaShortlink'))
    ).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn2"]'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tp-snp2"]'))).click()
    time.sleep(15)
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.btn-success.btn-lg.get-link'))
    )
    driver.execute_script("arguments[0].click();", button)

    time.sleep(bef_quit(bnum1, bnum2))
    time.sleep(3)
    driver.quit()