import customtkinter as ctk
import threading
import requests
import subprocess
import platform

class SystemInfoPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="System & Netzwerk-Info", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        
        self.btn = ctk.CTkButton(self, text="Infos abrufen", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Lade...")
        self.textbox.delete("0.0", "end")
        
        def worker():
            self.after(0, lambda: self.textbox.insert("end", "Rufe öffentliche IP ab...\n"))
            try:
                r = requests.get("https://api.ipify.org?format=json", timeout=5)
                ip = r.json()["ip"]
                self.after(0, lambda: self.textbox.insert("end", f"Öffentliche IP: {ip}\n"))
                
                # Geo-Lookup
                geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
                if geo["status"] == "success":
                    self.after(0, lambda: self.textbox.insert("end", f"Standort: {geo['city']}, {geo['country']} (ISP: {geo['isp']})\n"))
            except:
                self.after(0, lambda: self.textbox.insert("end", "Geo-IP fehlgeschlagen.\n"))
            
            self.after(0, lambda: self.btn.configure(state="normal", text="Infos abrufen"))
        
        threading.Thread(target=worker, daemon=True).start()