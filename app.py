from shortener import ouo, shrinkme, version_check
import os
import zipfile
import multiprocessing
import threading
import time
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import glob
import concurrent.futures
import shutil
from shortener.__version__ import __version__
import tkinter as tk
from tkinter import messagebox

if __version__ != version_check.version_check():
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo("Update", "There is a new version of this software. Contact the developer for the software")

    root.destroy()

app = Flask(__name__)
app.secret_key = r'c6wPq^5eba6,ky8kY>G8Y\5kF£UR?b2T/-s"%58C176BpQ:.]Z'  # Change this to a random secret key
stop_flag = multiprocessing.Value('i', 0)


def cleanup():
    def delete_folder(folder):
        try:
            shutil.rmtree(folder)
        except Exception as e:
            ...

    username = os.getlogin()
    temp_dir = rf'C:\Users\{username}\AppData\Local\Temp\scoped_*'
    chrome_fetcher_dir = rf'C:\Users\{username}\AppData\Local\Temp\chrome_url_fetcher_*'
    chrome_unpacker_dir = rf'C:\Users\{username}\AppData\Local\Temp\chrome_Unpacker_*'

    # Use glob to find directories matching the patterns
    folders = glob.glob(temp_dir)
    chrome_folders = glob.glob(chrome_fetcher_dir)
    chrome_unpacker = glob.glob(chrome_unpacker_dir)

    # Combine the two lists of folders
    all_folders = folders + chrome_folders + chrome_unpacker

    # Use ThreadPoolExecutor with more workers to delete folders concurrently
    try:
        max_workers = min(32, len(all_folders))  # Adjust max_workers as needed
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(delete_folder, all_folders)
    except:
        ...

def read_links(file_path_1, file_path_2):
    def read_file(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]

    links_1 = read_file(file_path_1)
    links_2 = read_file(file_path_2)

    return links_1, links_2


@app.route('/')
def index():
    # Check if the user has already agreed to the disclaimer
    if 'disclaimer_agreed' not in session:
        return redirect(url_for('agreement'))
    return render_template('index.html')


@app.route('/agreement')
def agreement():
    return render_template('agreement.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/agree')
def agree():
    session['disclaimer_agreed'] = True
    return redirect(url_for('index'))


@app.route('/start', methods=['POST'])
def start():
    data = request.json
    threads = data.get('threads')
    headless = data.get('headless')
    sleep_before_quit = data.get('sleepBeforeQuit', '').strip().split(',')
    if len(sleep_before_quit) == 2:
        first_sleep_before_quit, last_sleep_before_quit = map(int, map(str.strip, sleep_before_quit))
    else:
        first_sleep_before_quit, last_sleep_before_quit = 3, 5  # Default values

    # Handling randomSleep
    random_sleep = data.get('randomSleep', '').strip().split(',')
    if len(random_sleep) == 2:
        first_random_sleep, last_random_sleep = map(int, map(str.strip, random_sleep))
    else:
        first_random_sleep, last_random_sleep = 6, 10  # Default values
    proxy_host = data.get('proxyHost')
    proxy_port = data.get('proxyPort')
    proxy_username = data.get('proxyUsername')
    proxy_password = data.get('proxyPassword')
    ouo_links = data.get('ouoLinks')
    r_links = data.get('randomLinks')
    clean = data.get('cleanUp')
    api = data.get('apiKey')
    ouo_check = data.get('ouo')
    shrinkme_check = data.get('shrinkme')
    if clean:
        cleanup()
    if ouo_links and r_links:
        r_links, ouo_links = read_links(r_links, ouo_links)
    proxy_config(proxy_host, proxy_password, proxy_port, proxy_username)
    if ouo_check:
        ouoWorkers(threads, headless, first_random_sleep, last_random_sleep, first_sleep_before_quit,
                   last_sleep_before_quit, r_links, ouo_links)
    elif shrinkme_check:
        shrinkmeWorkers(threads, headless, first_random_sleep, last_random_sleep, first_sleep_before_quit,
                        last_sleep_before_quit, r_links, ouo_links, api)

    # Return a valid JSON response
    return jsonify({"status": "success", "message": "Started with provided parameters."}), 200


@app.route('/stop', methods=['POST'])
def stop():
    stop_flag.value = 1  # Set the flag to stop the processes
    return "Stopping processes...", 200


def proxy_config(PROXY_HOST, PROXY_PASS, PROXY_PORT, PROXY_USER):
    file_path = os.path.join(os.getcwd(), "proxy_auth_plugin.zip")
    if not os.path.isfile(file_path):
        manifest_json = """
            {
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Chrome Proxy",
                "permissions": [
                    "proxy",
                    "tabs", 
                    "unlimitedStorage",
                    "storage",
                    "<all_urls>",
                    "webRequest",
                    "webRequestBlocking"
                ],
                "background": {
                    "scripts": ["background.js"]
                },
                "minimum_chrome_version":"22.0.0"
            }
            """

        background_js = """
            var config = {
                    mode: "fixed_servers",
                    rules: {
                    singleProxy: {
                        scheme: "http",
                        host: "%s",
                        port: parseInt(%s)
                    },
                    bypassList: ["localhost"]
                    }
                };

            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "%s",
                        password: "%s"
                    }
                };
            }

            chrome.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {urls: ["<all_urls>"]},
                        ['blocking']
            );
            """ % (
            PROXY_HOST,
            PROXY_PORT,
            PROXY_USER,
            PROXY_PASS,
        )
        pluginfile = os.path.join("extensions/", "proxy_auth_plugin.zip")

        with zipfile.ZipFile(pluginfile, "w") as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)


def run(thread, headless, num1, num2, bnum1, bnum2, r_links, ouo_links):
    while True:
        if stop_flag.value:  # Check if we should stop
            break

        processes = []
        for _ in range(int(thread)):
            process = multiprocessing.Process(target=ouo.main, args=(
            'extensions/chrome.crx', 'extensions/proxy_auth_plugin.zip', headless, num1, num2, bnum1, bnum2, r_links,
            ouo_links))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        time.sleep(1)


def run_shrinkme(thread, headless, num1, num2, bnum1, bnum2, r_links, ouo_links, wit):
    while True:
        if stop_flag.value:  # Check if we should stop
            break

        processes = []
        for _ in range(int(thread)):
            process = multiprocessing.Process(target=shrinkme.main, args=(
            'extensions/chrome.crx', 'extensions/proxy_auth_plugin.zip', headless, num1, num2, bnum1, bnum2, r_links,
            ouo_links, wit))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        time.sleep(1)


def ouoWorkers(thread, headless, num1, num2, bnum1, bnum2, r_links, ouo_links):
    run_thread = threading.Thread(target=run, args=(thread, headless, num1, num2, bnum1, bnum2, r_links, ouo_links))
    run_thread.daemon = True
    run_thread.start()


def shrinkmeWorkers(thread, headless, num1, num2, bnum1, bnum2, r_links, ouo_links, wit_api):
    run_thread = threading.Thread(target=run_shrinkme,
                                  args=(thread, headless, num1, num2, bnum1, bnum2, r_links, ouo_links, wit_api))
    run_thread.daemon = True
    run_thread.start()


if __name__ == '__main__':
    app.run(debug=True)

#TODO: binary file using nuitka, check_network,
