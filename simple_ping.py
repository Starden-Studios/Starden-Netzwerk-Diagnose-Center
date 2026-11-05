import customtkinter as ctk
import threading
import subprocess
import platform

class SimplePingPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Simple Ping", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        
        self.entry = ctk.CTkEntry(self, placeholder_text="Ziel-IP oder Domain (z.B. 8.8.8.8)", width=300)
        self.entry.pack(pady=10)
        
        self.btn = ctk.CTkButton(self, text="Ping starten", height=40, command=self.run_ping)
        self.btn.pack(pady=10)
        
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_ping(self):
        target = self.entry.get() or "8.8.8.8"
        self.btn.configure(state="disabled", text="Pinge...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", f"Pinge {target}...\n")
        
        def worker():
            try:
                cmd = ["ping", "-n", "4", target] if platform.system().lower() == "windows" else ["ping", "-c", "4", target]
                out = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="cp850", errors="ignore")
                self.after(0, lambda: self.textbox.insert("end", out.stdout))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
            
            self.after(0, lambda: self.btn.configure(state="normal", text="Ping starten"))
        
        threading.Thread(target=worker, daemon=True).start()