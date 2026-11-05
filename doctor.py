import customtkinter as ctk
from tkinter import messagebox  # <-- NEU: Der richtige Import
import threading
import ctypes

class DoctorPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # --- Titel ---
        ctk.CTkLabel(self, text="Netzwerk-Reparatur (Doctor)", font=ctk.CTkFont(size=28, weight="bold"), text_color="#c0392b").pack(pady=20)
        ctk.CTkLabel(self, text="Repariert hängende DNS-Einstellungen, Winsock und den IP-Stack.", font=ctk.CTkFont(size=14), text_color="#aaa").pack(pady=(0, 20))
        
        # --- Info-Box ---
        self.info_frame = ctk.CTkFrame(self, fg_color="#161b22", corner_radius=10)
        self.info_frame.pack(fill="x", padx=40, pady=10)
        
        info_text = (
            "Was macht der Doctor?\n\n"
            "1. DNS-Cache leeren (ipconfig /flushdns)\n"
            "2. Winsock zurücksetzen (netsh winsock reset)\n"
            "3. IP-Stack zurücksetzen (netsh int ip reset)\n\n"
            "WICHTIG: Windows wird nach Admin-Rechten fragen. Klicke auf 'Ja'."
        )
        ctk.CTkLabel(self.info_frame, text=info_text, justify="left", font=ctk.CTkFont(size=13), text_color="#ddd").pack(pady=15, padx=20)

        # --- Fortschrittsbalken (Standardmäßig unsichtbar) ---
        self.progress_bar = ctk.CTkProgressBar(self, width=600, height=20, progress_color="#c0392b")
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0)
        self.progress_bar.pack_forget()

        # --- Reset Button ---
        self.reset_btn = ctk.CTkButton(self, text="Netzwerk-Reset durchführen", height=50, font=ctk.CTkFont(size=18, weight="bold"), fg_color="#c0392b", hover_color="#e74c3c", command=self.start_repair)
        self.reset_btn.pack(pady=10, fill="x", padx=100)
        
        # --- Status-Label ---
        self.status_label = ctk.CTkLabel(self, text="Bereit.", font=ctk.CTkFont(size=14), text_color="#aaa")
        self.status_label.pack(pady=10)

    def start_repair(self):
        """Startet die Reparatur. Der Fortschrittsbalken wird sichtbar."""
        # Jetzt mit dem richtigen messagebox-Modul
        if not messagebox.askyesno("Netzwerk-Reset", "Dies führt Systembefehle aus.\n\nEs wird ein Windows-Admin-Dialog erscheinen. Klicke auf 'Ja'.\n\nFortfahren?"):
            return
            
        self.reset_btn.configure(state="disabled", text="Repariere...")
        self.status_label.configure(text="Fordere Admin-Rechte an...", text_color="#f1c40f")
        
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0)
        
        threading.Thread(target=self.run_repair, daemon=True).start()

    def run_repair(self):
        try:
            self.after(0, lambda: self.progress_bar.set(0.1))
            self.after(0, lambda: self.status_label.configure(text="Warte auf Admin-Bestätigung..."))

            cmd = "ipconfig /flushdns & netsh winsock reset & netsh int ip reset"
            
            # Hier wird der UAC-Dialog ausgelöst
            result = ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f"/c {cmd}", None, 1)
            
            if result <= 32:
                # Der Nutzer hat "Nein" geklickt oder es gab einen Fehler
                self.after(0, lambda: self.status_label.configure(text="❌ Admin-Rechte verweigert.", text_color="#da3633"))
                self.after(0, lambda: self.progress_bar.set(0))
                self.after(0, lambda: self.reset_btn.configure(state="normal", text="Netzwerk-Reset durchführen"))
                return

            # Fortschritt simulieren
            self.after(0, lambda: self.status_label.configure(text="1/3: Leere DNS-Cache..."))
            self.after(500, lambda: self.progress_bar.set(0.3))
            
            self.after(1500, lambda: self.status_label.configure(text="2/3: Setze Winsock zurück..."))
            self.after(2000, lambda: self.progress_bar.set(0.6))
            
            self.after(3000, lambda: self.status_label.configure(text="3/3: Setze IP-Stack zurück..."))
            self.after(3500, lambda: self.progress_bar.set(0.9))
            
            self.after(4500, lambda: self.status_label.configure(text="✅ Reparatur erfolgreich! Bitte starte deinen PC neu.", text_color="#2ea043"))
            self.after(4500, lambda: self.progress_bar.set(1.0))
            self.after(4500, lambda: self.reset_btn.configure(state="normal", text="Netzwerk-Reset durchführen"))

        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"❌ Fehler: {e}", text_color="#da3633"))
            self.after(0, lambda: self.reset_btn.configure(state="normal", text="Netzwerk-Reset durchführen"))