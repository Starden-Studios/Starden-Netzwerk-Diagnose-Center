# 👁️ Starden Netzwerk Diagnose Center (NDC)

**Ein professionelles, modulares Netzwerk-Diagnose-Tool für Windows – inspiriert von germanischer Mythologie und moderner Netzwerktechnik.**

![Logo](icon.ico)

---

## 📖 Über das Projekt

Das **Starden Netzwerk Diagnose Center** ist ein umfassendes Tool zur Analyse, Überwachung und Reparatur von Netzwerken. Es wurde entwickelt, um Probleme mit WLAN, Routing, DNS und Sicherheit aufzudecken und zu beheben – ohne teure Software.

Ursprünglich als kleines Python-Skript gestartet, ist es heute ein modulares Programm mit **über 40 Modulen**, die in einer aufklappbaren Seitenleiste organisiert sind.

---

## ✨ Features (Auszug)

### 📊 Übersicht
- **Dashboard:** Ampel-Übersicht über Ping, Download und Sicherheit.
- **Speed & Traffic:** Live-Geschwindigkeitstest mit Diagramm.

### 📡 WLAN & Funk
- **WLAN & Signal:** Signalstärke, Kanal, BSSID-Tracking.
- **WLAN Pro:** Umgebungsscan, versteckte Netzwerke, Sicherheitscheck.

### 🌐 Routing & Internet
- **Routing Live:** Server-Ping-Matrix (Router, Google, Cloudflare).
- **Advanced Routing:** TTFB, MTU-Discovery, Traceroute.
- **DNS & IP:** DNS-Lookup, Reverse DNS, Whois, Geo-IP, IPv6-Check.

### 🛡️ Sicherheit
- **Port-Scanner:** Lokal und im LAN.
- **Security Pro:** ARP-Spoofing, Service-Discovery, Vendor-Lookup.
- **VPN/Proxy-Check:** DNS-Leak-Test, Firewall-Status.

### 🛠️ Analyse & Tools
- **Monitoring:** Live-Traffic pro Prozess, P95-Latenz, Jitter-Trend.
- **Gaming & Bufferbloat:** Testet die Gaming-Tauglichkeit.
- **Packet Sniffer:** Zeigt aktive Verbindungen.
- **TCP-Optimierer:** Passt Windows-TCP-Einstellungen an.

### ⚙️ System & Reset
- **Doctor:** Repariert DNS-Cache, Winsock und IP-Stack (mit Admin-Rechten).
- **Update-Checker:** Prüft auf neue Versionen.

---

## 🚀 Installation

### Option 1: Installer (empfohlen)
1. Lade die neueste `Starden_NDC_Setup.exe` aus den [Releases](https://github.com/DEIN-NAME/DEIN-REPO/releases) herunter.
2. Führe den Installer aus.
3. Starte das Programm über die Desktop-Verknüpfung.

### Option 2: Portable Version
1. Lade die `main.exe` aus den Releases herunter.
2. Lege sie in einen Ordner deiner Wahl.
3. Doppelklicke sie (für einige Features werden Admin-Rechte benötigt).

---

## 🛠️ Entwicklung

### Voraussetzungen
- Python 3.10+
- Bibliotheken: `pip install customtkinter requests matplotlib psutil packaging`

### Starten
```bash
python main.py