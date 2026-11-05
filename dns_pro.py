import customtkinter as ctk
import threading
import subprocess

class DnsProPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="DNS Pro (Tiefenanalyse)", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        
        self.btn = ctk.CTkButton(self, text="DNS-Server auflisten", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Lade...")
        self.textbox.delete("0.0", "end")
        
        def worker():
            try:
                out = subprocess.check_output(["ipconfig", "/all"], text=True, encoding="cp850", errors="ignore")
                lines = out.split("\n")
                result = "Konfigurierte DNS-Server:\n"
                for i, line in enumerate(lines):
                    if "DNS-Server" in line or "DNS Servers" in line:
                        result += f"{line.strip()}\n"
                        # Die nächsten Zeilen könnten weitere IPs sein
                        for j in range(1, 3):
                            if i+j < len(lines) and lines[i+j].strip() and ":" not in lines[i+j]:
                                result += f"  {lines[i+j].strip()}\n"
                
                self.after(0, lambda: self.textbox.insert("0.0", result))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("0.0", f"Fehler: {e}"))
            
            self.after(0, lambda: self.btn.configure(state="normal", text="DNS-Server auflisten"))
        
        threading.Thread(target=worker, daemon=True).start()