import requests
import webbrowser
import os
import time
import threading
import nmap
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
clear_screen() 
def ico():
    x = """
  _      __    __     __           
 | | /| / /__ / /    / /  ___ __ __
 | |/ |/ / -_) _ \  / _ \/ _ \\ \ /
 |__/|__/\__/_.__/ /_.__/\___/_\_\ 
                        Created By: Crashi_z
 [01] Certificate Search        [05] Nmap custom
 [02] Website Discovery         [06] Nikto Web Server Scan (Only Linux)
 [03] Website Scan              [07] WPScan for WordPress (Only Linux)
 [04] PC Scan                   [08] Google Dorking

 [99] Exit                          
"""
    print(x)
def ico2():
    x = """
  _      __    __     __           
 | | /| / /__ / /    / /  ___ __ __
 | |/ |/ / -_) _ \  / _ \/ _ \\ \ /
 |__/|__/\__/_.__/ /_.__/\___/_\_\ 
                        Created By: Crashi_z

                       
"""
    print(x)
def install_chek():
    if os.name == 'nt':
        pass
    else:
        print("[+] Installing...")
        os.system("sudo apt-get install nikto")
        os.system("sudo apt-get install wpscan")
        os.system("sudo apt-get install nmap") 
        clear_screen()   
install_chek()   
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
        with open("common.txt", "r", encoding="utf-8") as file:
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
def A3():
    url = input("Enter IP address or domain: ")
    try:
        nm = nmap.PortScanner()
        nm.scan(url, '1-65535', '-Pn -A -v -T4 -sV -sS -sC -O --script=http-title,http-headers,vuln')
        if nm.all_hosts():
            for host in nm.all_hosts():
                print(f'Host: {host} ({nm[host].hostname()})')
                print(f'State: {nm[host].state()}')
                for proto in nm[host].all_protocols():
                    print('----------')
                    print(f'Protocol: {proto}')
                    
                    lport = nm[host][proto].keys()
                    for port in lport:
                        print(f'port: {port}\tstate: {nm[host][proto][port]["state"]}')
                        print(f'service: {nm[host][proto][port]["name"]}')
                        if 'script' in nm[host][proto][port]:
                            print(f'script: {nm[host][proto][port]["script"]}')
        else:
            print(f"No hosts found for {url}")

    except nmap.PortScannerError as e:
        print(f"[-] {url} [Error: {e}]")
        time.sleep(4)
        A3()
    except Exception as e:
        print(f"An error occurred: {e}")
    
    input("Press Enter to continue...")

def A4():
    url = input("Enter IP address: ")
    try:
        nm = nmap.PortScanner()
        nm.scan(url, '1-65535', '-Pn -A -v -T4 -sV -sS -sC -O --script=default,vuln')
        if nm.all_hosts():
            for host in nm.all_hosts():
                print(f'Host: {host} ({nm[host].hostname()})')
                print(f'State: {nm[host].state()}')
                for proto in nm[host].all_protocols():
                    print('----------')
                    print(f'Protocol: {proto}')
                    
                    lport = nm[host][proto].keys()
                    for port in lport:
                        print(f'port: {port}\tstate: {nm[host][proto][port]["state"]}')
                        print(f'service: {nm[host][proto][port]["name"]}')
                        if 'script' in nm[host][proto][port]:
                            print(f'script: {nm[host][proto][port]["script"]}')
        else:
            print(f"No hosts found for {url}")

    except nmap.PortScannerError as e:
        print(f"[-] {url} [Error: {e}]")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    input("Press Enter to continue...")
def A5():
    url = input("Enter IP address or domain: ")
    port = input("Enter ports (default: 1-65535): ")
    command = input("Nmap command: ")
    
    if port == "":
        port = "1-65535" 
    
    try:
        nm = nmap.PortScanner()
        nm.scan(url, port, arguments=command)
        
        if nm.all_hosts():
            for host in nm.all_hosts():
                print(f'Host: {host} ({nm[host].hostname()})')
                print(f'State: {nm[host].state()}')
                
                for proto in nm[host].all_protocols():
                    print('----------')
                    print(f'Protocol: {proto}')
                    
                    lport = nm[host][proto].keys()
                    sorted_ports = sorted(lport, key=lambda x: int(x))
                    
                    for port in sorted_ports:
                        port_info = nm[host][proto][port]
                        service_name = name_service(port_info)
                        print(f'port: {port}\tstate: {port_info["state"]}\t{service_name}')
                        
                        if 'product' in port_info or 'version' in port_info:
                            print(f'\tProduct: {port_info["product"]}')
                            print(f'\tVersion: {port_info["version"]}')
                        
                        if 'extrainfo' in port_info:
                            print(f'\tAdditional Info: {port_info["extrainfo"]}')
                        
                        if 'script' in port_info:
                            for script in port_info['script']:
                                print(f'\t{script}: {port_info["script"][script]}')
        
        else:
            print(f"No hosts found for {url}")

    except nmap.PortScannerError as e:
        print(f"[-] {url} [Error: {e}]")
    
    except Exception as e:
        print(f"An error occurred: {e}")

    input("Press Enter to continue...")

def name_service(port_info):
    if 'name' in port_info:
        return f'service: {port_info["name"]}'
    elif port_info["state"] == "filtered":
        return f'state: filtered service: {port_info["reason"]}'
    else:
        return f'service: unknown'
def A6():
    if os.name == 'nt':
        print("No no.....")   
    else:
        clear_screen()
        ico2()
        print(" [01] NormalScan")
        print(" [02] HTTPSScan ")
        print(" [03] PortScan  ")
        print(" [04] Tuning    ")
        x = input(f"{os.getlogin()}~# ")
        if x == 1:
            url = input("Enter website url: ")
            os.system(f"nikto -h {url}")
        elif x == 2:
            url = input("Enter website url: ")
            port = input("Enter port: ")
            os.system(f"nikto -h {url} -ssl")
        elif x == 3:
            url = input("Enter website url: ")
            port = input("Enter port: ")
            os.system(f"nikto -h {url} -p {port}")
        elif x == 4:
            url = input("Enter website url: ")
            os.system(f"nikto -h {url} -Tuning 1234567890")
        else:
            print("Invalid option")
    input("Press Enter to continue...")
def A7():
    if os.name == 'nt':
        print("No no.....")
    input("Press Enter to continue...")
def A8():
    url = input("Enter URL (e.g., www.kkando.hu): ")
    if url.startswith('www.'):
        new_str = url[3:]
    else:
        new_str = url
        url = 'www.'+url
    webbrowser.open(f"https://www.google.com/search?q=-site:{url} site:*{new_str}")
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
                A3()
                clear_screen() 
                main_run()
            elif ch == 4:
                A4()
                clear_screen() 
                main_run()
            elif ch == 5:
                A5()
                clear_screen() 
                main_run()
            elif ch == 6:
                A6()
                clear_screen() 
                main_run()
            elif ch == 7:
                A7()
                clear_screen() 
                main_run()
            elif ch == 8:
                A8()
                clear_screen() 
                main_run()
            elif ch == 99:
                print("bye.....")
                time.sleep(2)
                os._exit
            else:
                print("Invalid choice, exiting...")
        except ValueError as Error:
            print(f"Error: {Error}")
    main_run()
