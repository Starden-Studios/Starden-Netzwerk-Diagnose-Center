import customtkinter as ctk
import threading
import subprocess

class DnsLeakPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="DNS-Leak-Test", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        
        self.btn = ctk.CTkButton(self, text="DNS-Leak prüfen", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Prüfe...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Prüfe DNS-Server...\n")
        
        def worker():
            try:
                out = subprocess.check_output(["nslookup", "google.com"], text=True, encoding="cp850", errors="ignore")
                self.after(0, lambda: self.textbox.insert("end", out))
                if "192.168" in out:
                    self.after(0, lambda: self.textbox.insert("end", "\n⚠️ Du nutzt einen lokalen DNS (Router). Das ist normal, aber kein VPN.\n"))
                else:
                    self.after(0, lambda: self.textbox.insert("end", "\n✅ DNS-Server sieht extern aus.\n"))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="DNS-Leak prüfen"))
        threading.Thread(target=worker, daemon=True).start()