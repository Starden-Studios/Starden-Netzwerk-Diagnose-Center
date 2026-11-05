import customtkinter as ctk
import threading
import subprocess

class DriverCheckPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="WLAN-Treiber-Check", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        self.btn = ctk.CTkButton(self, text="Treiber anzeigen", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Lade...")
        self.textbox.delete("0.0", "end")
        def worker():
            try:
                cmd = 'Get-PnpDevice -Class Net | Where-Object { $_.FriendlyName -like "*Wireless*" -or $_.FriendlyName -like "*WLAN*" } | Select-Object FriendlyName, Status, Version'
                out = subprocess.check_output(["powershell", "-Command", cmd], text=True, encoding="cp850", errors="ignore")
                self.after(0, lambda: self.textbox.insert("end", f"WLAN-Treiber:\n{out}\n"))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="Treiber anzeigen"))
        threading.Thread(target=worker, daemon=True).start()