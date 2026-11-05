import customtkinter as ctk
import threading
import subprocess

class IpResetPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="IP-Stack-Reset", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        ctk.CTkLabel(self, text="ACHTUNG: Benötigt Admin-Rechte & Neustart.", text_color="#da3633").pack(pady=5)
        self.btn = ctk.CTkButton(self, text="IP-Stack zurücksetzen", height=40, fg_color="#c0392b", command=self.run_test)
        self.btn.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Reset...")
        self.textbox.delete("0.0", "end")
        def worker():
            try:
                out = subprocess.check_output(["netsh", "int", "ip", "reset"], text=True, encoding="cp850", errors="ignore")
                self.after(0, lambda: self.textbox.insert("end", f"{out}\n✅ Bitte starte den PC neu.\n"))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler (Admin-Rechte?): {e}\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="IP-Stack zurücksetzen"))
        threading.Thread(target=worker, daemon=True).start()