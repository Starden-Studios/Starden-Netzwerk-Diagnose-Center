import customtkinter as ctk
import threading
import socket

class UdpTestPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="UDP-Test", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        self.btn = ctk.CTkButton(self, text="UDP-Paket senden", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        self.btn.configure(state="disabled", text="Sende...")
        self.textbox.delete("0.0", "end")
        def worker():
            try:
                # Wir senden ein UDP-Paket an einen öffentlichen DNS-Server (Port 53)
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.settimeout(2)
                s.sendto(b"TEST", ("8.8.8.8", 53))
                self.after(0, lambda: self.textbox.insert("end", "✅ UDP-Paket erfolgreich gesendet!\n"))
                s.close()
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"❌ UDP-Test fehlgeschlagen: {e}\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="UDP-Paket senden"))
        threading.Thread(target=worker, daemon=True).start()