import customtkinter as ctk
import threading
import time
import socket
import statistics

class MonitoringProPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # --- Titel ---
        ctk.CTkLabel(self, text="Monitoring Pro (Langzeit-Analyse)", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        ctk.CTkLabel(self, text="Analysiert Latenz, Jitter und Uptime über einen Zeitraum.", font=ctk.CTkFont(size=14), text_color="#aaa").pack(pady=(0, 20))
        
        # --- Button ---
        self.start_btn = ctk.CTkButton(self, text="Analyse starten (30 Sekunden)", height=40, command=self.start_analysis_thread)
        self.start_btn.pack(pady=10)
        
        # --- Textbox für Ausgabe ---
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def do_ping(self, target="1.1.1.1", timeout=1.0):
        try:
            start = time.time()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            s.connect((target, 53)) # DNS-Port, normalerweise offen
            s.close()
            return (time.time() - start) * 1000
        except:
            return None

    def start_analysis_thread(self):
        self.start_btn.configure(state="disabled", text="Analysiere...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Starte 30-Sekunden-Analyse...\n\n")
        threading.Thread(target=self.run_analysis, daemon=True).start()

    def run_analysis(self):
        target = "1.1.1.1"
        duration = 30 # Sekunden
        interval = 1 # 1 Ping pro Sekunde
        
        pings = []
        lost = 0
        total = 0
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            t = self.do_ping(target)
            total += 1
            
            if t is not None:
                pings.append(t)
                self.after(0, lambda p=t, c=total: self.textbox.insert("end", f"Ping {c}: {p:.1f} ms\n"))
            else:
                lost += 1
                self.after(0, lambda c=total: self.textbox.insert("end", f"Ping {c}: Timeout ❌\n"))
            
            self.after(0, lambda: self.textbox.see("end")) # Auto-scroll
            time.sleep(interval)
        
        # --- Auswertung ---
        self.after(0, lambda: self.textbox.insert("end", "\n" + "="*30 + "\n"))
        self.after(0, lambda: self.textbox.insert("end", "ERGEBNISSE:\n"))
        
        # 1. Uptime
        uptime = ((total - lost) / total) * 100
        self.after(0, lambda u=uptime: self.textbox.insert("end", f"Uptime: {u:.1f} % ({total-lost}/{total})\n"))
        
        if not pings:
            self.after(0, lambda: self.textbox.insert("end", "Keine Pings erfolgreich. Verbindung tot.\n"))
        else:
            # 2. Durchschnitt (Avg)
            avg = statistics.mean(pings)
            self.after(0, lambda a=avg: self.textbox.insert("end", f"Durchschnitt: {a:.1f} ms\n"))
            
            # 3. P95-Latenz (95% der Pings sind besser als dieser Wert)
            sorted_pings = sorted(pings)
            idx_95 = int(len(sorted_pings) * 0.95) - 1
            if idx_95 < 0: idx_95 = 0
            p95 = sorted_pings[idx_95]
            self.after(0, lambda p=p95: self.textbox.insert("end", f"P95-Latenz: {p:.1f} ms\n"))
            
            # 4. Jitter (Standardabweichung)
            if len(pings) > 1:
                jitter = statistics.stdev(pings)
                self.after(0, lambda j=jitter: self.textbox.insert("end", f"Jitter (StdAbw): {j:.1f} ms\n"))
            
            # 5. Min/Max
            self.after(0, lambda mi=min(pings), ma=max(pings): self.textbox.insert("end", f"Min: {mi:.1f} ms | Max: {ma:.1f} ms\n"))

        self.after(0, lambda: self.start_btn.configure(state="normal", text="Analyse starten (30 Sekunden)"))