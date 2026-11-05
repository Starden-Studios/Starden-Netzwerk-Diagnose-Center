import customtkinter as ctk
import socket
import time
import threading
import requests
from update_checker import UpdateChecker

class DashboardPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # --- Titel ---
        ctk.CTkLabel(self, text="System-Dashboard", font=ctk.CTkFont(size=32, weight="bold"), text_color="#88c0ff").pack(pady=20)
        ctk.CTkLabel(self, text="Schnellübersicht deines Netzwerks", font=ctk.CTkFont(size=16), text_color="#aaa").pack(pady=(0, 20))
        
        # --- Container für die Status-Karten ---
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        self.cards_frame.grid_columnconfigure(0, weight=1)
        self.cards_frame.grid_columnconfigure(1, weight=1)
        self.cards_frame.grid_columnconfigure(2, weight=1)

        self.ping_card = self.create_status_card(self.cards_frame, "Ping (Router)", "--- ms", 0)
        self.download_card = self.create_status_card(self.cards_frame, "Download (Internet)", "--- Mbit/s", 1)
        self.security_card = self.create_status_card(self.cards_frame, "Sicherheit", "---", 2)
        
        # --- Unterer Bereich: Schnell-Analyse Button ---
        self.analyze_btn = ctk.CTkButton(self, text="Schnell-Analyse starten", height=50, font=ctk.CTkFont(size=18, weight="bold"), command=self.start_analysis)
        self.analyze_btn.pack(pady=20, fill="x", padx=100)
        
        self.status_label = ctk.CTkLabel(self, text="Bereit für die Analyse.", font=ctk.CTkFont(size=14), text_color="#aaa")
        self.status_label.pack(pady=10)

        # --- Update-Checker (NEU) ---
        self.update_frame = UpdateChecker(self)
        self.update_frame.pack(pady=10, padx=100, fill="x")

    def create_status_card(self, parent, title, initial_value, col):
        card = ctk.CTkFrame(parent, fg_color="#161b22", corner_radius=15, border_width=1, border_color="#333")
        card.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14), text_color="#aaa").pack(pady=(20, 5))
        
        value_label = ctk.CTkLabel(card, text=initial_value, font=ctk.CTkFont(size=28, weight="bold"), text_color="#fff")
        value_label.pack(pady=5)
        
        status_indicator = ctk.CTkLabel(card, text="⚪ Unbekannt", font=ctk.CTkFont(size=14, weight="bold"), text_color="#aaa")
        status_indicator.pack(pady=(5, 20))
        
        return {"value": value_label, "status": status_indicator}

    def set_card_status(self, card, value, status_text, color):
        card["value"].configure(text=value)
        card["status"].configure(text=status_text, text_color=color)

    def start_analysis(self):
        self.analyze_btn.configure(state="disabled", text="Analysiere...")
        self.status_label.configure(text="Führe Schnell-Analyse durch...")
        
        self.set_card_status(self.ping_card, "--- ms", "Messe...", "#aaa")
        self.set_card_status(self.download_card, "--- Mbit/s", "Messe...", "#aaa")
        self.set_card_status(self.security_card, "---", "Prüfe...", "#aaa")
        
        threading.Thread(target=self.run_analysis, daemon=True).start()

    def run_analysis(self):
        # 1. Ping zum Router messen
        try:
            start = time.time()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            s.connect(("192.168.11.1", 80))
            s.close()
            ping_time = (time.time() - start) * 1000
            
            if ping_time < 10:
                self.after(0, lambda: self.set_card_status(self.ping_card, f"{ping_time:.1f} ms", "🟢 Optimal", "#2ea043"))
            elif ping_time < 50:
                self.after(0, lambda: self.set_card_status(self.ping_card, f"{ping_time:.1f} ms", "🟡 Okay", "#f1c40f"))
            else:
                self.after(0, lambda: self.set_card_status(self.ping_card, f"{ping_time:.1f} ms", "🔴 Schlecht", "#da3633"))
        except:
            self.after(0, lambda: self.set_card_status(self.ping_card, "Timeout", "🔴 Fehler", "#da3633"))

        # 2. Download-Geschwindigkeit testen
        try:
            start = time.time()
            total = 0
            with requests.get("https://speed.cloudflare.com/__down?bytes=5000000", stream=True, timeout=10) as r:
                for chunk in r.iter_content(chunk_size=32768):
                    total += len(chunk)
                    if time.time() - start > 3: break
            speed = (total * 8) / ((time.time() - start) * 1_000_000)
            
            if speed > 50:
                self.after(0, lambda: self.set_card_status(self.download_card, f"{speed:.1f} Mbit/s", "🟢 Sehr gut", "#2ea043"))
            elif speed > 16:
                self.after(0, lambda: self.set_card_status(self.download_card, f"{speed:.1f} Mbit/s", "🟡 Okay", "#f1c40f"))
            else:
                self.after(0, lambda: self.set_card_status(self.download_card, f"{speed:.1f} Mbit/s", "🔴 Langsam", "#da3633"))
        except:
            self.after(0, lambda: self.set_card_status(self.download_card, "Fehler", "🔴 Fehler", "#da3633"))

        # 3. Sicherheit prüfen (Port 23 Telnet)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex(("192.168.11.1", 23)) == 0:
                self.after(0, lambda: self.set_card_status(self.security_card, "Port 23 offen", "🔴 Risiko", "#da3633"))
            else:
                self.after(0, lambda: self.set_card_status(self.security_card, "Keine offenen Ports", "🟢 Sicher", "#2ea043"))
            s.close()
        except:
            self.after(0, lambda: self.set_card_status(self.security_card, "Unbekannt", "🟡 Prüfen", "#f1c40f"))

        self.after(0, lambda: self.analyze_btn.configure(state="normal", text="Analyse erneut starten"))
        self.after(0, lambda: self.status_label.configure(text="Analyse abgeschlossen."))