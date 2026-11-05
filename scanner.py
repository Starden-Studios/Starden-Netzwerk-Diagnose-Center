import customtkinter as ctk
import threading
import subprocess
import platform

class ScannerPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # --- Titel ---
        ctk.CTkLabel(self, text="WLAN & Signal-Analyse", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        
        # --- Live-Anzeige der Signalstärke ---
        self.signal_frame = ctk.CTkFrame(self, fg_color="#161b22", corner_radius=10)
        self.signal_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(self.signal_frame, text="Verbindungsstatus:", font=ctk.CTkFont(size=14), text_color="#aaa").pack(pady=(10, 0))
        self.signal_label = ctk.CTkLabel(self.signal_frame, text="---", font=ctk.CTkFont(size=28, weight="bold"), text_color="#3498db")
        self.signal_label.pack(pady=(0, 10))
        
        # --- Button zum Aktualisieren der Signalstärke ---
        self.refresh_btn = ctk.CTkButton(self.signal_frame, text="Status aktualisieren", height=30, command=self.update_signal)
        self.refresh_btn.pack(pady=(0, 10))

        # --- WLAN-Scan Button ---
        self.scan_btn = ctk.CTkButton(self, text="WLAN-Umgebung scannen", height=40, command=self.start_scan_thread)
        self.scan_btn.pack(pady=10)
        
        # --- Textbox für die Ausgabe ---
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)
        
        # Status beim Start einmal abrufen
        self.update_signal()

    def update_signal(self):
        """Prüft den Verbindungsstatus (Fallback, falls kein WLAN-Adapter gefunden wird)."""
        if platform.system().lower() != "windows":
            self.signal_label.configure(text="Nur Windows")
            return

        try:
            # Wir prüfen, ob wir überhaupt eine aktive Netzwerkverbindung haben
            cmd = 'ping -n 1 1.1.1.1'
            output = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="cp850", errors="ignore")
            
            if "Antwort von" in output.stdout or "Reply from" in output.stdout:
                # Verbindung ist da. Wir prüfen, ob es WLAN oder LAN ist.
                cmd_wlan = 'netsh wlan show interfaces'
                wlan_output = subprocess.run(cmd_wlan, shell=True, capture_output=True, text=True, encoding="cp850", errors="ignore")
                
                if "Signal" in wlan_output.stdout:
                    # Wenn wir hier reinkommen, ist es ein echtes WLAN
                    for line in wlan_output.stdout.split("\n"):
                        if "Signal" in line:
                            signal = line.split(":")[-1].strip()
                            self.signal_label.configure(text=f"{signal}")
                            return
                else:
                    # Kein echtes WLAN (Repeater oder LAN)
                    self.signal_label.configure(text="Verbunden (via Repeater/LAN)")
                    return
            else:
                self.signal_label.configure(text="Keine Verbindung")
                
        except Exception as e:
            self.signal_label.configure(text="Fehler")
            print(f"Status-Fehler: {e}")

    def start_scan_thread(self):
        self.scan_btn.configure(state="disabled", text="Scanne...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Starte WLAN-Scan... (Dies kann einige Sekunden dauern)\n")
        threading.Thread(target=self.run_scan, daemon=True).start()

    def run_scan(self):
        try:
            if platform.system().lower() == "windows":
                cmd = 'netsh wlan show networks mode=bssid'
                output = subprocess.check_output(cmd, shell=True, text=True, encoding="cp850", errors="ignore")
                
                self.after(0, lambda: self.textbox.delete("0.0", "end"))
                self.after(0, lambda: self.textbox.insert("0.0", output))
            else:
                self.after(0, lambda: self.textbox.insert("end", "WLAN-Scan wird nur unter Windows unterstützt.\n"))
        except Exception as e:
            self.after(0, lambda: self.textbox.insert("end", f"\nFehler: {e}"))
        finally:
            self.after(0, lambda: self.scan_btn.configure(state="normal", text="WLAN-Umgebung scannen"))