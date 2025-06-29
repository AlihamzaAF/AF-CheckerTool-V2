AF CHECKER V2 - Proxy Generator, IP Checker, Link Scanner

Developer: Ali Hamza AF | Powered by AF Cyber Force

import requests, os, time from urllib.parse import urlparse

def banner(): os.system("clear") print(""" \033[1;32m █████╗ ███████╗    ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ ██╔══██╗██╔════╝   ██╔════╝██║  ██║██╔════╝██╔════╝██║  ██║██╔════╝██╔══██╗ ███████║█████╗     ██║     ███████║█████╗  ██║     ███████║█████╗  ██████╔╝ ██╔══██║██╔══╝     ██║     ██╔══██║██╔══╝  ██║     ██╔══██║██╔══╝  ██╔══██╗ ██║  ██║██║         ╚██████╗██║  ██║███████╗╚██████╗██║  ██║███████╗██║  ██║ ╚═╝  ╚═╝╚═╝         ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ \033[1;37m 🔥 AF CHECKER V2 – Real Proxy Tool + IP + Scanner 💻 Developer: Ali Hamza AF ❤️ Powered by AF Cyber Force """)

def select_proxy_purpose(): print("\nSelect platform for proxy:") print("[1] Telegram") print("[2] WhatsApp") print("[3] Twitter") print("[4] Other") purpose = input("📌 Enter number: ").strip() return purpose

def select_proxy_country(): print("\nSelect country:") print("[1] Pakistan") print("[2] India") print("[3] US") print("[4] UK") print("[5] Any") country_map = {"1": "PK", "2": "IN", "3": "US", "4": "GB", "5": "all"} choice = input("🌍 Country number: ").strip() return country_map.get(choice, "all")

def fetch_proxies(): purpose = select_proxy_purpose() country = select_proxy_country() print("\n[*] Generating proxies based on your selection...") try: url = f"https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&timeout=5000&country={country}&proxy_format=ipport&format=text" res = requests.get(url, timeout=15) proxies = [p.strip() for p in res.text.splitlines() if p.strip()] if not proxies: print("[!] No proxies found for this combination. Try again.\n") return

with open("proxies.txt", "w") as f:
        f.write("\n".join(proxies))

    print(f"[✓] {len(proxies)} proxies saved to proxies.txt\n")
except Exception as e:
    print(f"[!] Error: {e}\n")

def check_my_ip(): try: res = requests.get("https://ipinfo.io/json", timeout=10) ip_data = res.json() print("\n[✓] Your IP Info:") print(f"IP: {ip_data.get('ip')}") print(f"City: {ip_data.get('city')}, Region: {ip_data.get('region')}, Country: {ip_data.get('country')}") print(f"ISP: {ip_data.get('org')}") print(f"Google Maps: https://www.google.com/maps/place/{ip_data.get('loc')}\n") except: print("[!] Failed to get IP info.\n")

def scan_link(): url = input("\n🔗 Enter URL to scan: ").strip() if not url.startswith("http"): url = "http://" + url try: print("[*] Scanning...") res = requests.get(url, timeout=10) if res.status_code == 200: print("[✓] Link is SAFE ✅\n") else: print("[!] Link returned unusual status ⚠️\n") except

