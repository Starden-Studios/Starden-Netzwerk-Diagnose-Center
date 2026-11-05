import customtkinter as ctk
import threading
import socket

class PortScannerProPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Port-Scanner Pro", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        
        self.btn = ctk.CTkButton(self, text="Ports im LAN scannen (Port 80)", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Scanne...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Scanne LAN nach offenen Ports (80)...\n")
        
        def worker():
            base_ip = "192.168.11."
            for i in range(1, 20): # Nur die ersten 20, um es schnell zu halten
                ip = f"{base_ip}{i}"
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.1)
                if s.connect_ex((ip, 80)) == 0:
                    self.after(0, lambda x=ip: self.textbox.insert("end", f"  ✅ {x}:80 ist OFFEN\n"))
                s.close()
            
            self.after(0, lambda: self.btn.configure(state="normal", text="Ports im LAN scannen (Port 80)"))
        
        threading.Thread(target=worker, daemon=True).start()