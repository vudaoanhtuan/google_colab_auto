import argparse
import pickle
import time
import datetime
import threading
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

parser = argparse.ArgumentParser()
parser.add_argument('cookie_file')
parser.add_argument('notebook_url')
parser.add_argument('--driver', default='chromedriver')


def get_notebook_status(driver):
    status_cell = None
    try:
        status_cell = driver.find_element_by_css_selector("#connect > paper-button > iron-icon > svg > g > path")
    except Exception:
        pass
    if status_cell is None:
        return 'Disconnected'
    status_icon = status_cell.get_attribute('d')
    if status_icon.startswith('M9 16'):
        return 'Idle'
    elif status_icon.startswith("M6 10"):
        return 'Running'

def find_cell(driver, cell_desc):
    cell = driver.find_elements_by_class_name("cell")
    for c in cell:
        if c.text.find(cell_desc) > 0:
            return c
    return None

def stop_driver(driver):
    global running
    while True:
        inp = input()
        if inp=='q':
            running = False
            print("Stopping")
            break

running = True
if __name__=='__main__':
    args = parser.parse_args()

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=args.driver, options=options)

    print("Open colab.research.google.com")
    driver.get("https://colab.research.google.com")

    print("Load cookie")
    with open(args.cookie_file, 'rb') as f:
        cookies = pickle.load(f)

    for cookie in cookies:
        if isinstance(cookie.get('expiry'), float):
            cookie['expiry'] = int(cookie['expiry'])
        driver.add_cookie(cookie)

    print("Go to notebook")
    driver.get(args.notebook_url)

    time.sleep(1)
    selected_cell = None
    for _ in range(5):
        cell = driver.find_elements_by_class_name("cell")
        for c in cell:
            if c.text.find("__#CELL#__") > 0:
                selected_cell = c
                break
        if selected_cell is not None:
            break
        else:
            print("Try to find __#KEEP#__")
            time.sleep(5)

    if selected_cell is not None:
        print("Start running script")
        selected_cell.click()

        auto_run_js = """
        time_loop = 5 // minute

        var evt = new KeyboardEvent('keydown', {'keyCode':"13" ,'ctrlKey':true});

        function run_cell() {
            document.dispatchEvent(evt);
        }

        window.setInterval(run_cell, time_loop*1000*60);
        """
        driver.execute_script(auto_run_js);

    else:
        print("Missing __#KEEP#__ in running")

    print("Enter q to quit")
    start = time.time()
    thread = threading.Thread(target=stop_driver, args=(driver,))
    thread.start()
    while running:
        connect_status = get_notebook_status(driver)
        running_time = datetime.timedelta(seconds=time.time() - start)
        print(" "*100, end='\r', flush=True)
        print("Status: %s\t\tRunning time: %s "%(connect_status, running_time), end='', flush=True)
        time.sleep(60)
    
    driver.close()
    print("Notebook stopped")
