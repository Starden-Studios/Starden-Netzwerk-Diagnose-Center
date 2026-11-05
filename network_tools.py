import customtkinter as ctk
import threading
import subprocess
import platform
import socket
import time
import requests

class NetworkToolsPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # --- Titel ---
        ctk.CTkLabel(self, text="Network Tools", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        ctk.CTkLabel(self, text="Erweiterte Netzwerk-Analyse und Simulation.", font=ctk.CTkFont(size=14), text_color="#aaa").pack(pady=(0, 20))
        
        # --- Button-Leiste ---
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=10)
        
        self.dns_btn = ctk.CTkButton(self.btn_frame, text="DNS-Vergleich", width=180, command=self.run_dns_compare)
        self.dns_btn.pack(side="left", padx=5)
        
        self.sweep_btn = ctk.CTkButton(self.btn_frame, text="Ping-Sweep (LAN)", width=180, command=self.run_ping_sweep)
        self.sweep_btn.pack(side="left", padx=5)
        
        self.loss_btn = ctk.CTkButton(self.btn_frame, text="Packet-Loss-Sim", width=180, command=self.run_packet_loss)
        self.loss_btn.pack(side="left", padx=5)

        # --- Textbox für Ausgabe ---
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def get_gateway(self):
        try:
            if platform.system().lower() == "windows":
                output = subprocess.check_output(["ipconfig"], text=True, encoding="cp850", errors="ignore")
                for line in output.split("\n"):
                    if "Standardgateway" in line or "Default Gateway" in line:
                        return line.split(":")[-1].strip()
        except: pass
        return "192.168.11.1"

    def tcp_ping(self, ip, port=53, timeout=1.0):
        """TCP-Ping (funktioniert auch, wenn ICMP blockiert wird)."""
        try:
            start = time.time()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            s.connect((ip, port))
            s.close()
            return (time.time() - start) * 1000
        except:
            return None

    # ================= DNS-VERGLEICH =================
    def run_dns_compare(self):
        self.dns_btn.configure(state="disabled", text="Teste...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "DNS-Vergleich (Latenz zu DNS-Servern)...\n\n")
        
        def worker():
            dns_servers = [
                ("Standard (Router)", self.get_gateway()),
                ("Google DNS", "8.8.8.8"),
                ("Cloudflare DNS", "1.1.1.1")
            ]
            
            results = []
            for name, ip in dns_servers:
                pings = []
                for _ in range(5):
                    t = self.tcp_ping(ip, 53)
                    if t: pings.append(t)
                if pings:
                    avg = sum(pings) / len(pings)
                    results.append((name, ip, avg))
                    self.after(0, lambda n=name, i=ip, a=avg: self.textbox.insert("end", f"{n:<20} ({i}): {a:.1f} ms\n"))
                else:
                    self.after(0, lambda n=name, i=ip: self.textbox.insert("end", f"{n:<20} ({i}): Timeout\n"))
            
            # Empfehlung
            if results:
                best = min(results, key=lambda x: x[2])
                self.after(0, lambda b=best: self.textbox.insert("end", f"\n🏆 Empfehlung: {b[0]} ({b[1]}) mit {b[2]:.1f} ms.\n"))
            
            self.after(0, lambda: self.dns_btn.configure(state="normal", text="DNS-Vergleich"))
        
        threading.Thread(target=worker, daemon=True).start()

    # ================= PING-SWEEP =================
    def run_ping_sweep(self):
        self.sweep_btn.configure(state="disabled", text="Scanne...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Ping-Sweep (Suche aktive Geräte im LAN)...\n\n")
        
        def worker():
            gateway = self.get_gateway()
            base_ip = ".".join(gateway.split(".")[:3])
            
            active_ips = []
            self.after(0, lambda: self.textbox.insert("end", f"Scanne {base_ip}.1 bis {base_ip}.254...\n"))
            
            for i in range(1, 255):
                ip = f"{base_ip}.{i}"
                # TCP-Ping auf Port 80/443 (oft offen) oder ICMP-Ping
                t = self.tcp_ping(ip, 80, timeout=0.1) or self.tcp_ping(ip, 443, timeout=0.1)
                
                if t is not None:
                    active_ips.append(ip)
                    self.after(0, lambda x=ip: self.textbox.insert("end", f"  ✅ {x} ist ONLINE\n"))
            
            if not active_ips:
                self.after(0, lambda: self.textbox.insert("end", "\nKeine aktiven Geräte gefunden (oder Firewall blockiert).\n"))
            else:
                self.after(0, lambda c=len(active_ips): self.textbox.insert("end", f"\n📊 {c} aktive Geräte gefunden.\n"))
            
            self.after(0, lambda: self.sweep_btn.configure(state="normal", text="Ping-Sweep (LAN)"))
        
        threading.Thread(target=worker, daemon=True).start()

    # ================= PACKET-LOSS-SIMULATION =================
    def run_packet_loss(self):
        self.loss_btn.configure(state="disabled", text="Simuliere...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Packet-Loss-Simulation (Ping-Test mit künstlichem Verlust)...\n\n")
        
        def worker():
            # Wir senden 50 Pings an Cloudflare und zählen die Timeouts
            target = "1.1.1.1"
            total_pings = 50
            lost = 0
            pings = []
            
            for i in range(total_pings):
                t = self.tcp_ping(target, 53, timeout=1.0)
                if t is None:
                    lost += 1
                else:
                    pings.append(t)
                
                if (i+1) % 10 == 0:
                    self.after(0, lambda cur=i+1: self.textbox.insert("end", f"  {cur}/{total_pings} Pings gesendet...\n"))
            
            loss_percent = (lost / total_pings) * 100
            avg_ping = sum(pings) / len(pings) if pings else 0
            
            self.after(0, lambda: self.textbox.insert("end", f"\n--- Ergebnis ---\n"))
            self.after(0, lambda: self.textbox.insert("end", f"Gesendet: {total_pings}\n"))
            self.after(0, lambda: self.textbox.insert("end", f"Verloren: {lost} ({loss_percent:.1f} %)\n"))
            self.after(0, lambda: self.textbox.insert("end", f"Durchschnittlicher Ping: {avg_ping:.1f} ms\n"))
            
            if loss_percent > 5:
                self.after(0, lambda: self.textbox.insert("end", "🚨 Hoher Paketverlust! Deine Verbindung ist instabil.\n"))
            elif loss_percent > 0:
                self.after(0, lambda: self.textbox.insert("end", "⚠️ Leichter Paketverlust. Beobachten!\n"))
            else:
                self.after(0, lambda: self.textbox.insert("end", "✅ Kein Paketverlust. Perfekt!\n"))
            
            self.after(0, lambda: self.loss_btn.configure(state="normal", text="Packet-Loss-Sim"))
        
        threading.Thread(target=worker, daemon=True).start()