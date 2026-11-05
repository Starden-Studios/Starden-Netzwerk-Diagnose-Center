import customtkinter as ctk
import threading
import socket

class ReverseDnsPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Reverse DNS", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        self.entry = ctk.CTkEntry(self, placeholder_text="IP (z.B. 8.8.8.8)", width=300)
        self.entry.pack(pady=10)
        self.btn = ctk.CTkButton(self, text="Reverse Lookup", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        ip = self.entry.get() or "8.8.8.8"
        self.btn.configure(state="disabled", text="Suche...")
        self.textbox.delete("0.0", "end")
        def worker():
            try:
                host = socket.gethostbyaddr(ip)
                self.after(0, lambda: self.textbox.insert("end", f"{ip} -> {host[0]}\n"))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="Reverse Lookup"))
        threading.Thread(target=worker, daemon=True).start()