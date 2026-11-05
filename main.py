import customtkinter as ctk
import sys
import os
import ctypes

# ================= ADMIN-RECHTE CHECK =================
def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

if not is_admin():
    print("WARNUNG: Bitte starte das Programm über die 'start_admin.bat' Datei für volle Funktionen.")

# ================= IMPORTS =================
from dashboard import DashboardPage
from speed import SpeedPage
from scanner import ScannerPage
from wlan_pro import WlanProPage
from wlan_security import WlanSecurityPage
from hidden_networks import HiddenNetworksPage
from bssid_tracker import BssidTrackerPage
from driver_check import DriverCheckPage
from routing import RoutingPage
from advanced import AdvancedPage
from latency_trend import LatencyTrendPage
from simple_ping import SimplePingPage
from mtu_test import MtuTestPage
from public_ip import PublicIpPage
from geo_ip import GeoIpPage
from gateway_ping import GatewayPingPage
from external_ping import ExternalPingPage
from dns_lookup import DnsLookupPage
from reverse_dns import ReverseDnsPage
from whois_check import WhoisCheckPage
from http_check import HttpCheckPage
from ipv6_check import Ipv6CheckPage
from security import SecurityPage
from security_pro import SecurityProPage
from dns_pro import DnsProPage
from dns_leak import DnsLeakPage
from port_scanner_pro import PortScannerProPage
from port_scan_local import PortScanLocalPage
from firewall_check import FirewallCheckPage
from proxy_check import ProxyCheckPage
from vpn_check import VpnCheckPage
from icmp_flood import IcmpFloodPage
from udp_test import UdpTestPage
from netstat_viewer import NetstatViewerPage
from packet_sniffer import PacketSnifferPage
from packet_sniffer_pro import PacketSnifferProPage
from netflow import NetflowPage
from mesh_scanner import MeshScannerPage
from network_tools import NetworkToolsPage
from monitoring import MonitoringPage
from monitoring_pro import MonitoringProPage
from gaming import GamingPage
from system_info import SystemInfoPage
from experimental import ExperimentalPage
from bluetooth_scanner import BluetoothScannerPage
from speed_compare import SpeedComparePage
from speedtest_servers import SpeedtestServersPage
from tcp_optimizer import TcpOptimizerPage
from tcp_apply import TcpApplyPage
from traffic_analyzer import TrafficAnalyzerPage
from doctor import DoctorPage
from dns_cache import DnsCachePage
from winsock_reset import WinsockResetPage
from ip_reset import IpResetPage
from netsh_reset import NetshResetPage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Starden Netzwerk Diagnose Center")
        self.geometry("1400x950")
        self.resizable(True, True)

        # ================= FENSTER-ICON SETZEN (ENDGÜLTIGER FIX) =================
        
        # 1. Zwingt Windows, die App als eigenständig zu erkennen (wichtig für Taskleiste)
        try:
            myappid = 'starden.ndc.diagnose.1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

        # 2. Findet den Pfad zum Icon (funktioniert in der .exe und im Skript)
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
            
        icon_path = os.path.join(application_path, "stardenlogo.ico")
        
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
        
        # ========================================================================

        self.setup_layout()
        self.show_page_dashboard()

    def setup_layout(self):
        self.sidebar = ctk.CTkScrollableFrame(self, width=280, corner_radius=0, fg_color="#161b22")
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="STARDEN", font=ctk.CTkFont(size=24, weight="bold"), text_color="#88c0ff").pack(pady=(20, 5))
        ctk.CTkLabel(self.sidebar, text="Diagnose Center", font=ctk.CTkFont(size=12), text_color="#aaa").pack(pady=(0, 20))

        self.add_category("📊 Übersicht", [
            ("🏠 Dashboard", self.show_page_dashboard),
            ("📈 Speed & Traffic", self.show_page_speed),
        ])
        self.add_category("📡 WLAN & Funk", [
            ("📶 WLAN & Signal", self.show_page_scanner),
            ("📡 WLAN Pro", self.show_page_wlan_pro),
            ("🔒 WLAN-Sicherheit", self.show_page_wlan_security),
            ("👻 Versteckte Netze", self.show_page_hidden_networks),
            ("📡 BSSID-Tracker", self.show_page_bssid_tracker),
            ("⚙️ Treiber-Check", self.show_page_driver_check),
        ])
        self.add_category("🌐 Routing & Internet", [
            ("🌐 Routing Live", self.show_page_routing),
            ("🧪 Advanced Routing", self.show_page_advanced),
            ("📉 Jitter-Trend", self.show_page_latency_trend),
            ("📡 Simple Ping", self.show_page_simple_ping),
            ("📏 MTU-Test", self.show_page_mtu),
            ("🌍 Public IP", self.show_page_public_ip),
            ("📍 Geo-IP", self.show_page_geo_ip),
            ("🏠 Gateway-Ping", self.show_page_gateway_ping),
            ("🌍 Externer Ping", self.show_page_external_ping),
            ("📜 DNS-Lookup", self.show_page_dns_lookup),
            ("🔙 Reverse DNS", self.show_page_reverse_dns),
            ("📋 Whois-Check", self.show_page_whois),
            ("🌐 HTTP-Check", self.show_page_http_check),
            ("📡 IPv6-Check", self.show_page_ipv6_check),
        ])
        self.add_category("🛡️ Sicherheit", [
            ("🛡️ Sicherheit", self.show_page_security),
            ("🔒 Security Pro", self.show_page_security_pro),
            ("📜 DNS Pro", self.show_page_dns_pro),
            ("🔍 DNS-Leak", self.show_page_dns_leak),
            ("🚪 Port-Scanner Pro", self.show_page_port_scanner_pro),
            ("💻 Ports am PC", self.show_page_port_scan_local),
            ("🔥 Firewall-Check", self.show_page_firewall),
            ("🌐 Proxy-Check", self.show_page_proxy),
            ("🔒 VPN-Check", self.show_page_vpn),
            ("🌊 ICMP-Flut", self.show_page_icmp_flood),
            ("📡 UDP-Test", self.show_page_udp_test),
            ("📊 Netstat-Viewer", self.show_page_netstat),
            ("📦 Packet Sniffer Pro", self.show_page_packet_sniffer_pro),
            ("📊 NetFlow", self.show_page_netflow),
        ])
        self.add_category("🛠️ Analyse & Tools", [
            ("🛠️ Network Tools", self.show_page_tools),
            ("📈 Monitoring", self.show_page_monitoring),
            ("⏱️ Monitoring Pro", self.show_page_monitoring_pro),
            ("🎮 Gaming & Bufferbloat", self.show_page_gaming),
            ("🌍 System Info", self.show_page_system_info),
            ("🧪 Experimental", self.show_page_experimental),
            ("📦 Packet Sniffer", self.show_page_packet_sniffer),
            ("📶 Bluetooth-Scanner", self.show_page_bluetooth),
            ("⚖️ Speed-Vergleich", self.show_page_speed_compare),
            ("🚀 Speedtest-Server", self.show_page_speedtest_servers),
            ("⚙️ TCP-Optimierer", self.show_page_tcp_optimizer),
            ("🛠️ TCP anwenden", self.show_page_tcp_apply),
            ("📊 Traffic-Analyse", self.show_page_traffic_analyzer),
            ("🔗 Mesh-Scanner", self.show_page_mesh_scanner),
        ])
        self.add_category("⚙️ System & Reset", [
            ("🛠️ Doctor (Reset)", self.show_page_doctor),
            ("📜 DNS-Cache leeren", self.show_page_dns_cache),
            ("🔌 Winsock-Reset", self.show_page_winsock),
            ("🌐 IP-Stack-Reset", self.show_page_ip_reset),
            ("💥 Kompletter Reset", self.show_page_netsh_reset),
        ])

        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.pages = {}
        self.pages["dashboard"] = DashboardPage(self.main, fg_color="transparent")
        self.pages["speed"] = SpeedPage(self.main, fg_color="transparent")
        self.pages["scanner"] = ScannerPage(self.main, fg_color="transparent")
        self.pages["wlan_pro"] = WlanProPage(self.main, fg_color="transparent")
        self.pages["wlan_security"] = WlanSecurityPage(self.main, fg_color="transparent")
        self.pages["hidden_networks"] = HiddenNetworksPage(self.main, fg_color="transparent")
        self.pages["bssid_tracker"] = BssidTrackerPage(self.main, fg_color="transparent")
        self.pages["driver_check"] = DriverCheckPage(self.main, fg_color="transparent")
        self.pages["routing"] = RoutingPage(self.main, fg_color="transparent")
        self.pages["advanced"] = AdvancedPage(self.main, fg_color="transparent")
        self.pages["latency_trend"] = LatencyTrendPage(self.main, fg_color="transparent")
        self.pages["simple_ping"] = SimplePingPage(self.main, fg_color="transparent")
        self.pages["mtu"] = MtuTestPage(self.main, fg_color="transparent")
        self.pages["public_ip"] = PublicIpPage(self.main, fg_color="transparent")
        self.pages["geo_ip"] = GeoIpPage(self.main, fg_color="transparent")
        self.pages["gateway_ping"] = GatewayPingPage(self.main, fg_color="transparent")
        self.pages["external_ping"] = ExternalPingPage(self.main, fg_color="transparent")
        self.pages["dns_lookup"] = DnsLookupPage(self.main, fg_color="transparent")
        self.pages["reverse_dns"] = ReverseDnsPage(self.main, fg_color="transparent")
        self.pages["whois"] = WhoisCheckPage(self.main, fg_color="transparent")
        self.pages["http_check"] = HttpCheckPage(self.main, fg_color="transparent")
        self.pages["ipv6_check"] = Ipv6CheckPage(self.main, fg_color="transparent")
        self.pages["security"] = SecurityPage(self.main, fg_color="transparent")
        self.pages["security_pro"] = SecurityProPage(self.main, fg_color="transparent")
        self.pages["dns_pro"] = DnsProPage(self.main, fg_color="transparent")
        self.pages["dns_leak"] = DnsLeakPage(self.main, fg_color="transparent")
        self.pages["port_scanner_pro"] = PortScannerProPage(self.main, fg_color="transparent")
        self.pages["port_scan_local"] = PortScanLocalPage(self.main, fg_color="transparent")
        self.pages["firewall"] = FirewallCheckPage(self.main, fg_color="transparent")
        self.pages["proxy"] = ProxyCheckPage(self.main, fg_color="transparent")
        self.pages["vpn"] = VpnCheckPage(self.main, fg_color="transparent")
        self.pages["icmp_flood"] = IcmpFloodPage(self.main, fg_color="transparent")
        self.pages["udp_test"] = UdpTestPage(self.main, fg_color="transparent")
        self.pages["netstat"] = NetstatViewerPage(self.main, fg_color="transparent")
        self.pages["packet_sniffer_pro"] = PacketSnifferProPage(self.main, fg_color="transparent")
        self.pages["netflow"] = NetflowPage(self.main, fg_color="transparent")
        self.pages["tools"] = NetworkToolsPage(self.main, fg_color="transparent")
        self.pages["monitoring"] = MonitoringPage(self.main, fg_color="transparent")
        self.pages["monitoring_pro"] = MonitoringProPage(self.main, fg_color="transparent")
        self.pages["gaming"] = GamingPage(self.main, fg_color="transparent")
        self.pages["system_info"] = SystemInfoPage(self.main, fg_color="transparent")
        self.pages["experimental"] = ExperimentalPage(self.main, fg_color="transparent")
        self.pages["packet_sniffer"] = PacketSnifferPage(self.main, fg_color="transparent")
        self.pages["bluetooth"] = BluetoothScannerPage(self.main, fg_color="transparent")
        self.pages["speed_compare"] = SpeedComparePage(self.main, fg_color="transparent")
        self.pages["speedtest_servers"] = SpeedtestServersPage(self.main, fg_color="transparent")
        self.pages["tcp_optimizer"] = TcpOptimizerPage(self.main, fg_color="transparent")
        self.pages["tcp_apply"] = TcpApplyPage(self.main, fg_color="transparent")
        self.pages["traffic_analyzer"] = TrafficAnalyzerPage(self.main, fg_color="transparent")
        self.pages["mesh_scanner"] = MeshScannerPage(self.main, fg_color="transparent")
        self.pages["doctor"] = DoctorPage(self.main, fg_color="transparent")
        self.pages["dns_cache"] = DnsCachePage(self.main, fg_color="transparent")
        self.pages["winsock"] = WinsockResetPage(self.main, fg_color="transparent")
        self.pages["ip_reset"] = IpResetPage(self.main, fg_color="transparent")
        self.pages["netsh_reset"] = NetshResetPage(self.main, fg_color="transparent")

    def add_category(self, title, buttons):
        category_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        category_frame.pack(fill="x", pady=2)
        header_btn = ctk.CTkButton(category_frame, text=f"▼ {title}", fg_color="transparent", text_color="#88c0ff", hover_color="#2c3e50", anchor="w", height=30, font=ctk.CTkFont(size=13, weight="bold"))
        header_btn.pack(fill="x", padx=5)
        content_frame = ctk.CTkFrame(category_frame, fg_color="#0d1117", corner_radius=5)
        content_frame.pack(fill="x", padx=5, pady=(2, 5))
        for text, command in buttons:
            btn = ctk.CTkButton(content_frame, text=text, fg_color="transparent", text_color="#ddd", hover_color="#1f242c", anchor="w", height=30, command=command)
            btn.pack(fill="x", padx=2, pady=1)
        def toggle():
            if content_frame.winfo_viewable():
                content_frame.pack_forget()
                header_btn.configure(text=f"▶ {title}")
            else:
                content_frame.pack(fill="x", padx=5, pady=(2, 5))
                header_btn.configure(text=f"▼ {title}")
        header_btn.configure(command=toggle)

    def hide_all(self):
        for frame in self.pages.values():
            frame.pack_forget()

    # --- Navigation (Alle Seiten) ---
    def show_page_dashboard(self): self.hide_all(); self.pages["dashboard"].pack(fill="both", expand=True)
    def show_page_speed(self): self.hide_all(); self.pages["speed"].pack(fill="both", expand=True)
    def show_page_scanner(self): self.hide_all(); self.pages["scanner"].pack(fill="both", expand=True)
    def show_page_wlan_pro(self): self.hide_all(); self.pages["wlan_pro"].pack(fill="both", expand=True)
    def show_page_wlan_security(self): self.hide_all(); self.pages["wlan_security"].pack(fill="both", expand=True)
    def show_page_hidden_networks(self): self.hide_all(); self.pages["hidden_networks"].pack(fill="both", expand=True)
    def show_page_bssid_tracker(self): self.hide_all(); self.pages["bssid_tracker"].pack(fill="both", expand=True)
    def show_page_driver_check(self): self.hide_all(); self.pages["driver_check"].pack(fill="both", expand=True)
    def show_page_routing(self): self.hide_all(); self.pages["routing"].pack(fill="both", expand=True); self.pages["routing"].on_show()
    def show_page_advanced(self): self.hide_all(); self.pages["advanced"].pack(fill="both", expand=True)
    def show_page_latency_trend(self): self.hide_all(); self.pages["latency_trend"].pack(fill="both", expand=True)
    def show_page_simple_ping(self): self.hide_all(); self.pages["simple_ping"].pack(fill="both", expand=True)
    def show_page_mtu(self): self.hide_all(); self.pages["mtu"].pack(fill="both", expand=True)
    def show_page_public_ip(self): self.hide_all(); self.pages["public_ip"].pack(fill="both", expand=True)
    def show_page_geo_ip(self): self.hide_all(); self.pages["geo_ip"].pack(fill="both", expand=True)
    def show_page_gateway_ping(self): self.hide_all(); self.pages["gateway_ping"].pack(fill="both", expand=True)
    def show_page_external_ping(self): self.hide_all(); self.pages["external_ping"].pack(fill="both", expand=True)
    def show_page_dns_lookup(self): self.hide_all(); self.pages["dns_lookup"].pack(fill="both", expand=True)
    def show_page_reverse_dns(self): self.hide_all(); self.pages["reverse_dns"].pack(fill="both", expand=True)
    def show_page_whois(self): self.hide_all(); self.pages["whois"].pack(fill="both", expand=True)
    def show_page_http_check(self): self.hide_all(); self.pages["http_check"].pack(fill="both", expand=True)
    def show_page_ipv6_check(self): self.hide_all(); self.pages["ipv6_check"].pack(fill="both", expand=True)
    def show_page_security(self): self.hide_all(); self.pages["security"].pack(fill="both", expand=True)
    def show_page_security_pro(self): self.hide_all(); self.pages["security_pro"].pack(fill="both", expand=True)
    def show_page_dns_pro(self): self.hide_all(); self.pages["dns_pro"].pack(fill="both", expand=True)
    def show_page_dns_leak(self): self.hide_all(); self.pages["dns_leak"].pack(fill="both", expand=True)
    def show_page_port_scanner_pro(self): self.hide_all(); self.pages["port_scanner_pro"].pack(fill="both", expand=True)
    def show_page_port_scan_local(self): self.hide_all(); self.pages["port_scan_local"].pack(fill="both", expand=True)
    def show_page_firewall(self): self.hide_all(); self.pages["firewall"].pack(fill="both", expand=True)
    def show_page_proxy(self): self.hide_all(); self.pages["proxy"].pack(fill="both", expand=True)
    def show_page_vpn(self): self.hide_all(); self.pages["vpn"].pack(fill="both", expand=True)
    def show_page_icmp_flood(self): self.hide_all(); self.pages["icmp_flood"].pack(fill="both", expand=True)
    def show_page_udp_test(self): self.hide_all(); self.pages["udp_test"].pack(fill="both", expand=True)
    def show_page_netstat(self): self.hide_all(); self.pages["netstat"].pack(fill="both", expand=True)
    def show_page_packet_sniffer_pro(self): self.hide_all(); self.pages["packet_sniffer_pro"].pack(fill="both", expand=True)
    def show_page_netflow(self): self.hide_all(); self.pages["netflow"].pack(fill="both", expand=True)
    def show_page_tools(self): self.hide_all(); self.pages["tools"].pack(fill="both", expand=True)
    def show_page_monitoring(self): self.hide_all(); self.pages["monitoring"].pack(fill="both", expand=True)
    def show_page_monitoring_pro(self): self.hide_all(); self.pages["monitoring_pro"].pack(fill="both", expand=True)
    def show_page_gaming(self): self.hide_all(); self.pages["gaming"].pack(fill="both", expand=True)
    def show_page_system_info(self): self.hide_all(); self.pages["system_info"].pack(fill="both", expand=True)
    def show_page_experimental(self): self.hide_all(); self.pages["experimental"].pack(fill="both", expand=True)
    def show_page_packet_sniffer(self): self.hide_all(); self.pages["packet_sniffer"].pack(fill="both", expand=True)
    def show_page_bluetooth(self): self.hide_all(); self.pages["bluetooth"].pack(fill="both", expand=True)
    def show_page_speed_compare(self): self.hide_all(); self.pages["speed_compare"].pack(fill="both", expand=True)
    def show_page_speedtest_servers(self): self.hide_all(); self.pages["speedtest_servers"].pack(fill="both", expand=True)
    def show_page_tcp_optimizer(self): self.hide_all(); self.pages["tcp_optimizer"].pack(fill="both", expand=True)
    def show_page_tcp_apply(self): self.hide_all(); self.pages["tcp_apply"].pack(fill="both", expand=True)
    def show_page_traffic_analyzer(self): self.hide_all(); self.pages["traffic_analyzer"].pack(fill="both", expand=True)
    def show_page_mesh_scanner(self): self.hide_all(); self.pages["mesh_scanner"].pack(fill="both", expand=True)
    def show_page_doctor(self): self.hide_all(); self.pages["doctor"].pack(fill="both", expand=True)
    def show_page_dns_cache(self): self.hide_all(); self.pages["dns_cache"].pack(fill="both", expand=True)
    def show_page_winsock(self): self.hide_all(); self.pages["winsock"].pack(fill="both", expand=True)
    def show_page_ip_reset(self): self.hide_all(); self.pages["ip_reset"].pack(fill="both", expand=True)
    def show_page_netsh_reset(self): self.hide_all(); self.pages["netsh_reset"].pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()