import customtkinter as ctk
import threading
import subprocess
import platform

class ExternalPingPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Externer Ping", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        self.btn = ctk.CTkButton(self, text="Externe Server anpingen", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Pinge...")
        self.textbox.delete("0.0", "end")
        def worker():
            targets = [("Google", "8.8.8.8"), ("Cloudflare", "1.1.1.1"), ("Quad9", "9.9.9.9")]
            for name, ip in targets:
                cmd = ["ping", "-n", "3", ip] if platform.system().lower() == "windows" else ["ping", "-c", "3", ip]
                try:
                    out = subprocess.check_output(cmd, text=True, encoding="cp850", errors="ignore")
                    self.after(0, lambda n=name, o=out: self.textbox.insert("end", f"--- {n} ({ip}) ---\n{o}\n"))
                except:
                    self.after(0, lambda n=name: self.textbox.insert("end", f"--- {n} --- FEHLER\n\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="Externe Server anpingen"))
        threading.Thread(target=worker, daemon=True).start()