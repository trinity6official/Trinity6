import socket
import subprocess
import ipaddress
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

class NetworkDiscovery:
    """
    Trinity6 Network Discovery Module
    Discovers all connected devices on a network
    """
    
    def __init__(self, network_range):
        self.network_range = network_range
        self.discovered_devices = []
    
    def ping_host(self, ip):
        """Check if host is alive"""
        try:
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '1', str(ip)],
                capture_output=True,
                timeout=2
            )
            if result.returncode == 0:
                return str(ip)
        except:
            pass
        return None
    
    def get_hostname(self, ip):
        """Get hostname for IP address"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return "Unknown"
    
    def get_open_ports(self, ip):
        """Check common ports to identify device type"""
        common_ports = {
            22: 'SSH',
            23: 'Telnet',
            80: 'HTTP',
            443: 'HTTPS',
            445: 'SMB',
            3389: 'RDP',
            3306: 'MySQL',
            5432: 'PostgreSQL',
            6379: 'Redis',
            8080: 'HTTP-Alt',
            8443: 'HTTPS-Alt'
        }
        
        open_ports = {}
        for port, service in common_ports.items():
            try:
                sock = socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM
                )
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    open_ports[port] = service
                sock.close()
            except:
                pass
        
        return open_ports
    
    def classify_device(self, open_ports):
        """Classify device based on open ports"""
        if 3389 in open_ports and 445 in open_ports:
            return "Windows Server"
        elif 3389 in open_ports:
            return "Windows Desktop"
        elif 22 in open_ports and 445 in open_ports:
            return "Linux Server"
        elif 22 in open_ports:
            return "Linux Server"
        elif 23 in open_ports:
            return "Network Device"
        elif 80 in open_ports or 443 in open_ports:
            return "Web Server"
        elif 3306 in open_ports:
            return "Database Server"
        elif 5432 in open_ports:
            return "Database Server"
        else:
            return "Unknown Device"
    
    def get_os_hint(self, open_ports):
        """Get OS hint based on open ports"""
        if 3389 in open_ports:
            return "Windows"
        elif 22 in open_ports and 3389 not in open_ports:
            return "Linux/Unix"
        elif 23 in open_ports:
            return "Network OS"
        else:
            return "Unknown"
    
    def scan_host(self, ip):
        """Full scan of a single host"""
        if self.ping_host(ip):
            hostname = self.get_hostname(str(ip))
            open_ports = self.get_open_ports(str(ip))
            device_type = self.classify_device(open_ports)
            os_hint = self.get_os_hint(open_ports)
            
            device = {
                'ip': str(ip),
                'hostname': hostname,
                'device_type': device_type,
                'os_hint': os_hint,
                'open_ports': open_ports,
                'scan_time': datetime.now().isoformat(),
                'status': 'online',
                'scannable': os_hint in ['Linux/Unix', 'Windows']
            }
            
            print(f"  Found: {str(ip)} - {hostname} - {device_type}")
            return device
        return None
    
    def discover(self):
        """Discover all devices on network"""
        print("\n" + "=" * 50)
        print("TRINITY6 NETWORK DISCOVERY")
        print("=" * 50)
        print(f"Scanning network: {self.network_range}")
        
        network = ipaddress.IPv4Network(
            self.network_range,
            strict=False
        )
        
        hosts = list(network.hosts())
        print(f"Total hosts to scan: {len(hosts)}")
        print("Scanning...\n")
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            results = executor.map(self.scan_host, hosts)
        
        self.discovered_devices = [
            r for r in results if r is not None
        ]
        
        print(f"\nDiscovery complete!")
        print(f"Found {len(self.discovered_devices)} active devices")
        
        return self.discovered_devices
    
    def get_scannable_devices(self):
        """Get only devices that can be compliance scanned"""
        return [
            d for d in self.discovered_devices 
            if d.get('scannable', False)
        ]
    
    def get_summary(self):
        """Get summary of discovered devices"""
        summary = {
            'total_devices': len(self.discovered_devices),
            'scannable_devices': len(self.get_scannable_devices()),
            'device_types': {},
            'os_breakdown': {},
            'scan_time': datetime.now().isoformat(),
            'network': self.network_range
        }
        
        for device in self.discovered_devices:
            device_type = device['device_type']
            os_hint = device['os_hint']
            
            if device_type not in summary['device_types']:
                summary['device_types'][device_type] = 0
            summary['device_types'][device_type] += 1
            
            if os_hint not in summary['os_breakdown']:
                summary['os_breakdown'][os_hint] = 0
            summary['os_breakdown'][os_hint] += 1
        
        return summary
    
    def print_summary(self):
        """Print discovery summary"""
        summary = self.get_summary()
        
        print("\n" + "=" * 50)
        print("DISCOVERY SUMMARY")
        print("=" * 50)
        print(f"Total devices found: {summary['total_devices']}")
        print(f"Scannable devices: {summary['scannable_devices']}")
        print("\nDevice Types:")
        for dtype, count in summary['device_types'].items():
            print(f"  {dtype}: {count}")
        print("\nOS Breakdown:")
        for os, count in summary['os_breakdown'].items():
            print(f"  {os}: {count}")
        print("=" * 50)


if __name__ == "__main__":
    scanner = NetworkDiscovery("192.168.1.0/24")
    devices = scanner.discover()
    scanner.print_summary()
