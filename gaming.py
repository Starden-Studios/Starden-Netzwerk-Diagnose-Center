import customtkinter as ctk
import threading
import socket
import time

class GamingPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Gaming & Bufferbloat", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        
        self.btn = ctk.CTkButton(self, text="Bufferbloat-Test starten", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def tcp_ping(self, ip="1.1.1.1", port=53):
        try:
            start = time.time()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            s.connect((ip, port))
            s.close()
            return (time.time() - start) * 1000
        except: return None

    def run_test(self):
        self.btn.configure(state="disabled", text="Teste...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Starte Bufferbloat-Test...\n\n")
        
        def worker():
            idle_pings = []
            for _ in range(5):
                p = self.tcp_ping()
                if p: idle_pings.append(p)
            idle_avg = sum(idle_pings)/len(idle_pings) if idle_pings else 0
            
            self.after(0, lambda: self.textbox.insert("end", f"Idle Ping: {idle_avg:.1f} ms\nErzeuge Last...\n"))
            
            # Dummy-Last erzeugen
            for _ in range(5):
                self.tcp_ping("8.8.8.8", 53) 
            
            load_pings = []
            for _ in range(5):
                p = self.tcp_ping()
                if p: load_pings.append(p)
            load_avg = sum(load_pings)/len(load_pings) if load_pings else 0
            
            bloat = load_avg - idle_avg
            
            self.after(0, lambda: self.textbox.insert("end", f"Ping unter Last: {load_avg:.1f} ms\n"))
            self.after(0, lambda: self.textbox.insert("end", f"\nBufferbloat (Differenz): {bloat:.1f} ms\n"))
            
            if bloat > 100:
                self.after(0, lambda: self.textbox.insert("end", "🚨 SCHLECHT: Router hat vollen Buffer.\n"))
            elif bloat > 30:
                self.after(0, lambda: self.textbox.insert("end", "⚠️ OKAY: Leichter Bufferbloat.\n"))
            else:
                self.after(0, lambda: self.textbox.insert("end", "✅ SEHR GUT: Kein Bufferbloat.\n"))
            
            self.after(0, lambda: self.btn.configure(state="normal", text="Bufferbloat-Test starten"))
        
        threading.Thread(target=worker, daemon=True).start()