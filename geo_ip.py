import customtkinter as ctk
import threading
import requests

class GeoIpPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Geo-IP-Lookup", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        self.btn = ctk.CTkButton(self, text="Standort ermitteln", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Lade...")
        self.textbox.delete("0.0", "end")
        def worker():
            try:
                ip = requests.get("https://api.ipify.org?format=json", timeout=5).json()["ip"]
                geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
                self.after(0, lambda: self.textbox.insert("end", f"IP: {ip}\n"))
                self.after(0, lambda: self.textbox.insert("end", f"Land: {geo.get('country')}\n"))
                self.after(0, lambda: self.textbox.insert("end", f"Stadt: {geo.get('city')}\n"))
                self.after(0, lambda: self.textbox.insert("end", f"ISP: {geo.get('isp')}\n"))
                self.after(0, lambda: self.textbox.insert("end", f"Lat/Lon: {geo.get('lat')}, {geo.get('lon')}\n"))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="Standort ermitteln"))
        threading.Thread(target=worker, daemon=True).start()