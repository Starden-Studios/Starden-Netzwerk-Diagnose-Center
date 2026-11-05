import customtkinter as ctk
import threading
import socket

class PortScanLocalPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Ports am eigenen PC", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        self.btn = ctk.CTkButton(self, text="PC scannen", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Scanne...")
        self.textbox.delete("0.0", "end")
        def worker():
            self.after(0, lambda: self.textbox.insert("end", "Scanne localhost (127.0.0.1)...\n\n"))
            for port in [21, 22, 23, 80, 443, 3306, 8080]:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.1)
                if s.connect_ex(("127.0.0.1", port)) == 0:
                    self.after(0, lambda p=port: self.textbox.insert("end", f"  ✅ Port {p}: OFFEN\n"))
                s.close()
            self.after(0, lambda: self.btn.configure(state="normal", text="PC scannen"))
        threading.Thread(target=worker, daemon=True).start()