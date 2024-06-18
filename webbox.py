import requests
import webbrowser
import os
import time
import threading
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
clear_screen()    
def ico():
    x = """
  _      __    __     __           
 | | /| / /__ / /    / /  ___ __ __
 | |/ |/ / -_) _ \  / _ \/ _ \\ \ /
 |__/|__/\__/_.__/ /_.__/\___/_\_\ 

 [01] Certificate Search
 [02] Website Discovery
 [03] Exit                          
"""
    print(x)
def ico2():
    x = """
  _      __    __     __           
 | | /| / /__ / /    / /  ___ __ __
 | |/ |/ / -_) _ \  / _ \/ _ \\ \ /
 |__/|__/\__/_.__/ /_.__/\___/_\_\ 

                       
"""
    print(x)

def A1():
    url = input("Enter URL (e.g., www.kkando.hu): ")
    if url.startswith('www.'):
        new_str = url[4:]
    else:
        new_str = url
    webbrowser.open(f"https://crt.sh/?q={new_str}")

def check_directory(url, directory, succes_urls):
    full_url = f"{url}{directory}"
    try:
        response = requests.get(full_url)
        if response.status_code == 200:
            succes_urls.append(full_url)
            print(f"[+] {full_url} [200 OK]")
        else:
            print(f"[-] {full_url} [{response.status_code} {response.reason}]")
    except requests.exceptions.RequestException as e:
        print(f"[-] {full_url} [Error: {e}]")

def A2():
    succes_urls = []
    url = input("Enter URL (e.g., https://kkando.hu/): ")

    if url.startswith("https://") or url.startswith("http://"):
        with open("dircommon.txt", "r", encoding="utf-8") as file:
            threads = []
            for line in file:
                directory = line.strip()
                thread = threading.Thread(target=check_directory, args=(url, directory, succes_urls))
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()
    else:
        print("Invalid URL format. Please start with 'https://' or 'http://'.")
        return
    clear_screen() 
    print("\nResults:")
    for succ in succes_urls:
        print(f"[+] {succ} [200 OK]")
    print(f"[+] {len(succes_urls)} URLs found.")
    input("Press Enter to continue...")

if __name__ == "__main__":
    def main_run():
        ico()
        try:
            ch = int(input(f"{os.getlogin()}~# "))
            if ch == 1:
                A1()
                clear_screen() 
                main_run()
            elif ch == 2:
                A2()
                clear_screen() 
                main_run()
            elif ch == 3:
                print("bye.....")
                time.sleep(2)
                os._exit
            else:
                print("Invalid choice, exiting...")
        except ValueError as Error:
            print(f"Error: {Error}")
    main_run()
