import socket
import subprocess
import platform
import time
import requests

# ================= SYSTEM & NETZWERK =================

def get_local_ip():
    """Gibt die lokale IP-Adresse zurück."""
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "Unbekannt"

def get_gateway():
    """Findet den Standard-Gateway (Router) unter Windows."""
    try:
        if platform.system().lower() == "windows":
            output = subprocess.check_output(["ipconfig"], text=True, encoding="cp850", errors="ignore")
            for line in output.split("\n"):
                if "Standardgateway" in line or "Default Gateway" in line:
                    return line.split(":")[-1].strip()
    except:
        pass
    return "Unbekannt"

def get_wifi_signal():
    """Liest die aktuelle WLAN-Signalstärke aus."""
    try:
        if platform.system().lower() == "windows":
            cmd = 'netsh wlan show interfaces | findstr /C:"Signal"'
            output = subprocess.check_output(["powershell", "-Command", cmd], text=True, encoding="cp850", errors="ignore")
            if ":" in output:
                return output.split(":")[-1].strip()
    except:
        pass
    return "N/A"

def measure_ping(target="1.1.1.1", count=5):
    """Misst den Ping zu einem Ziel. Gibt Durchschnitt und Jitter zurück."""
    pings = []
    for _ in range(count):
        start = time.time()
        try:
            # Unter Windows nutzen wir ping -n 1, unter Linux -c 1
            param = "-n" if platform.system().lower() == "windows" else "-c"
            cmd = ["ping", param, "1", "-w", "1000", target] if platform.system().lower() == "windows" else ["ping", param, "1", "-W", "1", target]
            
            # Ausgabe unterdrücken
            startupinfo = None
            if platform.system().lower() == "windows":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            out = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo, timeout=2)
            
            if out.returncode == 0:
                # Wir nehmen die Zeit aus der Ausgabe oder messen selbst
                pings.append((time.time() - start) * 1000)
        except:
            pass
    
    if not pings:
        return 0, 0
    
    avg = sum(pings) / len(pings)
    jitter = sum([abs(pings[i] - pings[i-1]) for i in range(1, len(pings))]) / (len(pings)-1) if len(pings) > 1 else 0
    return avg, jitter

def measure_download(url="https://speed.cloudflare.com/__down?bytes=10000000", duration=5):
    """Misst die Download-Geschwindigkeit. Gibt Mbit/s zurück."""
    try:
        start = time.time()
        total_bytes = 0
        with requests.get(url, stream=True, timeout=10) as r:
            for chunk in r.iter_content(chunk_size=32768):
                total_bytes += len(chunk)
                if time.time() - start > duration:
                    break
        elapsed = time.time() - start
        return (total_bytes * 8) / (elapsed * 1_000_000)
    except:
        return 0

# ================= KONSTANTEN =================
PING_URL = "https://speed.cloudflare.com/__down?bytes=100"
DOWNLOAD_URL = "https://speed.cloudflare.com/__down?bytes=25000000"
UPLOAD_URL = "https://speed.cloudflare.com/__up"