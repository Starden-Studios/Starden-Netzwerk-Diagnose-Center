import customtkinter as ctk
import threading
import subprocess
import platform

class WlanProPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # --- Titel ---
        ctk.CTkLabel(self, text="WLAN Pro (Kanal & Umgebung)", font=ctk.CTkFont(size=28, weight="bold"), text_color="#88c0ff").pack(pady=10)
        ctk.CTkLabel(self, text="Zeigt alle WLANs in der Umgebung und ihre Kanäle.", font=ctk.CTkFont(size=14), text_color="#aaa").pack(pady=(0, 20))
        
        # --- Button ---
        self.scan_btn = ctk.CTkButton(self, text="Umgebung scannen", height=40, command=self.start_scan_thread)
        self.scan_btn.pack(pady=10)
        
        # --- Textbox für Ausgabe ---
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(fill="both", expand=True, pady=10, padx=20)

    def start_scan_thread(self):
        self.scan_btn.configure(state="disabled", text="Scanne...")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Scanne WLAN-Umgebung via PowerShell (WMI)...\n")
        threading.Thread(target=self.run_scan, daemon=True).start()

    def run_scan(self):
        try:
            if platform.system().lower() != "windows":
                self.after(0, lambda: self.textbox.insert("end", "Nur unter Windows verfügbar.\n"))
                return

            # PowerShell-Befehl, der die WLANs über WMI abfragt
            # Das ist die gleiche Methode, die auch die Windows-Einstellungen nutzen
            ps_script = """
            $wlan = Get-CimInstance -Namespace root\wmi -ClassName MSNdis_80211_BSSIList
            if ($wlan) {
                foreach ($net in $wlan.Ndis80211BSSIList) {
                    $ssid = [System.Text.Encoding]::ASCII.GetString($net.Ndis80211Ssid).Trim([char]0)
                    $signal = $net.Ndis80211Rssi
                    $channel = $net.Ndis80211Configuration[0].Ndis80211DSConfig
                    Write-Output "SSID: $ssid | Signal: $signal dBm | Kanal: $channel"
                }
            } else {
                Write-Output "Keine WLANs gefunden (oder WMI-Schnittstelle blockiert)."
            }
            """
            
            # PowerShell ausführen
            process = subprocess.Popen(
                ["powershell", "-Command", ps_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="cp850",
                errors="ignore"
            )
            stdout, stderr = process.communicate(timeout=15)
            
            # Ausgabe in die Textbox schreiben
            if stdout:
                self.after(0, lambda: self.textbox.delete("0.0", "end"))
                self.after(0, lambda: self.textbox.insert("0.0", stdout))
            else:
                self.after(0, lambda: self.textbox.insert("end", "Keine Antwort vom WMI-Dienst.\n"))
                
        except subprocess.TimeoutExpired:
            self.after(0, lambda: self.textbox.insert("end", "Timeout: WMI antwortet nicht.\n"))
        except Exception as e:
            self.after(0, lambda: self.textbox.insert("end", f"Fehler: {e}\n"))
        finally:
            self.after(0, lambda: self.scan_btn.configure(state="normal", text="Umgebung scannen"))