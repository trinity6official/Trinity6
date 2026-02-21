import paramiko
import json
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.discovery import NetworkDiscovery
from scanner.cis_checks import CISBenchmarkChecker
from engine.compliance_engine import ComplianceEngine
from scanner.ai_analyst import Trinity6AIAnalyst

class Trinity6Scanner:
    """
    Trinity6 Main Scanner
    Orchestrates network discovery,
    compliance checking, and AI analysis
    """
    
    def __init__(self, network_range):
        self.network_range = network_range
        self.scan_results = []
        self.scan_id = datetime.now().strftime("%Y%m%d%H%M%S")
        self.engine = ComplianceEngine()
        self.analyst = Trinity6AIAnalyst(model="mistral")
    
    def connect_ssh(self, ip, username,
                    private_key_path=None,
                    password=None):
        """Connect to server via SSH"""
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy()
            )
            
            if private_key_path:
                private_key = paramiko.RSAKey.from_private_key_file(
                    private_key_path
                )
                client.connect(
                    hostname=ip,
                    username=username,
                    pkey=private_key,
                    timeout=10
                )
            else:
                client.connect(
                    hostname=ip,
                    username=username,
                    password=password,
                    timeout=10
                )
            
            print(f"  ✅ SSH connected to {ip}")
            return client
            
        except Exception as e:
            print(f"  ❌ SSH failed to {ip}: {str(e)}")
            return None
    
    def scan_device(self, device, credentials):
        """Run full compliance scan on a single device"""
        ip = device['ip']
        hostname = device.get('hostname', ip)
        
        print(f"\nScanning {ip} ({hostname})")
        print(f"Device type: {device['device_type']}")
        
        if 'Linux' not in device['device_type'] and \
           'Linux' not in device.get('os_hint', ''):
            print(f"Skipping {ip} - not a Linux server")
            return None
        
        ssh_client = self.connect_ssh(
            ip,
            credentials.get('username', 'trinity6_audit'),
            credentials.get('private_key_path'),
            credentials.get('password')
        )
        
        if not ssh_client:
            return None
        
        try:
            self.engine.load_controls(
                framework='CIS',
                os_type='linux'
            )
            
            check_results = self.engine.run_all_checks(
                ssh_client, ip
            )
            
            compliance_score = self.engine.get_compliance_score(
                check_results
            )
            
            framework_coverage = self.engine.get_framework_coverage(
                check_results
            )
            
            section_summary = self.engine.get_section_summary(
                check_results
            )
            
            critical_findings = self.engine.get_critical_findings(
                check_results
            )
            
            print(f"\nRunning AI analysis...")
            ai_analysis = self.analyst.analyze_scan_results(
                check_results, ip
            )
            
            executive_summary = self.analyst.generate_executive_summary(
                ip,
                compliance_score['score'],
                compliance_score['total'],
                critical_findings,
                framework_coverage
            )
            
            scan_result = {
                'scan_id': self.scan_id,
                'device': device,
                'hostname': hostname,
                'ip': ip,
                'compliance_score': compliance_score,
                'framework_coverage': framework_coverage,
                'section_summary': section_summary,
                'critical_findings': critical_findings,
                'checks': check_results,
                'ai_analysis': ai_analysis,
                'executive_summary': executive_summary,
                'framework': 'CIS',
                'scan_time': datetime.now().isoformat()
            }
            
            print(f"\nCompliance Score: {compliance_score['score']}%")
            print(f"Passed: {compliance_score['passed']}")
            print(f"Failed: {compliance_score['failed']}")
            print(f"Critical Findings: {len(critical_findings)}")
            
            return scan_result
            
        finally:
            ssh_client.close()
    
    def run_full_scan(self, credentials):
        """Run complete network scan"""
        print("\n" + "=" * 60)
        print("  TRINITY6 GRC SCANNER")
        print("  Intelligent Security - Powered by AI")
        print("=" * 60)
        print(f"Scan ID: {self.scan_id}")
        print(f"Network: {self.network_range}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        discovery = NetworkDiscovery(self.network_range)
        devices = discovery.discover()
        discovery.print_summary()
        
        scannable = discovery.get_scannable_devices()
        print(f"\nStarting compliance scans on {len(scannable)} devices...")
        
        for device in scannable:
            result = self.scan_device(device, credentials)
            if result:
                self.scan_results.append(result)
                self.engine.save_results(
                    result['checks'],
                    result['ip']
                )
        
        self.save_full_results()
        self.print_final_summary()
        
        return self.scan_results
    
    def scan_single_host(self, ip, credentials):
        """Scan a single specific host"""
        print("\n" + "=" * 60)
        print("  TRINITY6 GRC SCANNER - Single Host")
        print("=" * 60)
        
        device = {
            'ip': ip,
            'hostname': ip,
            'device_type': 'Linux Server',
            'os_hint': 'Linux/Unix',
            'open_ports': {},
            'status': 'online',
            'scannable': True
        }
        
        result = self.scan_device(device, credentials)
        
        if result:
            self.scan_results.append(result)
            self.engine.save_results(
                result['checks'],
                result['ip']
            )
            self.print_final_summary()
        
        return result
    
    def save_full_results(self):
        """Save complete scan results"""
        os.makedirs('results', exist_ok=True)
        filename = f"results/trinity6_full_scan_{self.scan_id}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                'scan_id': self.scan_id,
                'network': self.network_range,
                'scan_time': datetime.now().isoformat(),
                'total_devices_scanned': len(self.scan_results),
                'results': self.scan_results
            }, f, indent=2)
        
        print(f"\nFull results saved to {filename}")
    
    def print_final_summary(self):
        """Print final scan summary"""
        print("\n" + "=" * 60)
        print("  TRINITY6 SCAN COMPLETE")
        print("=" * 60)
        print(f"Devices scanned: {len(self.scan_results)}")
        
        if self.scan_results:
            print("\nDevice Compliance Scores:")
            for result in self.scan_results:
                ip = result['ip']
                score = result['compliance_score']['score']
                passed = result['compliance_score']['passed']
                failed = result['compliance_score']['failed']
                critical = len(result['critical_findings'])
                
                status = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
                
                print(f"\n  {status} {ip}")
                print(f"     Score: {score}%")
                print(f"     Passed: {passed} | Failed: {failed}")
                print(f"     Critical Issues: {critical}")
            
            avg_score = sum(
                r['compliance_score']['score']
                for r in self.scan_results
            ) / len(self.scan_results)
            
            print(f"\nNetwork Average Score: {round(avg_score, 2)}%")
        
        print("=" * 60)
        print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)


if __name__ == "__main__":
    scanner = Trinity6Scanner("192.168.1.0/24")
    
    credentials = {
        'username': 'trinity6_audit',
        'private_key_path': '/path/to/private/key'
    }
    
    results = scanner.run_full_scan(credentials)
