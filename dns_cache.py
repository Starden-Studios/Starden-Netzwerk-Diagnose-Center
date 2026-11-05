import customtkinter as ctk
import threading
import subprocess

class DnsCachePage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="DNS-Cache leeren", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        self.btn = ctk.CTkButton(self, text="Cache leeren", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Leere...")
        self.textbox.delete("0.0", "end")
        def worker():
            try:
                out = subprocess.check_output(["ipconfig", "/flushdns"], text=True, encoding="cp850", errors="ignore")
                self.after(0, lambda: self.textbox.insert("end", f"✅ {out}\n"))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="Cache leeren"))
        threading.Thread(target=worker, daemon=True).start()