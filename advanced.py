import customtkinter as ctk
import threading
import subprocess
import platform
import time
import requests

class AdvancedPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # --- Titel ---
        ctk.CTkLabel(self, text="Advanced Routing-Labor", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        
        # --- Button-Leiste ---
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=10)
        
        self.ttfb_btn = ctk.CTkButton(self.btn_frame, text="TTFB-Messung", width=200, command=self.run_ttfb)
        self.ttfb_btn.pack(side="left", padx=10)
        
        self.mtu_btn = ctk.CTkButton(self.btn_frame, text="Path MTU Discovery", width=200, command=self.run_mtu)
        self.mtu_btn.pack(side="left", padx=10)
        
        self.hop_btn = ctk.CTkButton(self.btn_frame, text="Hop-Health (Traceroute)", width=200, command=self.run_hop_health)
        self.hop_btn.pack(side="left", padx=10)

        # --- Textbox für Ausgabe ---
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    # ================= TTFB =================
    def run_ttfb(self):
        self.ttfb_btn.configure(state="disabled", text="Messe...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Messe Time to First Byte (TTFB) für Webseiten...\n\n")
        
        def worker():
            sites = [
                ("Google", "https://google.com"),
                ("YouTube", "https://youtube.com"),
                ("Cloudflare", "https://cloudflare.com"),
                ("Wikipedia", "https://wikipedia.org")
            ]
            
            for name, url in sites:
                try:
                    start = time.time()
                    r = requests.get(url, timeout=5)
                    ttfb = (time.time() - start) * 1000
                    self.after(0, lambda n=name, t=ttfb: self.textbox.insert("end", f"{n:<15} | {t:.1f} ms\n"))
                except:
                    self.after(0, lambda n=name: self.textbox.insert("end", f"{n:<15} | Fehler\n"))
            
            self.after(0, lambda: self.ttfb_btn.configure(state="normal", text="TTFB-Messung"))
        
        threading.Thread(target=worker, daemon=True).start()

    # ================= MTU =================
    def run_mtu(self):
        self.mtu_btn.configure(state="disabled", text="Teste...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Ermittle optimale MTU-Größe (Ping mit 'Don't Fragment')...\n\n")
        
        def worker():
            target = "8.8.8.8"
            sizes = [1500, 1472, 1400, 1300, 1200, 1100, 1000]
            best_mtu = 0
            
            for size in sizes:
                try:
                    cmd = ["ping", "-f", "-l", str(size), target] if platform.system().lower() == "windows" else ["ping", "-M", "do", "-s", str(size), target]
                    startupinfo = None
                    if platform.system().lower() == "windows":
                        startupinfo = subprocess.STARTUPINFO()
                        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    
                    out = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo, timeout=2)
                    
                    if out.returncode == 0:
                        self.after(0, lambda s=size: self.textbox.insert("end", f"Größe {s}: OK ✅\n"))
                        if size > best_mtu: best_mtu = size
                    else:
                        self.after(0, lambda s=size: self.textbox.insert("end", f"Größe {s}: Zu groß ❌\n"))
                except:
                    pass
            
            if best_mtu == 0:
                self.after(0, lambda: self.textbox.insert("end", "\n❌ MTU-Test fehlgeschlagen.\n"))
            else:
                self.after(0, lambda b=best_mtu: self.textbox.insert("end", f"\nEmpfohlene MTU: {b} (bzw. {b+28} inkl. Header)\n"))
            
            self.after(0, lambda: self.mtu_btn.configure(state="normal", text="Path MTU Discovery"))
        
        threading.Thread(target=worker, daemon=True).start()

    # ================= HOP-HEALTH =================
    def run_hop_health(self):
        self.hop_btn.configure(state="disabled", text="Trace...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Führe Traceroute aus (Hop-Health)...\n\n")
        
        def worker():
            try:
                target = "1.1.1.1"
                cmd = ["tracert", "-h", "15", "-w", "1000", target] if platform.system().lower() == "windows" else ["traceroute", "-m", "15", "-w", "1", target]
                
                startupinfo = None
                if platform.system().lower() == "windows":
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                
                # Wir starten den Prozess und lesen die Ausgabe live
                process = subprocess.Popen(
                    cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    text=True, 
                    bufsize=1, 
                    startupinfo=startupinfo,
                    encoding="cp850",
                    errors="ignore"
                )
                
                # Zeile für Zeile lesen und sofort anzeigen
                for line in process.stdout:
                    self.after(0, lambda l=line: self.textbox.insert("end", l))
                    self.after(0, lambda: self.textbox.see("end")) # Automatisch scrollen
                
                process.wait()
                
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
            
            self.after(0, lambda: self.hop_btn.configure(state="normal", text="Hop-Health (Traceroute)"))
        
        threading.Thread(target=worker, daemon=True).start()