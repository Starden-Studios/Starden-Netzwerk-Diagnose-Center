import customtkinter as ctk
import threading
import socket

class DnsLookupPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="DNS-Lookup", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        self.entry = ctk.CTkEntry(self, placeholder_text="Domain (z.B. google.com)", width=300)
        self.entry.pack(pady=10)
        self.btn = ctk.CTkButton(self, text="Auflösen", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        domain = self.entry.get() or "google.com"
        self.btn.configure(state="disabled", text="Löse auf...")
        self.textbox.delete("0.0", "end")
        def worker():
            try:
                ip = socket.gethostbyname(domain)
                self.after(0, lambda: self.textbox.insert("end", f"{domain} -> {ip}\n"))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="Auflösen"))
        threading.Thread(target=worker, daemon=True).start()