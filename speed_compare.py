import customtkinter as ctk
import threading
import time
import requests

class SpeedComparePage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Speed-Vergleich", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        
        self.btn = ctk.CTkButton(self, text="Vergleich starten (3x 5s)", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Messe...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Messe Download 3 Mal (je 5 Sekunden)...\n\n")
        
        def worker():
            for i in range(3):
                try:
                    start = time.time()
                    total = 0
                    with requests.get("https://speed.cloudflare.com/__down?bytes=10000000", stream=True, timeout=10) as r:
                        for chunk in r.iter_content(chunk_size=32768):
                            total += len(chunk)
                            if time.time() - start > 5: break
                    speed = (total * 8) / ((time.time() - start) * 1_000_000)
                    self.after(0, lambda i=i+1, s=speed: self.textbox.insert("end", f"Durchlauf {i}: {s:.2f} Mbit/s\n"))
                except Exception as e:
                    self.after(0, lambda: self.textbox.insert("end", f"Fehler im Durchlauf\n"))
            
            self.after(0, lambda: self.textbox.insert("end", "\nVergleich abgeschlossen.\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="Vergleich starten (3x 5s)"))
        
        threading.Thread(target=worker, daemon=True).start()