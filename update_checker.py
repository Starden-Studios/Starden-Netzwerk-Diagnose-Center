import customtkinter as ctk
import requests
import webbrowser
import threading
import tkinter.messagebox as messagebox
from packaging import version

# ================= KONFIGURATION =================
# DEINE AKTUELLE VERSION (muss mit dem Installer übereinstimmen)
CURRENT_VERSION = "1.5"

# URL zur Textdatei mit der neuesten Version 
# (Platzhalter: Ersetze dies später durch deine eigene URL)
UPDATE_URL = "https://raw.githubusercontent.com/Starden-NDC/version/main/version.txt"

class UpdateChecker(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#161b22", corner_radius=10)
        
        self.label = ctk.CTkLabel(self, text="Update-Status: Unbekannt", font=ctk.CTkFont(size=14), text_color="#aaa")
        self.label.pack(pady=(10, 5))
        
        self.btn = ctk.CTkButton(self, text="Nach Updates suchen", height=30, command=self.start_update_check)
        self.btn.pack(pady=(0, 10))

    def start_update_check(self):
        self.btn.configure(state="disabled", text="Suche...")
        self.label.configure(text="Suche nach Updates...", text_color="#f1c40f")
        threading.Thread(target=self.check_for_updates, daemon=True).start()

    def check_for_updates(self):
        try:
            # 1. Neueste Version vom Server holen
            response = requests.get(UPDATE_URL, timeout=5)
            response.raise_for_status()
            latest_version = response.text.strip()
            
            # 2. Versionen vergleichen
            if version.parse(latest_version) > version.parse(CURRENT_VERSION):
                self.after(0, lambda: self.show_update_available(latest_version))
            else:
                self.after(0, lambda: self.show_up_to_date())
                
        except Exception as e:
            self.after(0, lambda: self.show_error(str(e)))

    def show_update_available(self, latest_version):
        self.btn.configure(state="normal", text="Update verfügbar!")
        self.btn.configure(fg_color="#2ea043") # Grün
        self.label.configure(text=f"Neue Version: {latest_version} (Du hast {CURRENT_VERSION})", text_color="#2ea043")
        
        answer = messagebox.askyesno(
            "Update verfügbar",
            f"Eine neue Version ({latest_version}) ist verfügbar!\n"
            f"Deine Version: {CURRENT_VERSION}\n\n"
            "Möchtest du zur Download-Seite?"
        )
        if answer:
            webbrowser.open("https://github.com/Starden-NDC/releases")

    def show_up_to_date(self):
        self.btn.configure(state="normal", text="Nach Updates suchen")
        self.btn.configure(fg_color="#1f6aa5") # Blau
        self.label.configure(text=f"Deine Version ({CURRENT_VERSION}) ist aktuell.", text_color="#2ea043")

    def show_error(self, error_msg):
        self.btn.configure(state="normal", text="Nach Updates suchen")
        self.btn.configure(fg_color="#da3633") # Rot
        self.label.configure(text=f"Update-Check fehlgeschlagen (Offline?)", text_color="#da3633")
        print(f"Update-Fehler: {error_msg}")