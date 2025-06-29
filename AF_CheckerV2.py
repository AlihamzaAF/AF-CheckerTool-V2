#!/data/data/com.termux/files/usr/bin/python
# AF CHECKER V2 - Ultimate Proxy & Security Tool
import requests
import os
import time
import webbrowser
import socket
import json
import re
from urllib.parse import urlparse

# ANSI color codes
COLOR_RED = "\033[1;31m"
COLOR_GREEN = "\033[1;32m"
COLOR_YELLOW = "\033[1;33m"
COLOR_BLUE = "\033[1;34m"
COLOR_MAGENTA = "\033[1;35m"
COLOR_CYAN = "\033[1;36m"
COLOR_RESET = "\033[0m"

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def banner():
    clear_screen()
    print(f"""
{COLOR_GREEN}
 █████╗ ███████╗    ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗
██╔══██╗██╔════╝   ██╔════╝██║  ██║██╔════╝██╔════╝██║  ██║██╔════╝██╔══██╗
███████║█████╗     ██║     ███████║█████╗  ██║     ███████║█████╗  ██████╔╝
██╔══██║██╔══╝     ██║     ██╔══██║██╔══╝  ██║     ██╔══██║██╔══╝  ██╔══██╗
██║  ██║██║         ╚██████╗██║  ██║███████╗╚██████╗██║  ██║███████╗██║  ██║
╚═╝  ╚═╝╚═╝         ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

{COLOR_CYAN}🔥 AF CHECKER V2 - Ultimate Proxy & Security Tool
💻 Developer: Ali Hamza AF
📱 Termux Optimized | ❤️ AF Cyber Force
{COLOR_RESET}
""")

def fetch_proxies():
    print(f"\n{COLOR_BLUE}[+] Select Proxy Type:{COLOR_RESET}")
    print("1. HTTP/HTTPS (General Purpose)")
    print("2. SOCKS5 (Telegram, Browsing)")
    print("3. WhatsApp Specific")
    print("4. Twitter Specific")
    print("5. Instagram Specific")
    print("6. All Types")
    
    choice = input(f"\n{COLOR_CYAN}[>] Select proxy type (1-6): {COLOR_RESET}").strip()
    
    proxy_types = {
        "1": "http",
        "2": "socks5",
        "3": "whatsapp",
        "4": "twitter",
        "5": "instagram",
        "6": "all"
    }
    proxy_type = proxy_types.get(choice, "http")
    
    print(f"\n{COLOR_BLUE}[+] Select Country:{COLOR_RESET}")
    print("1. United States (US)")
    print("2. United Kingdom (UK)")
    print("3. Pakistan (PK)")
    print("4. India (IN)")
    print("5. Germany (DE)")
    print("6. Saudi Arabia (SA)")
    print("7. All Countries")
    
    country_choice = input(f"\n{COLOR_CYAN}[>] Select country (1-7): {COLOR_RESET}").strip()
    
    countries = {
        "1": "US",
        "2": "GB",
        "3": "PK",
        "4": "IN",
        "5": "DE",
        "6": "SA",
        "7": "all"
    }
    country = countries.get(country_choice, "all")
    
    print(f"\n{COLOR_YELLOW}[*] Generating {proxy_type.upper()} proxies for {country}...{COLOR_RESET}")
    
    try:
        # Different sources for different proxy types
        sources = {
            "http": "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&timeout=10000&country={country}&proxy_format=ipport&format=text",
            "socks5": "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=socks5&timeout=10000&country={country}&proxy_format=ipport&format=text",
            "whatsapp": "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
            "twitter": "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/twitter.txt",
            "instagram": "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/instagram.txt",
            "all": "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt"
        }
        
        url = sources.get(proxy_type, sources['http']).format(country=country)
        res = requests.get(url, timeout=30)
        proxies = [p.strip() for p in res.text.splitlines() if p.strip()]
        
        # If no proxies found, use backup source
        if not proxies:
            print(f"{COLOR_YELLOW}[!] Primary source failed, trying backup...{COLOR_RESET}")
            url = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
            res = requests.get(url, timeout=30)
            proxies = [p.strip() for p in res.text.splitlines() if p.strip()]
        
        # Filter by country if not "all"
        if country != "all" and proxy_type not in ["whatsapp", "twitter", "instagram"]:
            filtered_proxies = []
            for proxy in proxies:
                if len(proxy.split(':')) == 2 and proxy.split(':')[1].isdigit():
                    filtered_proxies.append(proxy)
            proxies = filtered_proxies
        
        # Save to file
        with open("proxies.txt", "w") as f:
            f.write("\n".join(proxies))
        
        print(f"{COLOR_GREEN}[✓] {len(proxies)} {proxy_type.upper()} proxies saved to proxies.txt{COLOR_RESET}")
        
        # Test first 3 proxies
        if proxies:
            print(f"{COLOR_YELLOW}[*] Testing first 3 proxies...{COLOR_RESET}")
            for i, proxy in enumerate(proxies[:3]):
                print(f"\n{COLOR_CYAN}[{i+1}] Testing: {proxy}{COLOR_RESET}")
                test_proxy(proxy)
        
    except Exception as e:
        print(f"{COLOR_RED}[!] Error: {str(e)}{COLOR_RESET}")
        print(f"{COLOR_YELLOW}[!] Tip: Try using mobile data if Wi-Fi blocks requests{COLOR_RESET}")

def test_proxy(proxy):
    proxy_dict = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    
    try:
        start = time.time()
        res = requests.get("https://ipinfo.io/json", proxies=proxy_dict, timeout=15)
        duration = time.time() - start
        data = res.json()
        
        print(f"{COLOR_GREEN}[✓] WORKING | IP: {data.get('ip')} | Time: {duration:.2f}s{COLOR_RESET}")
        print(f"Location: {data.get('city', 'N/A')}, {data.get('country', 'N/A')}")
        print(f"ISP: {data.get('org', 'N/A')}")
        return True
        
    except Exception as e:
        print(f"{COLOR_RED}[!] FAILED: {str(e)}{COLOR_RESET}")
        return False

def check_my_ip():
    try:
        print(f"{COLOR_YELLOW}[*] Checking your real IP and location...{COLOR_RESET}")
        res = requests.get("https://ipinfo.io/json", timeout=10)
        data = res.json()
        
        print(f"\n{COLOR_GREEN}[✓] Your Real IP: {data.get('ip', 'N/A')}{COLOR_RESET}")
        print(f"Location: {data.get('city', 'N/A')}, {data.get('region', 'N/A')}, {data.get('country', 'N/A')}")
        print(f"ISP: {data.get('org', 'N/A')}")
        
        if data.get('loc'):
            print(f"Map: {COLOR_BLUE}https://www.google.com/maps/place/{data.get('loc')}{COLOR_RESET}")
        
        # Get device hostname
        try:
            hostname = socket.gethostname()
            print(f"Device Hostname: {hostname}")
        except:
            pass
            
        print()
        return True
        
    except Exception as e:
        print(f"{COLOR_RED}[!] Error: {str(e)}{COLOR_RESET}")
        try:
            print(f"{COLOR_YELLOW}[*] Trying alternative method...{COLOR_RESET}")
            ip = requests.get("https://api.ipify.org", timeout=5).text
            print(f"\n{COLOR_GREEN}[✓] Your Real IP: {ip}{COLOR_RESET}\n")
            return True
        except:
            print(f"{COLOR_RED}[!] Failed to get IP address{COLOR_RESET}\n")
            return False

def scan_link():
    url = input(f"\n{COLOR_CYAN}[🔗] Enter URL to scan: {COLOR_RESET}").strip()
    if not url:
        print(f"{COLOR_RED}[!] Empty URL{COLOR_RESET}\n")
        return
        
    try:
        if not url.startswith(('http://', 'https://')):
            url = "http://" + url
            
        print(f"{COLOR_YELLOW}[*] Scanning: {url}{COLOR_RESET}")
        start = time.time()
        res = requests.get(url, timeout=15, allow_redirects=True)
        duration = time.time() - start
        
        # Security assessment
        security_status = f"{COLOR_GREEN}✅ SAFE{COLOR_RESET}"
        threats = []
        
        # Check for suspicious content
        content = res.text.lower()
        suspicious_patterns = [
            r"phish", r"malware", r"trojan", r"virus", r"spyware",
            r"hack", r"exploit", r"keylogger", r"ransomware"
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, content):
                threats.append(f"Suspicious content found: {pattern.upper()}")
        
        # Check for URL shorteners
        shorteners = ["bit.ly", "goo.gl", "tinyurl", "ow.ly", "is.gd", "buff.ly"]
        if any(short in url for short in shorteners):
            threats.append("URL shortener detected (could be suspicious)")
        
        # Check redirects
        if len(res.history) > 2:
            threats.append(f"Multiple redirects detected ({len(res.history)})")
        
        # Check if known malicious site
        with open("malicious_domains.txt", "a+") as f:
            f.seek(0)
            malicious_domains = [line.strip() for line in f if line.strip()]
            
        domain = urlparse(url).netloc
        if domain in malicious_domains:
            threats.append(f"Known malicious domain: {domain}")
        
        # Final security rating
        if threats:
            security_status = f"{COLOR_RED}❌ DANGEROUS{COLOR_RESET}"
        elif res.status_code != 200:
            security_status = f"{COLOR_YELLOW}⚠️ SUSPICIOUS{COLOR_RESET}"
        
        # Print results
        print(f"\n{COLOR_GREEN}[✓] Status: {res.status_code} | Security: {security_status}{COLOR_RESET}")
        print(f"Scan Time: {duration:.2f}s")
        print(f"Final URL: {res.url}")
        print(f"Server: {res.headers.get('Server', 'N/A')}")
        print(f"Content Size: {len(res.content)/1024:.2f} KB")
        
        if threats:
            print(f"\n{COLOR_RED}[!] SECURITY THREATS DETECTED:{COLOR_RESET}")
            for threat in threats:
                print(f"- {threat}")
        else:
            print(f"\n{COLOR_GREEN}[✓] No security threats detected{COLOR_RESET}")
        
        print()
        return True
        
    except Exception as e:
        print(f"{COLOR_RED}[!] Scan Failed: {str(e)}{COLOR_RESET}\n")
        return False

def termux_open(url):
    try:
        os.system(f"termux-open-url '{url}' >/dev/null 2>&1")
        print(f"{COLOR_BLUE}[*] Opening in your browser...{COLOR_RESET}")
        return True
    except:
        try:
            webbrowser.open(url)
            return True
        except:
            print(f"{COLOR_RED}[!] Failed to open URL{COLOR_RESET}")
            return False

def show_menu():
    print(f"""
{COLOR_MAGENTA}
[1] 🔁 Generate Proxies (Select Type/Country)
[2] 🌐 Check My Real IP & Location
[3] 🛡️  Test Proxy from File
[4] 🔍 Scan Link for Security Threats
[5] 📺 YouTube Channel
[6] 💬 WhatsApp Channel
[7] 📷 Instagram
[8] 📱 Telegram
[9] 🚪 Exit Tool
{COLOR_RESET}""")

def main():
    banner()
    
    # Create malicious domains list if not exists
    if not os.path.exists("malicious_domains.txt"):
        with open("malicious_domains.txt", "w") as f:
            f.write("malicious.com\nexample.bad\nphishing.org")
    
    # Check internet
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
    except OSError:
        print(f"{COLOR_RED}[!] WARNING: No internet connection!{COLOR_RESET}")
    
    while True:
        try:
            show_menu()
            choice = input(f"\n{COLOR_CYAN}[📥] Select Option: {COLOR_RESET}").strip()
            
            if choice == "1":
                fetch_proxies()
            elif choice == "2":
                check_my_ip()
            elif choice == "3":
                if not os.path.exists("proxies.txt"):
                    print(f"{COLOR_RED}[!] No proxies.txt found. Generate proxies first.{COLOR_RESET}")
                    continue
                    
                with open("proxies.txt") as f:
                    proxies = [line.strip() for line in f if line.strip()]
                
                if not proxies:
                    print(f"{COLOR_RED}[!] No proxies in file.{COLOR_RESET}")
                    continue
                    
                print(f"\n{COLOR_BLUE}[+] Select proxy to test:{COLOR_RESET}")
                for i, proxy in enumerate(proxies[:15]):
                    print(f"{i+1}. {proxy}")
                    
                try:
                    selection = input(f"\n{COLOR_CYAN}[>] Enter number (1-{min(15, len(proxies))}) or 'r' for random: {COLOR_RESET}").strip()
                    
                    if selection.lower() == 'r':
                        import random
                        proxy = random.choice(proxies)
                    else:
                        selection = int(selection)
                        if 1 <= selection <= min(15, len(proxies)):
                            proxy = proxies[selection-1]
                        else:
                            print(f"{COLOR_RED}[!] Invalid selection{COLOR_RESET}")
                            continue
                    
                    test_proxy(proxy)
                except Exception as e:
                    print(f"{COLOR_RED}[!] Error: {str(e)}{COLOR_RESET}")
                    
            elif choice == "4":
                scan_link()
            elif choice == "5":
                termux_open("https://youtube.com/@AliHamzaAF")
            elif choice == "6":
                termux_open("https://whatsapp.com/channel/0029VaU5UfBBVJl2sqYwbJ1t")
            elif choice == "7":
                termux_open("https://instagram.com/alihamzaaf")
            elif choice == "8":
                termux_open("https://t.me/alihamzaaf")
            elif choice == "9":
                print(f"\n{COLOR_GREEN}[✓] Thank you for using AF Checker V2!{COLOR_RESET}")
                break
            else:
                print(f"{COLOR_RED}[!] Invalid option. Try again.{COLOR_RESET}")
                
            time.sleep(1)
            
        except KeyboardInterrupt:
            print(f"\n{COLOR_RED}[!] Operation cancelled. Press 9 to exit.{COLOR_RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()
