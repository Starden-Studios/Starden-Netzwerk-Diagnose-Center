import customtkinter as ctk
import socket
import time
import threading

class RoutingPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        ctk.CTkLabel(self, text="Routing & Internet-Analyse", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        
        self.matrix_frame = ctk.CTkFrame(self, fg_color="#161b22", corner_radius=10)
        self.matrix_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(self.matrix_frame, text="Server-Ping-Matrix (Live & Automatisch):", font=ctk.CTkFont(size=14), text_color="#aaa").pack(pady=(10, 0))
        
        self.matrix_labels = []
        self.targets = [
            ("Router", "192.168.11.1", 80), 
            ("Google", "8.8.8.8", 53), 
            ("Cloudflare", "1.1.1.1", 53)
        ]
        
        for name, ip, port in self.targets:
            frame = ctk.CTkFrame(self.matrix_frame, fg_color="transparent")
            frame.pack(pady=5)
            ctk.CTkLabel(frame, text=f"{name} ({ip}):", width=150, anchor="w", font=ctk.CTkFont(size=14)).pack(side="left")
            lbl = ctk.CTkLabel(frame, text="--- ms", font=ctk.CTkFont(size=14, weight="bold"), text_color="#f1c40f")
            lbl.pack(side="left", padx=10)
            self.matrix_labels.append(lbl)

        self.start_btn = ctk.CTkButton(self, text="Ping-Matrix starten", height=40, command=self.run_matrix)
        self.start_btn.pack(pady=10)
        
        self.dns_btn = ctk.CTkButton(self, text="DNS-Vergleich starten", height=40, command=self.run_dns)
        self.dns_btn.pack(pady=10)
        
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)
        
        self.is_running = False
        self.update_thread = None

    def tcp_ping(self, ip, port):
        try:
            start = time.time()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            s.connect((ip, port))
            s.close()
            return (time.time() - start) * 1000
        except:
            return None

    def run_matrix(self):
        if self.is_running:
            self.is_running = False
            self.start_btn.configure(text="Ping-Matrix starten", fg_color="#1f6aa5")
            self.textbox.insert("end", "\n[Live-Modus gestoppt]\n")
        else:
            self.is_running = True
            self.start_btn.configure(text="Stoppen", fg_color="#da3633")
            self.textbox.insert("end", "\n[Live-Modus gestartet - aktualisiert jede Sekunde]\n")
            self.update_thread = threading.Thread(target=self.live_update_loop, daemon=True)
            self.update_thread.start()

    def live_update_loop(self):
        while self.is_running:
            for i, (name, ip, port) in enumerate(self.targets):
                if not self.is_running: break
                self.after(0, lambda idx=i: self.matrix_labels[idx].configure(text="Messe..."))
                ping_time = self.tcp_ping(ip, port)
                if ping_time is not None:
                    self.after(0, lambda idx=i, t=ping_time: self.matrix_labels[idx].configure(text=f"{t:.1f} ms"))
                else:
                    self.after(0, lambda idx=i: self.matrix_labels[idx].configure(text="Timeout"))
            
            # WICHTIG: Hier auf 1 Sekunde geändert!
            time.sleep(1)

    def run_dns(self):
        self.dns_btn.configure(state="disabled", text="Teste...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Teste DNS-Server (TCP-Latenz)...\n\n")
        
        dns_servers = [
            ("Standard (Router)", "192.168.11.1", 80),
            ("Google DNS", "8.8.8.8", 53),
            ("Cloudflare DNS", "1.1.1.1", 53)
        ]
        
        def dns_worker():
            for name, ip, port in dns_servers:
                ping_time = self.tcp_ping(ip, port)
                if ping_time is not None:
                    self.after(0, lambda n=name, t=ping_time: self.textbox.insert("end", f"{n:<20} | {t:.1f} ms\n"))
                else:
                    self.after(0, lambda n=name: self.textbox.insert("end", f"{n:<20} | Timeout\n"))
            self.after(0, lambda: self.dns_btn.configure(state="normal", text="DNS-Vergleich starten"))
        
        threading.Thread(target=dns_worker, daemon=True).start()

    def on_show(self):
        if not self.is_running:
            self.run_matrix()