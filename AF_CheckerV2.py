# AF CHECKER V2 - Enhanced Proxy Generator & IP Scanner
import requests, os, time, webbrowser, socket, json
from urllib.parse import urlparse

def banner():
    os.system('clear')
    print("""
\033[1;32m
 █████╗ ███████╗    ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗
██╔══██╗██╔════╝   ██╔════╝██║  ██║██╔════╝██╔════╝██║  ██║██╔════╝██╔══██╗
███████║█████╗     ██║     ███████║█████╗  ██║     ███████║█████╗  ██████╔╝
██╔══██║██╔══╝     ██║     ██╔══██║██╔══╝  ██║     ██╔══██║██╔══╝  ██╔══██╗
██║  ██║██║         ╚██████╗██║  ██║███████╗╚██████╗██║  ██║███████╗██║  ██║
╚═╝  ╚═╝╚═╝         ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

\033[1;37m🔥 AF CHECKER V2 - Enhanced Proxy Tools + IP Scanner
💻 Developer: Ali Hamza AF
📱 Termux Optimized | ❤️ AF Cyber Force
\033[0m
""")

def fetch_proxies():
    print("\n\033[1;34m[+] Select Proxy Type:\033[0m")
    print("1. HTTP/HTTPS (General Purpose)")
    print("2. SOCKS5 (Telegram, Browsing)")
    print("3. WhatsApp Specific")
    print("4. Twitter Specific")
    print("5. Custom (All Types)")
    
    choice = input("\n\033[1;36m[>] Select proxy type (1-5): \033[0m").strip()
    
    proxy_type = ""
    if choice == "1":
        proxy_type = "http"
    elif choice == "2":
        proxy_type = "socks5"
    elif choice == "3":
        proxy_type = "whatsapp"
    elif choice == "4":
        proxy_type = "twitter"
    elif choice == "5":
        proxy_type = "all"
    else:
        print("\033[1;31m[!] Invalid choice. Using default (HTTP)\033[0m")
        proxy_type = "http"
    
    print("\n\033[1;34m[+] Select Country:\033[0m")
    print("1. United States (US)")
    print("2. United Kingdom (UK)")
    print("3. Pakistan (PK)")
    print("4. India (IN)")
    print("5. Germany (DE)")
    print("6. All Countries")
    
    country_choice = input("\n\033[1;36m[>] Select country (1-6): \033[0m").strip()
    
    countries = {
        "1": "US",
        "2": "GB",
        "3": "PK",
        "4": "IN",
        "5": "DE",
        "6": "all"
    }
    country = countries.get(country_choice, "all")
    
    print(f"\n\033[1;33m[*] Generating {proxy_type.upper()} proxies for {country}...\033[0m")
    
    try:
        # Primary source
        if proxy_type in ["http", "socks5"]:
            url = f"https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol={proxy_type}&timeout=10000&country={country}&proxy_format=ipport&format=text"
        elif proxy_type == "whatsapp":
            url = "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data-with-geolocation.json"
        elif proxy_type == "twitter":
            url = "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/twitter.txt"
        else:  # all types
            url = "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt"
        
        res = requests.get(url, timeout=30)
        
        proxies = []
        if proxy_type == "whatsapp":
            data = res.json()
            proxies = [f"{item['ip']}:{item['port']}" for item in data]
        elif proxy_type == "twitter":
            proxies = [p.strip() for p in res.text.splitlines() if p.strip()]
        else:
            proxies = [p.strip() for p in res.text.splitlines() if p.strip()]
        
        # Secondary source if first fails
        if not proxies:
            print("\033[1;33m[!] Primary source failed, trying backup...\033[0m")
            backup_url = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
            res = requests.get(backup_url, timeout=30)
            proxies = [p.strip() for p in res.text.splitlines() if p.strip()]
        
        with open("proxies.txt", "w") as f:
            f.write("\n".join(proxies))
        
        print(f"\033[1;32m[✓] {len(proxies)} {proxy_type.upper()} proxies saved to proxies.txt\033[0m")
        
        # Test first proxy automatically
        if proxies:
            print("\033[1;33m[*] Testing first proxy...\033[0m")
            test_proxy(proxies[0])
        
    except Exception as e:
        print(f"\033[1;31m[!] Error: {e}\033[0m")
        print("\033[1;33m[!] Try using mobile data if Wi-Fi blocks the request\033[0m")

def test_proxy(proxy):
    print(f"\033[1;34m[*] Testing proxy: {proxy}\033[0m")
    proxy_dict = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    
    try:
        start = time.time()
        res = requests.get("https://ipinfo.io/json", proxies=proxy_dict, timeout=15)
        duration = time.time() - start
        data = res.json()
        
        print(f"\n\033[1;32m[✓] Proxy IP: {data.get('ip')} | Time: {duration:.2f}s\033[0m")
        print(f"Location: {data.get('city')}, {data.get('country')}")
        print(f"ISP: {data.get('org')}")
        print(f"Working Status: \033[1;32mACTIVE ✓\033[0m\n")
        return True
        
    except Exception as e:
        print(f"\033[1;31m[!] Proxy Failed: {e}\033[0m")
        print("\033[1;33m[*] Tip: This proxy might be inactive. Try another one\033[0m\n")
        return False

def check_my_ip():
    try:
        print("\033[1;34m[*] Checking your real IP and location...\033[0m")
        res = requests.get("https://ipinfo.io/json", timeout=10)
        data = res.json()
        
        print(f"\n\033[1;32m[✓] Your Real IP: {data.get('ip')}\033[0m")
        print(f"Location: {data.get('city')}, {data.get('region')}, {data.get('country')}")
        print(f"ISP: {data.get('org')}")
        print(f"Coordinates: {data.get('loc')}")
        print(f"Map: \033[4;34mhttps://www.google.com/maps/place/{data.get('loc')}\033[0m")
        
        # Additional device information
        try:
            hostname = socket.gethostname()
            print(f"Device Hostname: {hostname}")
        except:
            pass
            
        print()
        
    except Exception as e:
        print(f"\033[1;31m[!] Error: {e}\033[0m")
        print("\033[1;33m[*] Trying alternative method...\033[0m")
        try:
            ip = requests.get("https://api.ipify.org", timeout=5).text
            print(f"\n\033[1;32m[✓] Your Real IP: {ip}\033[0m\n")
        except:
            print("\033[1;31m[!] Failed to get IP address\033[0m\n")

def scan_link():
    url = input("\n\033[1;36m[🔗] Enter URL to scan: \033[0m").strip()
    if not url:
        print("\033[1;31m[!] Empty URL\033[0m\n")
        return
        
    try:
        if not url.startswith(('http://', 'https://')):
            url = "http://" + url
            
        print(f"\033[1;34m[*] Scanning: {url}\033[0m")
        start = time.time()
        res = requests.get(url, timeout=15, allow_redirects=True)
        duration = time.time() - start
        
        # Security assessment
        security_status = "\033[1;32m✅ SAFE\033[0m" 
        if res.status_code != 200:
            security_status = "\033[1;33m⚠️ SUSPICIOUS\033[0m"
        
        # Check for common threats
        threats = []
        content = res.text.lower()
        if "phishing" in content:
            threats.append("Phishing content detected")
        if "malware" in content:
            threats.append("Malware references found")
        if "bit.ly" in url or "tinyurl" in url:
            threats.append("URL shortener used (could be suspicious)")
        if len(res.history) > 2:
            threats.append(f"Multiple redirects ({len(res.history)}) detected")
        
        if threats:
            security_status = "\033[1;31m❌ DANGEROUS\033[0m"
        
        print(f"\n\033[1;32m[✓] Status: {res.status_code} | Security: {security_status}\033[0m")
        print(f"Scan Time: {duration:.2f}s")
        print(f"Final URL: {res.url}")
        print(f"Server: {res.headers.get('Server', 'Unknown')}")
        print(f"Size: {len(res.content)/1024:.2f} KB")
        
        if threats:
            print("\n\033[1;31m[!] SECURITY THREATS DETECTED:\033[0m")
            for threat in threats:
                print(f"- {threat}")
        
        print()
        
    except Exception as e:
        print(f"\033[1;31m[!] Scan Failed: {e}\033[0m\n")

def termux_open(url):
    try:
        os.system(f"termux-open-url '{url}' 2>/dev/null")
        print("\033[1;34m[*] Opening in your browser...\033[0m")
    except:
        webbrowser.open(url)

def show_menu():
    print("""
\033[1;35m[1] 🔁 Generate Proxies (Select Type/Country)
[2] 🌐 Check My Real IP & Location
[3] 🛡️  Test Proxy from File
[4] 🔍 Scan Link for Security Threats
[5] 📺 YouTube Channel
[6] 💬 WhatsApp Channel
[7] 🚪 Exit Tool
\033[0m""")

def main():
    banner()
    
    # Check internet
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
    except OSError:
        print("\033[1;31m[!] WARNING: No internet connection!\033[0m")
    
    while True:
        try:
            show_menu()
            choice = input("\n\033[1;36m[📥] Select Option: \033[0m").strip()
            
            if choice == "1":
                fetch_proxies()
            elif choice == "2":
                check_my_ip()
            elif choice == "3":
                if not os.path.exists("proxies.txt"):
                    print("\033[1;31m[!] No proxies.txt found. Generate proxies first.\033[0m")
                    continue
                    
                with open("proxies.txt") as f:
                    proxies = [line.strip() for line in f if line.strip()]
                
                if not proxies:
                    print("\033[1;31m[!] No proxies in file.\033[0m")
                    continue
                    
                print("\n\033[1;34m[+] Select proxy to test:\033[0m")
                for i, proxy in enumerate(proxies[:10]):
                    print(f"{i+1}. {proxy}")
                    
                try:
                    selection = int(input("\n\033[1;36m[>] Enter number (1-10): \033[0m").strip())
                    if 1 <= selection <= min(10, len(proxies)):
                        test_proxy(proxies[selection-1])
                    else:
                        print("\033[1;31m[!] Invalid selection\033[0m")
                except:
                    print("\033[1;31m[!] Invalid input\033[0m")
                    
            elif choice == "4":
                scan_link()
            elif choice == "5":
                termux_open("https://youtube.com/@AliHamzaAF")
            elif choice == "6":
                termux_open("https://whatsapp.com/channel/0029VaU5UfBBVJl2sqYwbJ1t")
            elif choice == "7":
                print("\n\033[1;32m[✓] Thank you for using AF Checker V2!\033[0m")
                break
            else:
                print("\033[1;31m[!] Invalid option. Try again.\033[0m")
                
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\n\033[1;31m[!] Operation cancelled. Press 7 to exit.\033[0m")
            time.sleep(1)

if __name__ == "__main__":
    main()
