import customtkinter as ctk
import threading
import subprocess
import platform

class MtuTestPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="MTU-Test (Path Discovery)", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        
        self.btn = ctk.CTkButton(self, text="MTU ermitteln", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Teste...")
        self.textbox.delete("0.0", "end")
        
        def worker():
            target = "8.8.8.8"
            sizes = [1500, 1472, 1400, 1300, 1200, 1000]
            best = 0
            for size in sizes:
                cmd = ["ping", "-f", "-l", str(size), target] if platform.system().lower() == "windows" else ["ping", "-M", "do", "-s", str(size), target]
                startupinfo = None
                if platform.system().lower() == "windows":
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                try:
                    out = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo, timeout=2)
                    if out.returncode == 0:
                        self.after(0, lambda s=size: self.textbox.insert("end", f"Größe {s}: OK\n"))
                        if size > best: best = size
                    else:
                        self.after(0, lambda s=size: self.textbox.insert("end", f"Größe {s}: Zu groß\n"))
                except: pass
            self.after(0, lambda b=best: self.textbox.insert("end", f"\nEmpfohlene MTU: {b+28}\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="MTU ermitteln"))
        threading.Thread(target=worker, daemon=True).start()