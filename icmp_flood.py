import customtkinter as ctk
import threading
import subprocess
import platform
import time

class IcmpFloodPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Ping-Flut (Stresstest)", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        self.btn = ctk.CTkButton(self, text="50 Pings senden", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Sende...")
        self.textbox.delete("0.0", "end")
        def worker():
            target = "8.8.8.8"
            for i in range(50):
                cmd = ["ping", "-n", "1", "-w", "1000", target] if platform.system().lower() == "windows" else ["ping", "-c", "1", "-W", "1", target]
                startupinfo = None
                if platform.system().lower() == "windows":
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                try:
                    start = time.time()
                    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, startupinfo=startupinfo, timeout=2)
                    latency = (time.time() - start) * 1000
                    self.after(0, lambda i=i+1, l=latency: self.textbox.insert("end", f"Ping {i}: {l:.1f} ms\n"))
                except:
                    self.after(0, lambda i=i+1: self.textbox.insert("end", f"Ping {i}: Timeout\n"))
                self.after(0, lambda: self.textbox.see("end"))
            self.after(0, lambda: self.btn.configure(state="normal", text="50 Pings senden"))
        threading.Thread(target=worker, daemon=True).start()