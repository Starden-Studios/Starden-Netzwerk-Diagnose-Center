import customtkinter as ctk
import threading
import subprocess
import platform

class WifiStrengthPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="WLAN-Signalstärke", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        self.btn = ctk.CTkButton(self, text="Signal messen", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Messe...")
        self.textbox.delete("0.0", "end")
        def worker():
            try:
                cmd = 'netsh wlan show interfaces | findstr /C:"Signal"'
                out = subprocess.check_output(["powershell", "-Command", cmd], text=True, encoding="cp850", errors="ignore")
                if ":" in out:
                    signal = out.split(":")[-1].strip()
                    self.after(0, lambda: self.textbox.insert("end", f"Signalstärke: {signal}\n"))
                else:
                    self.after(0, lambda: self.textbox.insert("end", "Signal konnte nicht gelesen werden.\n"))
            except:
                self.after(0, lambda: self.textbox.insert("end", "Fehler beim Auslesen.\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="Signal messen"))
        threading.Thread(target=worker, daemon=True).start()