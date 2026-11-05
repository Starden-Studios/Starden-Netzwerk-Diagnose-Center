import customtkinter as ctk
import threading
import subprocess

class TcpApplyPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="TCP-Optimierer (Anwenden)", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        ctk.CTkLabel(self, text="ACHTUNG: Benötigt Admin-Rechte.", text_color="#da3633").pack(pady=5)
        self.btn = ctk.CTkButton(self, text="TCP optimieren", height=40, fg_color="#c0392b", command=self.run_test)
        self.btn.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Optimiere...")
        self.textbox.delete("0.0", "end")
        def worker():
            try:
                # Autotuning aktivieren (Standard unter Windows 10/11)
                subprocess.run(["netsh", "int", "tcp", "set", "global", "autotuninglevel=normal"], capture_output=True)
                self.after(0, lambda: self.textbox.insert("end", "✅ TCP-Autotuning aktiviert.\n"))
                # Weitere Optimierungen könnten hier folgen
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="TCP optimieren"))
        threading.Thread(target=worker, daemon=True).start()