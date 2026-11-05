import customtkinter as ctk
import threading
import time
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Cloudflare Endpunkte
PING_URL = "https://speed.cloudflare.com/__down?bytes=100"
DOWNLOAD_URL = "https://speed.cloudflare.com/__down?bytes=25000000"
UPLOAD_URL = "https://speed.cloudflare.com/__up"

class SpeedPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.is_testing = False
        self.live_data = []
        self.result_ping = 0
        self.result_jitter = 0
        self.result_download = 0
        self.result_upload = 0
        
        # --- Titel ---
        ctk.CTkLabel(self, text="Speed & Traffic", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        
        # --- Große Live-Anzeige ---
        self.live_speed_label = ctk.CTkLabel(self, text="0.00 Mbit/s", font=ctk.CTkFont(size=64, weight="bold"), text_color="#2ea043")
        self.live_speed_label.pack(pady=10)

        # --- Stat-Boxen ---
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(pady=10, fill="x")
        
        self.box_ping = self.create_stat_box(self.stats_frame, "Ping / Jitter", "--- ms", 0, "#f85149")
        self.box_dl = self.create_stat_box(self.stats_frame, "Download", "--- Mbit/s", 1, "#2ea043")
        self.box_ul = self.create_stat_box(self.stats_frame, "Upload", "--- Mbit/s", 2, "#f1c40f")
        self.box_score = self.create_stat_box(self.stats_frame, "Gaming-Score", "--- / 10", 3, "#9b59b6")

        # --- Diagramm ---
        self.chart_frame = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=10)
        self.chart_frame.pack(fill="both", expand=True, pady=10)
        
        plt.style.use('dark_background')
        self.fig = Figure(figsize=(10, 3), dpi=100, facecolor='#0d1117')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#0d1117')
        self.ax.tick_params(colors='white')
        self.ax.grid(True, color='#333333')
        self.line, = self.ax.plot([], [], color='#88c0ff', linewidth=2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # --- Start Button ---
        self.start_btn = ctk.CTkButton(self, text="Test starten", height=50, font=ctk.CTkFont(size=18, weight="bold"), command=self.start_test_thread)
        self.start_btn.pack(pady=10, fill="x")

    def create_stat_box(self, parent, title, value, col, color):
        frame = ctk.CTkFrame(parent, fg_color="#161b22", corner_radius=10, border_width=1, border_color="#333")
        frame.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)
        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=12), text_color="#aaa").pack(pady=(10, 0))
        lbl = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=18, weight="bold"), text_color=color)
        lbl.pack(pady=(0, 10))
        return lbl

    def start_test_thread(self):
        if self.is_testing: return
        self.is_testing = True
        self.start_btn.configure(state="disabled", text="Test läuft...")
        self.live_speed_label.configure(text="0.00 Mbit/s", text_color="#2ea043")
        self.live_data.clear()
        self.ax.clear()
        self.line, = self.ax.plot([], [], color='#88c0ff', linewidth=2)
        self.canvas.draw()
        
        threading.Thread(target=self.run_full_test, daemon=True).start()

    def measure_ping(self):
        pings = []
        for _ in range(10):
            start = time.time()
            try:
                r = requests.get(PING_URL, timeout=2.0)
                if r.status_code == 200: pings.append((time.time() - start) * 1000)
            except: pass
        if not pings: return 0, 0
        avg = sum(pings) / len(pings)
        jitter = sum([abs(pings[i] - pings[i-1]) for i in range(1, len(pings))]) / (len(pings)-1) if len(pings) > 1 else 0
        return avg, jitter

    def measure_download(self):
        start = time.time()
        last_update = start
        last_bytes = 0
        total = 0
        interval = []
        try:
            with requests.get(DOWNLOAD_URL, stream=True, timeout=15) as r:
                for chunk in r.iter_content(chunk_size=32768):
                    if not self.is_testing: break
                    total += len(chunk)
                    now = time.time()
                    if now - last_update >= 0.2:
                        speed = ((total - last_bytes) * 8) / ((now - last_update) * 1_000_000)
                        interval.append(speed)
                        self.live_data.append((now - start, speed))
                        # GUI Update im Haupt-Thread
                        self.after(0, lambda s=speed, e=now-start: self.update_gui_live(s, e))
                        last_update = now
                        last_bytes = total
                        if now - start > 8: break
        except: pass
        return sum(interval) / len(interval) if interval else 0

    def measure_upload(self):
        daten = b"0" * (5 * 1024 * 1024)
        self.ax.clear()
        self.line, = self.ax.plot([], [], color='#f1c40f', linewidth=2)
        start = time.time()
        try:
            requests.post(UPLOAD_URL, data=daten, timeout=20)
            return (len(daten) * 8) / ((time.time() - start) * 1_000_000)
        except: return 0

    def update_gui_live(self, speed, elapsed):
        self.live_speed_label.configure(text=f"{speed:.2f} Mbit/s")
        times = [d[0] for d in self.live_data]
        speeds = [d[1] for d in self.live_data]
        self.line.set_data(times, speeds)
        self.ax.relim()
        self.ax.autoscale_view()
        if times: self.ax.set_xlim(0, max(times) + 1)
        self.canvas.draw()

    def run_full_test(self):
        try:
            # 1. Ping
            self.result_ping, self.result_jitter = self.measure_ping()
            self.after(0, lambda: self.box_ping.configure(text=f"{self.result_ping:.1f} / {self.result_jitter:.1f} ms"))
            
            # 2. Download
            self.after(0, lambda: self.live_speed_label.configure(text_color="#2ea043"))
            self.result_download = self.measure_download()
            self.after(0, lambda: self.box_dl.configure(text=f"{self.result_download:.2f} Mbit/s"))
            
            # 3. Upload
            self.after(0, lambda: self.live_speed_label.configure(text_color="#f1c40f"))
            self.result_upload = self.measure_upload()
            self.after(0, lambda: self.box_ul.configure(text=f"{self.result_upload:.2f} Mbit/s"))
            
            # 4. Score
            score = max(1, round(10 - (self.result_ping/20) - (self.result_jitter/5), 1))
            self.after(0, lambda: self.box_score.configure(text=f"{score} / 10"))
            
            self.after(0, self.finish_test)
        except Exception as e:
            self.after(0, lambda: self.show_error(str(e)))

    def finish_test(self):
        self.is_testing = False
        self.start_btn.configure(state="normal", text="Test erneut starten")
        self.live_speed_label.configure(text="Fertig", text_color="#fff")

    def show_error(self, msg):
        self.is_testing = False
        self.start_btn.configure(state="normal", text="Test starten")
        print(f"Fehler: {msg}")