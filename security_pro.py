import customtkinter as ctk
import threading
import subprocess
import platform
import socket

class SecurityProPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # --- Titel ---
        ctk.CTkLabel(self, text="Security Pro (Erweitert)", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        ctk.CTkLabel(self, text="Tiefen-Analyse deines Netzwerks.", font=ctk.CTkFont(size=14), text_color="#aaa").pack(pady=(0, 20))
        
        # --- Button-Leiste ---
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=10)
        
        self.arp_btn = ctk.CTkButton(self.btn_frame, text="ARP-Spoofing Detektor", width=200, command=self.run_arp_check)
        self.arp_btn.pack(side="left", padx=10)
        
        self.service_btn = ctk.CTkButton(self.btn_frame, text="Service-Discovery (LAN)", width=200, command=self.run_service_discovery)
        self.service_btn.pack(side="left", padx=10)
        
        self.vendor_btn = ctk.CTkButton(self.btn_frame, text="Vendor-Lookup (MAC)", width=200, command=self.run_vendor_lookup)
        self.vendor_btn.pack(side="left", padx=10)

        # --- Textbox für Ausgabe ---
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    # ================= ARP-SPOOFING =================
    def run_arp_check(self):
        self.arp_btn.configure(state="disabled", text="Prüfe...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Prüfe ARP-Tabelle auf Spoofing...\n\n")
        
        def worker():
            try:
                output = subprocess.check_output(["arp", "-a"], text=True, encoding="cp850", errors="ignore")
                lines = output.split("\n")
                
                mac_to_ips = {}
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 2 and ("." in parts[0]) and ("-" in parts[1] or ":" in parts[1]):
                        ip = parts[0]
                        mac = parts[1].lower()
                        if mac not in mac_to_ips:
                            mac_to_ips[mac] = []
                        mac_to_ips[mac].append(ip)
                
                result = "ARP-Tabelle:\n"
                result += f"{'IP-Adresse':<20} | {'MAC-Adresse':<20}\n"
                result += "-" * 45 + "\n"
                
                spoofed = False
                for mac, ips in mac_to_ips.items():
                    if len(ips) > 1:
                        result += f"🚨 WARNUNG: MAC {mac} ist mit mehreren IPs verbunden: {', '.join(ips)}\n"
                        spoofed = True
                    for ip in ips:
                        result += f"{ip:<20} | {mac:<20}\n"
                
                if not spoofed:
                    result += "\n✅ Kein ARP-Spoofing erkannt.\n"
                
                self.after(0, lambda: self.textbox.insert("end", result))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
            
            self.after(0, lambda: self.arp_btn.configure(state="normal", text="ARP-Spoofing Detektor"))
        
        threading.Thread(target=worker, daemon=True).start()

    # ================= SERVICE-DISCOVERY =================
    def run_service_discovery(self):
        self.service_btn.configure(state="disabled", text="Scanne...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Scanne Dienste auf Geräten im LAN...\n\n")
        
        def worker():
            try:
                # Einfache Service-Discovery: Wir prüfen die offenen Ports auf bekannten IPs
                output = subprocess.check_output(["arp", "-a"], text=True, encoding="cp850", errors="ignore")
                lines = output.split("\n")
                
                ips = set()
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 1 and ("." in parts[0]):
                        ips.add(parts[0])
                
                result = "Service-Discovery:\n"
                for ip in list(ips)[:5]: # Nur die ersten 5 IPs prüfen, um es schnell zu halten
                    result += f"\n--- Prüfe {ip} ---\n"
                    common_ports = {21: "FTP", 22: "SSH", 23: "Telnet", 80: "HTTP", 443: "HTTPS"}
                    for port, name in common_ports.items():
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(0.3)
                        if s.connect_ex((ip, port)) == 0:
                            result += f"  Port {port} ({name}): OFFEN ✅\n"
                        s.close()
                
                self.after(0, lambda: self.textbox.insert("end", result))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
            
            self.after(0, lambda: self.service_btn.configure(state="normal", text="Service-Discovery (LAN)"))
        
        threading.Thread(target=worker, daemon=True).start()

    # ================= VENDOR-LOOKUP =================
    def run_vendor_lookup(self):
        self.vendor_btn.configure(state="disabled", text="Prüfe...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Führe Vendor-Lookup durch (MAC-OUI)...\n\n")
        
        def worker():
            try:
                output = subprocess.check_output(["arp", "-a"], text=True, encoding="cp850", errors="ignore")
                lines = output.split("\n")
                
                result = "Geräte-Hersteller:\n"
                result += f"{'IP-Adresse':<20} | {'MAC-Adresse':<20} | {'Vendor (OUI)':<20}\n"
                result += "-" * 65 + "\n"
                
                found = False
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 2 and ("." in parts[0]) and ("-" in parts[1] or ":" in parts[1]):
                        ip = parts[0]
                        mac = parts[1].upper().replace("-", ":")
                        # Die ersten 3 Bytes (OUI) sind der Hersteller
                        oui = mac[:8] 
                        # (Eine echte Datenbank wäre hier nötig, wir zeigen nur die OUI)
                        result += f"{ip:<20} | {mac:<20} | {oui}\n"
                        found = True
                
                if not found:
                    result += "Keine Geräte gefunden.\n"
                
                self.after(0, lambda: self.textbox.insert("end", result))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
            
            self.after(0, lambda: self.vendor_btn.configure(state="normal", text="Vendor-Lookup (MAC)"))
        
        threading.Thread(target=worker, daemon=True).start()