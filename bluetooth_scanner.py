import customtkinter as ctk
import threading

class BluetoothScannerPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Bluetooth-Scanner", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        
        self.btn = ctk.CTkButton(self, text="Bluetooth-Geräte suchen", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Suche...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Suche Bluetooth-Geräte (Windows API)...\n\n")
        
        def worker():
            try:
                # Einfacher Ansatz: Wir listen die Bluetooth-Geräte über PowerShell auf
                import subprocess
                ps = "Get-PnpDevice -Class Bluetooth | Select-Object FriendlyName, Status"
                out = subprocess.check_output(["powershell", "-Command", ps], text=True, encoding="cp850", errors="ignore")
                self.after(0, lambda: self.textbox.insert("end", out))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
            
            self.after(0, lambda: self.btn.configure(state="normal", text="Bluetooth-Geräte suchen"))
        
        threading.Thread(target=worker, daemon=True).start()