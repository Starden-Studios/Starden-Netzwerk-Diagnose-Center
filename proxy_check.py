import customtkinter as ctk
import threading
import urllib.request

class ProxyCheckPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Proxy-Check", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        self.btn = ctk.CTkButton(self, text="Proxy prüfen", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Prüfe...")
        self.textbox.delete("0.0", "end")
        def worker():
            proxies = urllib.request.getproxies()
            if proxies:
                self.after(0, lambda: self.textbox.insert("end", f"System-Proxy gefunden: {proxies}\n"))
            else:
                self.after(0, lambda: self.textbox.insert("end", "Kein System-Proxy aktiv.\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="Proxy prüfen"))
        threading.Thread(target=worker, daemon=True).start()