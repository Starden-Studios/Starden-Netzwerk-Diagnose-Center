import customtkinter as ctk
import threading
import requests

class WhoisCheckPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Whois-Check", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        self.entry = ctk.CTkEntry(self, placeholder_text="Domain (z.B. google.com)", width=300)
        self.entry.pack(pady=10)
        self.btn = ctk.CTkButton(self, text="Whois abrufen", height=40, command=self.run_test)
        self.btn.pack(pady=10)
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def run_test(self):
        domain = self.entry.get() or "google.com"
        self.btn.configure(state="disabled", text="Lade...")
        self.textbox.delete("0.0", "end")
        def worker():
            try:
                # Einfache API (kostenlos, limitiert)
                r = requests.get(f"https://rdap.org/domain/{domain}", timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    self.after(0, lambda: self.textbox.insert("end", f"Domain: {data.get('ldhName', domain)}\n"))
                    events = data.get('events', [])
                    for ev in events:
                        self.after(0, lambda e=ev: self.textbox.insert("end", f"{e.get('eventAction')}: {e.get('eventDate')}\n"))
                else:
                    self.after(0, lambda: self.textbox.insert("end", f"Fehler: Status {r.status_code}\n"))
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
            self.after(0, lambda: self.btn.configure(state="normal", text="Whois abrufen"))
        threading.Thread(target=worker, daemon=True).start()