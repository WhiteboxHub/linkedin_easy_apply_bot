import psutil
import time

def close_chrome_tabs():
    chrome_processes = []
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                chrome_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if not chrome_processes:
        print("No Chrome tabs are running.")
        return

    print(f"Found {len(chrome_processes)} Chrome processes. Terminating...")
    for proc in chrome_processes:
        try:
            proc.terminate()
        except Exception as e:
            print(f"Error terminating process {proc.pid}: {e}")

    psutil.wait_procs(chrome_processes)
    print("All Chrome tabs closed.")


