import customtkinter as ctk
import threading
import subprocess
import platform

class ExperimentalPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Experimentell (NetFlow / Mesh)", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        
        self.btn = ctk.CTkButton(self, text="Mesh/Netzwerk-Scan", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Scanne...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Suche nach Mesh-Knoten & Netzwerk-Topologie...\n")
        
        def worker():
            # Einfacher Ansatz: Wir schauen uns die ARP-Tabelle an
            try:
                out = subprocess.check_output(["arp", "-a"], text=True, encoding="cp850", errors="ignore")
                self.after(0, lambda: self.textbox.insert("end", "\nGefundene Geräte (ARP):\n"))
                self.after(0, lambda: self.textbox.insert("end", out))
            except:
                self.after(0, lambda: self.textbox.insert("end", "Fehler beim ARP-Scan.\n"))
            
            self.after(0, lambda: self.btn.configure(state="normal", text="Mesh/Netzwerk-Scan"))
        
        threading.Thread(target=worker, daemon=True).start()