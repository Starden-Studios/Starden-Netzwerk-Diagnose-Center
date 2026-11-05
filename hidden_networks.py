import customtkinter as ctk
import threading
import subprocess

class HiddenNetworksPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Versteckte Netzwerke", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        self.btn = ctk.CTkButton(self, text="Nach versteckten WLANs suchen", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Suche...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Suche nach versteckten Netzwerken...\n\n")
        def worker():
            try:
                out = subprocess.check_output(["netsh", "wlan", "show", "networks"], text=True, encoding="cp850", errors="ignore")
                found = False
                for line in out.split("\n"):
                    if "SSID" in line and line.strip().endswith(":"):
                        self.after(0, lambda: self.textbox.insert("end", f"Verstecktes Netzwerk gefunden: {line.strip()}\n"))
                        found = True
                if not found:
                    self.after(0, lambda: self.textbox.insert("end", "Keine versteckten Netzwerke gefunden.\n"))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="Nach versteckten WLANs suchen"))
        threading.Thread(target=worker, daemon=True).start()