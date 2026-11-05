import customtkinter as ctk
import socket
import subprocess
import platform
import threading

class SecurityPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # --- Titel ---
        ctk.CTkLabel(self, text="Sicherheit & Netzwerk-Scan", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        
        # --- Button-Leiste ---
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=10)
        
        self.port_btn = ctk.CTkButton(self.btn_frame, text="Port-Scan (Router)", width=200, command=self.run_port_scan)
        self.port_btn.pack(side="left", padx=10)
        
        self.mac_btn = ctk.CTkButton(self.btn_frame, text="MAC-Adressen scannen", width=200, command=self.run_mac_scan)
        self.mac_btn.pack(side="left", padx=10)
        
        self.dns_btn = ctk.CTkButton(self.btn_frame, text="DNS-Leak Test", width=200, command=self.run_dns_leak)
        self.dns_btn.pack(side="left", padx=10)

        # --- Textbox für Ausgabe ---
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def get_gateway(self):
        """Ermittelt den Router (Gateway)."""
        try:
            if platform.system().lower() == "windows":
                output = subprocess.check_output(["ipconfig"], text=True, encoding="cp850", errors="ignore")
                for line in output.split("\n"):
                    if "Standardgateway" in line or "Default Gateway" in line:
                        return line.split(":")[-1].strip()
        except:
            pass
        return "192.168.11.1" # Fallback

    # ================= PORT-SCAN =================
    def run_port_scan(self):
        self.port_btn.configure(state="disabled", text="Scanne...")
        self.textbox.insert("end", f"\n--- Starte Port-Scan auf {self.get_gateway()} ---\n")
        
        def scan():
            gateway = self.get_gateway()
            # Die wichtigsten Ports für einen Heimrouter
            ports_to_check = [21, 22, 23, 53, 80, 443, 8080]
            open_ports = []
            
            for port in ports_to_check:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5) # Kurzer Timeout für schnellen Scan
                try:
                    if s.connect_ex((gateway, port)) == 0:
                        open_ports.append(port)
                except:
                    pass
                s.close()
            
            if open_ports:
                result = f"Gefundene offene Ports: {', '.join(map(str, open_ports))}\n"
                if 23 in open_ports:
                    result += "🚨 WARNUNG: Port 23 (Telnet) ist offen! Das ist ein Sicherheitsrisiko.\n"
            else:
                result = "Keine der Standard-Ports sind offen. (Das ist gut!)\n"
            
            self.after(0, lambda: self.textbox.insert("end", result))
            self.after(0, lambda: self.port_btn.configure(state="normal", text="Port-Scan (Router)"))
        
        threading.Thread(target=scan, daemon=True).start()

    # ================= MAC-SCAN =================
    def run_mac_scan(self):
        self.mac_btn.configure(state="disabled", text="Scanne...")
        self.textbox.insert("end", "\n--- Scanne MAC-Adressen im LAN (ARP) ---\n")
        
        def scan():
            try:
                # arp -a listet alle Geräte auf, mit denen dein PC kommuniziert hat
                output = subprocess.check_output(["arp", "-a"], text=True, encoding="cp850", errors="ignore")
                lines = output.split("\n")
                
                result = f"{'IP-Adresse':<20} | {'MAC-Adresse':<20}\n"
                result += "-" * 45 + "\n"
                
                found = False
                for line in lines:
                    parts = line.split()
                    # Prüfen, ob die Zeile eine IP und eine MAC enthält
                    if len(parts) >= 2 and ("." in parts[0]) and ("-" in parts[1] or ":" in parts[1]):
                        result += f"{parts[0]:<20} | {parts[1]:<20}\n"
                        found = True
                
                if not found:
                    result = "Keine Geräte im ARP-Cache gefunden. (Bist du mit dem Internet verbunden?)\n"
                
                self.after(0, lambda: self.textbox.insert("end", result))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
            
            self.after(0, lambda: self.mac_btn.configure(state="normal", text="MAC-Adressen scannen"))
        
        threading.Thread(target=scan, daemon=True).start()

    # ================= DNS-LEAK =================
    def run_dns_leak(self):
        self.dns_btn.configure(state="disabled", text="Teste...")
        self.textbox.insert("end", "\n--- DNS-Leak Test ---\n")
        
        def scan():
            try:
                # nslookup zeigt den Standard-DNS-Server an
                output = subprocess.check_output(["nslookup", "google.com"], text=True, encoding="cp850", errors="ignore")
                
                # Wir suchen die Zeile mit "Server:" oder "Address:"
                result = "DNS-Auflösung:\n"
                for line in output.split("\n"):
                    if "Server:" in line or "Address:" in line:
                        result += line + "\n"
                
                self.after(0, lambda: self.textbox.insert("end", result))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
            
            self.after(0, lambda: self.dns_btn.configure(state="normal", text="DNS-Leak Test"))
        
        threading.Thread(target=scan, daemon=True).start()