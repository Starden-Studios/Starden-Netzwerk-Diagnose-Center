import customtkinter as ctk
import threading
import requests

class VpnCheckPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="VPN-Erkennung", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        self.btn = ctk.CTkButton(self, text="VPN prüfen", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Prüfe...")
        self.textbox.delete("0.0", "end")
        def worker():
            try:
                r1 = requests.get("https://api.ipify.org?format=json", timeout=5).json()["ip"]
                r2 = requests.get("https://ipinfo.io/json", timeout=5).json()
                if r2.get("org", "").lower().find("vpn") != -1 or r2.get("org", "").lower().find("hosting") != -1:
                    self.after(0, lambda: self.textbox.insert("end", f"🚨 VPN/Proxy erkannt! IP: {r1}\nOrg: {r2.get('org')}\n"))
                else:
                    self.after(0, lambda: self.textbox.insert("end", f"✅ Keine VPN erkannt. IP: {r1}\nOrg: {r2.get('org')}\n"))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="VPN prüfen"))
        threading.Thread(target=worker, daemon=True).start()