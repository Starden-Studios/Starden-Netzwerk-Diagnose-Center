import customtkinter as ctk
import threading
import subprocess

class TcpOptimizerPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="TCP-Optimierer", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        ctk.CTkLabel(self, text="Zeigt und optimiert TCP-Einstellungen (benötigt Admin).", text_color="#aaa").pack(pady=5)
        
        self.btn = ctk.CTkButton(self, text="TCP-Einstellungen anzeigen", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Lade...")
        self.textbox.delete("0.0", "end")
        
        def worker():
            try:
                out = subprocess.check_output(["netsh", "int", "tcp", "show", "global"], text=True, encoding="cp850", errors="ignore")
                self.after(0, lambda: self.textbox.insert("0.0", out))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("0.0", f"Fehler (Admin-Rechte benötigt?): {e}"))
            
            self.after(0, lambda: self.btn.configure(state="normal", text="TCP-Einstellungen anzeigen"))
        
        threading.Thread(target=worker, daemon=True).start()