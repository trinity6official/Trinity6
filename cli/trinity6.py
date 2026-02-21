#!/usr/bin/env python3
"""
Trinity6 CLI Tool
Command line interface for Trinity6 GRC Scanner
"""

import argparse
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.main import Trinity6Scanner

def cmd_scan(args):
    """Run network scan"""
    print(f"Starting Trinity6 scan on {args.network}")
    
    credentials = {}
    
    if args.key:
        credentials['private_key_path'] = args.key
    if args.password:
        credentials['password'] = args.password
    if args.username:
        credentials['username'] = args.username
    else:
        credentials['username'] = 'trinity6_audit'
    
    scanner = Trinity6Scanner(args.network)
    results = scanner.run_full_scan(credentials)
    
    print(f"\nScan complete. {len(results)} devices scanned.")

def cmd_host(args):
    """Scan a single host"""
    print(f"Starting Trinity6 scan on {args.host}")
    
    credentials = {}
    
    if args.key:
        credentials['private_key_path'] = args.key
    if args.password:
        credentials['password'] = args.password
    if args.username:
        credentials['username'] = args.username
    else:
        credentials['username'] = 'trinity6_audit'
    
    scanner = Trinity6Scanner(args.host)
    result = scanner.scan_single_host(args.host, credentials)
    
    if result:
        print(f"\nScan complete.")
        print(f"Score: {result['compliance_score']['score']}%")

def cmd_report(args):
    """Generate report from saved results"""
    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}")
        sys.exit(1)
    
    with open(args.file, 'r') as f:
        results = json.load(f)
    
    print(f"Generating report from {args.file}")
    print(f"Format: {args.format}")
    print("Report generation coming in Phase 2")

def cmd_discover(args):
    """Discover devices on network"""
    from scanner.discovery import NetworkDiscovery
    
    print(f"Discovering devices on {args.network}")
    
    discovery = NetworkDiscovery(args.network)
    devices = discovery.discover()
    discovery.print_summary()
    
    if args.output:
        import json
        with open(args.output, 'w') as f:
            json.dump({
                'network': args.network,
                'devices': devices,
                'summary': discovery.get_summary()
            }, f, indent=2)
        print(f"\nResults saved to {args.output}")

def cmd_version(args):
    """Show version information"""
    print("""
╔══════════════════════════════════════╗
║         TRINITY6 GRC SCANNER         ║
║       Intelligent Security v1.0      ║
╚══════════════════════════════════════╝

Version:   1.0.0
Framework: CIS Benchmark 2.0
AI Model:  Mistral via Ollama
Author:    Trinity6
Website:   https://trinity6.com
""")

def main():
    parser = argparse.ArgumentParser(
        prog='trinity6',
        description="""
╔══════════════════════════════════════╗
║         TRINITY6 GRC SCANNER         ║
║       Intelligent Security v1.0      ║
╚══════════════════════════════════════╝
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(
        title='commands',
        dest='command'
    )
    
    # Scan network command
    scan_parser = subparsers.add_parser(
        'scan',
        help='Scan entire network range'
    )
    scan_parser.add_argument(
        '--network',
        required=True,
        help='Network range to scan (e.g. 192.168.1.0/24)'
    )
    scan_parser.add_argument(
        '--username',
        help='SSH username (default: trinity6_audit)'
    )
    scan_parser.add_argument(
        '--key',
        help='Path to SSH private key'
    )
    scan_parser.add_argument(
        '--password',
        help='SSH password (less secure than key)'
    )
    scan_parser.set_defaults(func=cmd_scan)
    
    # Single host command
    host_parser = subparsers.add_parser(
        'host',
        help='Scan a single host'
    )
    host_parser.add_argument(
        '--host',
        required=True,
        help='IP address or hostname to scan'
    )
    host_parser.add_argument(
        '--username',
        help='SSH username (default: trinity6_audit)'
    )
    host_parser.add_argument(
        '--key',
        help='Path to SSH private key'
    )
    host_parser.add_argument(
        '--password',
        help='SSH password'
    )
    host_parser.set_defaults(func=cmd_host)
    
    # Discover command
    discover_parser = subparsers.add_parser(
        'discover',
        help='Discover devices on network'
    )
    discover_parser.add_argument(
        '--network',
        required=True,
        help='Network range to discover'
    )
    discover_parser.add_argument(
        '--output',
        help='Save results to JSON file'
    )
    discover_parser.set_defaults(func=cmd_discover)
    
    # Report command
    report_parser = subparsers.add_parser(
        'report',
        help='Generate report from scan results'
    )
    report_parser.add_argument(
        '--file',
        required=True,
        help='Path to scan results JSON file'
    )
    report_parser.add_argument(
        '--format',
        choices=['pdf', 'html', 'json'],
        default='pdf',
        help='Report format (default: pdf)'
    )
    report_parser.set_defaults(func=cmd_report)
    
    # Version command
    version_parser = subparsers.add_parser(
        'version',
        help='Show version information'
    )
    version_parser.set_defaults(func=cmd_version)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        print("""
Examples:
  Scan entire network:
    python trinity6.py scan --network 192.168.1.0/24 --key ~/.ssh/id_rsa

  Scan single host:
    python trinity6.py host --host 192.168.1.100 --key ~/.ssh/id_rsa

  Discover devices:
    python trinity6.py discover --network 192.168.1.0/24

  Generate report:
    python trinity6.py report --file results/scan.json --format pdf
""")
        sys.exit(0)
    
    args.func(args)


if __name__ == "__main__":
    main()
