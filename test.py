# Linked In automation with chrome browser

# import psutil
# import subprocess
# import platform
# import os
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager 
# import time
# from selenium.webdriver.chrome.options import Options

# LINKEDIN_LOGIN_URL = "https://www.linkedin.com/login"

# chrome_options = webdriver.ChromeOptions()



# def get_chrome_paths():
#     os_name = platform.system()
#     if os_name == "Windows":
#         chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
#         if not os.path.exists(chrome_path):
#             chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
#         user = os.getlogin()
#         profile_path = rf"C:\Users\{user}\AppData\Local\Google\Chrome\User Data"
#     elif os_name == "Darwin":
#         chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
#         profile_path = f"/Users/{os.getlogin()}/Library/Application Support/Google/Chrome"
#     elif os_name == "Linux":
#         chrome_path = "/usr/bin/google-chrome"
#         profile_path = f"/home/{os.getlogin()}/.config/google-chrome"
#     else:
#         raise Exception(f"Unsupported OS: {os_name}")
#     if not os.path.exists(chrome_path):
#         raise FileNotFoundError(f"Chrome executable not found at {chrome_path}")
#     if not os.path.exists(profile_path):
#         raise FileNotFoundError(f"Chrome profile not found at {profile_path}")
#     return chrome_path, profile_path

# def find_chrome_debug_port():
#     for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
#         try:
#             if 'chrome' in proc.info['name'].lower():
#                 for arg in proc.info['cmdline']:
#                     if '--remote-debugging-port=' in arg:
#                         port = arg.split('=')[1]
#                         print(port)
#                         return port
#         except (psutil.NoSuchProcess, psutil.AccessDenied):
#             continue
#     return None

# def launch_chrome_with_debugging():
#     chrome_path, profile_path = get_chrome_paths()
#     port = "9223"
#     print("Launching Chrome with remote debugging...")
#     subprocess.Popen([
#         chrome_path,
#         f'--remote-debugging-port={port}',
#         f'--user-data-dir={profile_path}',
#         '--start-maximized',
#         LINKEDIN_LOGIN_URL
#     ])
#     time.sleep(10)
#     return port

# def attach_to_chrome(port):
    
#     chrome_options.debugger_address = f"127.0.0.1:{port}"
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#     for handle in driver.window_handles:
#         driver.switch_to.window(handle)
#         if "https://www.linkedin.com/login" in driver.current_url:
            
#             break
#     return driver

# def skip_login_if_not_present(driver, username, password):
#     try:
#         WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "username")))
#         print("Login page detected. Proceeding with login...")
#         driver.find_element(By.ID, 'username').clear()
#         driver.find_element(By.ID, 'username').send_keys(username)
#         driver.find_element(By.ID, 'password').clear()
#         driver.find_element(By.ID, 'password').send_keys(password)
#         driver.find_element(By.XPATH, "//button[@type='submit']").click()
#         time.sleep(10)
#         print("Login successful!")
#     except Exception:
#         print("Login page not found. Skipping login...")

# def main():
#     try:
        
#         port = find_chrome_debug_port()
#         if not port:
#             port = launch_chrome_with_debugging()
        
#         driver = attach_to_chrome(port)
        
      

#         print("Proceeding with the rest of the automation script...")
        
#         return driver  

#     except Exception as e:
#         print(f"Error in test.py: {e}")
#         raise

# if __name__ == "_main_":
#     main()



# Linked In automation with chrome webdriver

import psutil
import subprocess
import platform
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager 
import time
from selenium.webdriver.chrome.options import Options

LINKEDIN_LOGIN_URL = "https://www.linkedin.com/login"

chrome_options = webdriver.ChromeOptions()

def find_chrome_debug_port():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'chrome' in proc.info['name'].lower():
                for arg in proc.info['cmdline']:
                    if '--remote-debugging-port=' in arg:
                        port = arg.split('=')[1]
                        print(port)
                        return port
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None
def get_chrome_paths():
    os_name = platform.system()

    if os_name == "Windows":
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        if not os.path.exists(chrome_path):
            chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        user = os.getlogin()
        profile_path = rf"C:\Users\{user}\AppData\Local\Google\Chrome\User Data"
        user_data_dir = r'C:\chrome_dev_session'

    elif os_name == "Darwin":
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        user = os.getlogin()
        profile_path = f"/Users/{user}/Library/Application Support/Google/Chrome"
        user_data_dir = f"/Users/{user}/chrome_dev_session"

    elif os_name == "Linux":
        chrome_path = "/usr/bin/google-chrome"
        user = os.getlogin()
        profile_path = f"/home/{user}/.config/google-chrome"
        user_data_dir = f"/home/{user}/chrome_dev_session"

    else:
        raise Exception(f"Unsupported OS: {os_name}")


    if not os.path.exists(chrome_path):
        raise FileNotFoundError(f"Chrome executable not found at {chrome_path}")
    if not os.path.exists(profile_path):
        raise FileNotFoundError(f"Chrome profile not found at {profile_path}")

    return chrome_path, profile_path, user_data_dir


def launch_chrome_with_debugging():
    chrome_path, profile_path, user_data_dir = get_chrome_paths()
    port = "9223"
    print("Launching Chrome with remote debugging...")

    subprocess.Popen([
        chrome_path,
        f'--remote-debugging-port={port}',
        f'--user-data-dir={user_data_dir}',
        '--start-maximized',
        LINKEDIN_LOGIN_URL
    ])
    time.sleep(10)
    return port


def attach_to_chrome(port):
    
    chrome_options.debugger_address = f"127.0.0.1:{port}"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if "https://www.linkedin.com/login" in driver.current_url:
            
            break
    return driver

def skip_login_if_not_present(driver, username, password):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "username")))
        print("Login page detected. Proceeding with login...")
        driver.find_element(By.ID, 'username').clear()
        driver.find_element(By.ID, 'username').send_keys(username)
        driver.find_element(By.ID, 'password').clear()
        driver.find_element(By.ID, 'password').send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(10)
        print("Login successful!")
    except Exception:
        print("Login page not found. Skipping login...")

def main():
    try:
       
        
        port = find_chrome_debug_port()
        if not port:
            port = launch_chrome_with_debugging()
        
        driver = attach_to_chrome(port)
        

        print("Proceeding with the rest of the automation script...")
        
        return driver 

    except Exception as e:
        print(f"Error in test.py: {e}")
        raise

if __name__ == "__main__":
    main()

