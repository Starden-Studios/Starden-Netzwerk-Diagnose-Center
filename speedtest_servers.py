import customtkinter as ctk
import threading
import time
import requests

class SpeedtestServersPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Speedtest (Server-Auswahl)", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        self.btn = ctk.CTkButton(self, text="Geschwindigkeit testen", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Messe...")
        self.textbox.delete("0.0", "end")
        def worker():
            servers = [
                ("Cloudflare", "https://speed.cloudflare.com/__down?bytes=10000000"),
                ("Hetzner", "https://speed.hetzner.de/10MB.bin"),
                ("Google", "https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/DDoS_Header.gif")
            ]
            for name, url in servers:
                try:
                    start = time.time()
                    total = 0
                    with requests.get(url, stream=True, timeout=10) as r:
                        for chunk in r.iter_content(chunk_size=32768):
                            total += len(chunk)
                            if time.time() - start > 5: break
                    speed = (total * 8) / ((time.time() - start) * 1_000_000)
                    self.after(0, lambda n=name, s=speed: self.textbox.insert("end", f"{n:<15} | {s:.2f} Mbit/s\n"))
                except:
                    self.after(0, lambda n=name: self.textbox.insert("end", f"{n:<15} | Fehler\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="Geschwindigkeit testen"))
        threading.Thread(target=worker, daemon=True).start()