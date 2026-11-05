import customtkinter as ctk
import threading
import requests

class HttpCheckPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="HTTP/HTTPS-Check", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        self.btn = ctk.CTkButton(self, text="Webseiten prüfen", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Prüfe...")
        self.textbox.delete("0.0", "end")
        def worker():
            sites = ["https://google.com", "https://youtube.com", "https://cloudflare.com", "https://github.com"]
            for site in sites:
                try:
                    r = requests.get(site, timeout=5)
                    self.after(0, lambda s=site, c=r.status_code: self.textbox.insert("end", f"{s:<25} -> {c} OK\n"))
                except:
                    self.after(0, lambda s=site: self.textbox.insert("end", f"{s:<25} -> FEHLER\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="Webseiten prüfen"))
        threading.Thread(target=worker, daemon=True).start()