import customtkinter as ctk
import psutil
import threading
import time

class MonitoringPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # --- Titel ---
        ctk.CTkLabel(self, text="Bandbreiten-Monitor (Live)", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        
        # --- Info ---
        ctk.CTkLabel(self, text="Zeigt Prozesse, die gerade aktive Internetverbindungen haben.", text_color="#aaa").pack(pady=5)
        
        # --- Textbox für die Ausgabe ---
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)
        
        # --- Live-Update starten ---
        self.is_running = True
        self.update_thread = threading.Thread(target=self.live_update_loop, daemon=True)
        self.update_thread.start()

    def live_update_loop(self):
        while self.is_running:
            try:
                # Wir sammeln alle Prozesse, die aktive Verbindungen haben
                procs = {}
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        # connections() braucht oft Admin-Rechte, aber wir versuchen es
                        conns = proc.connections()
                        if conns:
                            # Wir zählen nur Verbindungen, die nicht lokal sind (also echte Internet-Verbindungen)
                            ext_conns = [c for c in conns if c.raddr]
                            if ext_conns:
                                procs[proc.info['name']] = len(ext_conns)
                    except:
                        pass
                
                # Sortieren nach Anzahl der Verbindungen
                sorted_procs = sorted(procs.items(), key=lambda x: x[1], reverse=True)[:15]
                
                # Ausgabe formatieren
                output = "Prozess (Externe Verbindungen)\n" + "-"*40 + "\n"
                for name, count in sorted_procs:
                    output += f"{name[:25]:<25} | {count}\n"
                
                if not sorted_procs:
                    output = "Keine aktiven Internet-Verbindungen gefunden.\n"
                
                # GUI aktualisieren (muss im Haupt-Thread passieren)
                self.after(0, lambda: self.update_textbox(output))
                
            except Exception as e:
                self.after(0, lambda: self.update_textbox(f"Fehler: {e}\n"))
            
            time.sleep(2) # Alle 2 Sekunden aktualisieren

    def update_textbox(self, text):
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", text)