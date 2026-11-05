import customtkinter as ctk
import threading
import requests

class PublicIpPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Public IP & Geo", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        
        self.btn = ctk.CTkButton(self, text="IP abrufen", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Lade...")
        self.textbox.delete("0.0", "end")
        def worker():
            try:
                r = requests.get("https://api.ipify.org?format=json", timeout=5)
                ip = r.json()["ip"]
                self.after(0, lambda: self.textbox.insert("end", f"Öffentliche IP: {ip}\n"))
                geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
                self.after(0, lambda: self.textbox.insert("end", f"Standort: {geo.get('city')}, {geo.get('country')}\nISP: {geo.get('isp')}\n"))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="IP abrufen"))
        threading.Thread(target=worker, daemon=True).start()