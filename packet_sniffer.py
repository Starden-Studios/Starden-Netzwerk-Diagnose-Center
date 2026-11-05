import customtkinter as ctk
import threading
import time
import subprocess

class PacketSnifferPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Packet Sniffer (Light)", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        
        self.btn = ctk.CTkButton(self, text="Sniffer starten (10s)", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Sniffe...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Starte Sniffer (nutzt Windows 'netstat')...\n\n")
        
        def worker():
            try:
                # Wir nutzen netstat als "Light"-Sniffer
                for i in range(5):
                    out = subprocess.check_output(["netstat", "-n"], text=True, encoding="cp850", errors="ignore")
                    self.after(0, lambda: self.textbox.delete("0.0", "end"))
                    self.after(0, lambda: self.textbox.insert("0.0", out))
                    time.sleep(2)
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("0.0", f"Fehler: {e}"))
            
            self.after(0, lambda: self.btn.configure(state="normal", text="Sniffer starten (10s)"))
        
        threading.Thread(target=worker, daemon=True).start()