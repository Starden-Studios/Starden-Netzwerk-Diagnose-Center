import customtkinter as ctk
import threading
import time
import socket
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class LatencyTrendPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        ctk.CTkLabel(self, text="Jitter-Trend (Live-Graph)", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        
        self.btn = ctk.CTkButton(self, text="Live-Trend starten", height=40, command=self.start_trend)
        self.btn.pack(pady=10)
        
        plt.style.use('dark_background')
        self.fig = Figure(figsize=(10, 3), dpi=100, facecolor='#161b22')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#161b22')
        self.ax.tick_params(colors='white')
        self.ax.grid(True, color='#333333')
        self.line, = self.ax.plot([], [], color='#88c0ff', linewidth=2)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, pady=10, padx=20)
        
        self.data = []
        self.running = False

    def tcp_ping(self, ip="1.1.1.1", port=53):
        try:
            start = time.time()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            s.connect((ip, port))
            s.close()
            return (time.time() - start) * 1000
        except: return 0

    def start_trend(self):
        if self.running:
            self.running = False
            self.btn.configure(text="Live-Trend starten")
            return
        
        self.running = True
        self.btn.configure(text="Stoppen")
        self.data.clear()
        threading.Thread(target=self.update_loop, daemon=True).start()

    def update_loop(self):
        while self.running:
            p = self.tcp_ping()
            self.data.append(p)
            if len(self.data) > 20: self.data.pop(0)
            
            times = list(range(len(self.data)))
            self.line.set_data(times, self.data)
            self.ax.relim()
            self.ax.autoscale_view()
            self.ax.set_xlim(0, 20)
            self.canvas.draw()
            
            time.sleep(1)