import customtkinter as ctk
import threading
import subprocess

class MeshScannerPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Mesh-Netzwerk-Scanner", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        self.btn = ctk.CTkButton(self, text="Mesh-Knoten suchen", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Suche...")
        self.textbox.delete("0.0", "end")
        
        def worker():
            try:
                # Befehl ausführen
                cmd = 'netsh wlan show networks mode=bssid | findstr /C:"BSSID"'
                out = subprocess.check_output(["powershell", "-Command", cmd], text=True, encoding="cp850", errors="ignore")
                
                # Ergebnis in die Textbox schreiben
                self.after(0, lambda: self.textbox.insert("end", f"Mesh-Knoten (BSSIDs):\n{out}\n"))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
            
            # Button wieder aktivieren
            self.after(0, lambda: self.btn.configure(state="normal", text="Mesh-Knoten suchen"))
        
        threading.Thread(target=worker, daemon=True).start()