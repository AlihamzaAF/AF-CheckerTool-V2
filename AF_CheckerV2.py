# AF CHECKER V2 - Termux Optimized
import requests, os, time, webbrowser, socket
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

\033[1;37m🔥 AF CHECKER V2 – Termux Optimized
💻 Developer: Ali Hamza AF
📱 Runs on Android Termux
❤️ Powered by AF Cyber Force
""")

def fetch_proxies():
    print("[*] Generating proxies from ProxyScrape...")
    try:
        url = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&timeout=10000&country=all&proxy_format=ipport&format=text"
        res = requests.get(url, timeout=30)
        proxies = [p.strip() for p in res.text.splitlines() if p.strip()]
        with open("proxies.txt", "w") as f:
            f.write("\n".join(proxies))
        print(f"[✓] {len(proxies)} proxies saved to proxies.txt\n")
    except Exception as e:
        print(f"[!] Error: {e}")
        print("[!] Try using mobile data if Wi-Fi blocks the request\n")

def check_my_ip():
    try:
        print("[*] Checking your IP...")
        res = requests.get("https://ipinfo.io/json", timeout=10)
        data = res.json()
        print(f"\n[✓] Your IP: {data.get('ip')}")
        print(f"Location: {data.get('city')}, {data.get('region')}, {data.get('country')}")
        print(f"ISP: {data.get('org')}")
        print(f"Map: https://www.google.com/maps/place/{data.get('loc')}\n")
    except Exception as e:
        print(f"[!] Error: {e}")
        print("[*] Trying alternative method...")
        try:
            ip = requests.get("https://api.ipify.org", timeout=5).text
            print(f"\n[✓] Your IP: {ip}\n")
        except:
            print("[!] Failed to get IP address\n")

def check_proxy_ip():
    if not os.path.exists("proxies.txt"):
        print("[!] No proxies.txt found. Generate proxies first.\n")
        return
        
    with open("proxies.txt") as f:
        proxies = [line.strip() for line in f if line.strip()]
    
    if not proxies:
        print("[!] No proxies in file.\n")
        return
        
    proxy = proxies[0]
    print(f"[*] Testing proxy: {proxy}")
    proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    try:
        start = time.time()
        res = requests.get("https://ipinfo.io/json", proxies=proxy_dict, timeout=15)
        duration = time.time() - start
        data = res.json()
        print(f"\n[✓] Proxy IP: {data.get('ip')} | Time: {duration:.2f}s")
        print(f"Location: {data.get('city')}, {data.get('country')}")
        print(f"ISP: {data.get('org')}\n")
    except Exception as e:
        print(f"[!] Proxy Failed: {e}")
        print("[*] Tip: Free proxies often fail. Try generating a new list\n")

def scan_link():
    url = input("🔗 Enter URL to scan: ").strip()
    if not url:
        print("[!] Empty URL\n")
        return
        
    try:
        if not url.startswith(('http://', 'https://')):
            url = "http://" + url
            
        print(f"[*] Scanning: {url}")
        start = time.time()
        res = requests.get(url, timeout=15, allow_redirects=True)
        duration = time.time() - start
        
        security_status = "✅ Safe" if res.status_code == 200 else "⚠️ Suspicious"
        print(f"\n[✓] Status: {res.status_code} ({security_status})")
        print(f"Time: {duration:.2f}s")
        print(f"Final URL: {res.url}")
        print(f"Server: {res.headers.get('Server', 'Unknown')}")
        print(f"Size: {len(res.content)/1024:.2f} KB")
        
        # Security checks
        security_notes = []
        if 'php' in res.headers.get('Server', '').lower():
            security_notes.append("⚠️ PHP server - Common attack target")
        if len(res.content) < 1024:
            security_notes.append("⚠️ Small page size - Might be suspicious")
        if res.history:
            security_notes.append(f"⚠️ {len(res.history)} redirects detected")
            
        if security_notes:
            print("\nSecurity Notes:")
            for note in security_notes:
                print(f"• {note}")
        print()
        
    except Exception as e:
        print(f"[!] Scan Failed: {e}\n")

def termux_open(url):
    try:
        # Try using termux-open-url if available
        os.system(f"termux-open-url '{url}' 2>/dev/null")
        print("[*] Opening in your browser...")
    except:
        # Fallback to webbrowser module
        webbrowser.open(url)

def show_menu():
    print("""
[1] 🔁 Generate Proxies
[2] 🌐 Check My IP
[3] 🛡️  Test Proxy
[4] 🔍 Scan Link
[5] 📺 YouTube Channel
[6] 💬 WhatsApp Channel
[7] 🚪 Exit
""")

if __name__ == "__main__":
    banner()
    print("[*] Initializing Termux environment...")
    time.sleep(1)
    
    # Check internet connection
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
    except OSError:
        print("[!] No internet connection!\n")
    
    while True:
        try:
            show_menu()
            choice = input("📥 Select: ").strip()
            
            if choice == "1":
                fetch_proxies()
            elif choice == "2":
                check_my_ip()
            elif choice == "3":
                check_proxy_ip()
            elif choice == "4":
                scan_link()
            elif choice == "5":
                termux_open("https://youtube.com/@AliHamzaAF")
            elif choice == "6":
                termux_open("https://whatsapp.com/channel/0029VaU5UfBBVJl2sqYwbJ1t")
            elif choice == "7":
                print("👋 Exiting... Thank you for using AF Checker V2")
                break
            else:
                print("[!] Invalid option\n")
                
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\n\n👋 Operation cancelled. Press 7 to exit.")
            time.sleep(1)
