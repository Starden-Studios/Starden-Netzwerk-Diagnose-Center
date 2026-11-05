import customtkinter as ctk
import threading
import socket

class Ipv6CheckPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="IPv6-Check", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        self.btn = ctk.CTkButton(self, text="IPv6 testen", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Teste...")
        self.textbox.delete("0.0", "end")
        def worker():
            try:
                # Teste, ob wir eine IPv6-Adresse auflösen können
                info = socket.getaddrinfo("google.com", 80, socket.AF_INET6)
                self.after(0, lambda: self.textbox.insert("end", "✅ IPv6 wird unterstützt!\n\n"))
                for entry in info[:3]:
                    self.after(0, lambda e=entry[4][0]: self.textbox.insert("end", f"IPv6-Adresse: {e}\n"))
            except:
                self.after(0, lambda: self.textbox.insert("end", "❌ IPv6 wird NICHT unterstützt (oder blockiert).\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="IPv6 testen"))
        threading.Thread(target=worker, daemon=True).start()