import customtkinter as ctk
import threading
import time
import psutil

class TrafficAnalyzerPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Traffic-Analyse (NetFlow-Style)", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        
        self.btn = ctk.CTkButton(self, text="Traffic analysieren (10s)", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Analysiere...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Analysiere Traffic pro Protokoll (10s)...\n\n")
        
        def worker():
            start_net = psutil.net_io_counters()
            time.sleep(10)
            end_net = psutil.net_io_counters()
            
            dl = (end_net.bytes_recv - start_net.bytes_recv) / 1024 / 1024
            ul = (end_net.bytes_sent - start_net.bytes_sent) / 1024 / 1024
            
            self.after(0, lambda: self.textbox.insert("end", f"Gesamt-Download: {dl:.2f} MB\n"))
            self.after(0, lambda: self.textbox.insert("end", f"Gesamt-Upload: {ul:.2f} MB\n"))
            
            self.after(0, lambda: self.btn.configure(state="normal", text="Traffic analysieren (10s)"))
        
        threading.Thread(target=worker, daemon=True).start()