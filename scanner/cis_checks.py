import paramiko
from datetime import datetime

class CISBenchmarkChecker:
    """
    Trinity6 CIS Benchmark Checker
    Legacy hardcoded checks - use compliance_engine.py
    for dynamic YAML based checking
    This file provides direct SSH based checks
    as backup and reference
    """
    
    def __init__(self, ssh_client, hostname):
        self.ssh = ssh_client
        self.hostname = hostname
        self.results = []
    
    def run_command(self, command):
        """Execute command on remote server"""
        try:
            stdin, stdout, stderr = self.ssh.exec_command(
                command, timeout=10
            )
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            return output, error
        except Exception as e:
            return "", str(e)
    
    def add_result(self, control_id, description,
                   status, current_value, expected_value,
                   severity="Medium", remediation=""):
        """Add check result"""
        self.results.append({
            'control_id': control_id,
            'description': description,
            'status': status,
            'current_value': str(current_value),
            'expected_value': str(expected_value),
            'severity': severity,
            'remediation': remediation,
            'timestamp': datetime.now().isoformat()
        })
    
    # ==========================================
    # SECTION 1 - FILESYSTEM
    # ==========================================
    
    def check_filesystem_cramfs(self):
        """CIS 1.1.1.1 - Ensure cramfs is disabled"""
        output, _ = self.run_command(
            "modprobe -n -v cramfs 2>&1"
        )
        status = "PASS" if "install /bin/true" in output else "FAIL"
        self.add_result(
            "1.1.1.1",
            "Ensure cramfs filesystem is disabled",
            status,
            output,
            "install /bin/true",
            "Low",
            "echo 'install cramfs /bin/true' >> /etc/modprobe.d/CIS.conf"
        )
    
    def check_aslr_enabled(self):
        """CIS 1.5.3 - Ensure ASLR is enabled"""
        output, _ = self.run_command(
            "sysctl kernel.randomize_va_space"
        )
        status = "PASS" if "= 2" in output else "FAIL"
        self.add_result(
            "1.5.3",
            "Ensure address space layout randomization is enabled",
            status,
            output,
            "kernel.randomize_va_space = 2",
            "High",
            "echo 'kernel.randomize_va_space = 2' >> /etc/sysctl.conf"
        )
    
    # ==========================================
    # SECTION 2 - SERVICES
    # ==========================================
    
    def check_xinetd_not_installed(self):
        """CIS 2.1.1 - Ensure xinetd is not installed"""
        output, _ = self.run_command(
            "dpkg -l xinetd 2>/dev/null | grep -c xinetd"
        )
        try:
            count = int(output.strip())
            status = "PASS" if count == 0 else "FAIL"
        except:
            status = "FAIL"
        self.add_result(
            "2.1.1",
            "Ensure xinetd is not installed",
            status,
            output,
            "0",
            "Medium",
            "apt purge xinetd -y"
        )
    
    def check_nfs_not_enabled(self):
        """CIS 2.2.7 - Ensure NFS is not enabled"""
        output, _ = self.run_command(
            "systemctl is-enabled nfs-server 2>/dev/null"
        )
        status = "PASS" if "disabled" in output or "not-found" in output else "FAIL"
        self.add_result(
            "2.2.7",
            "Ensure NFS is not enabled",
            status,
            output,
            "disabled",
            "Medium",
            "systemctl disable nfs-server"
        )
    
    def check_ftp_not_enabled(self):
        """CIS 2.2.9 - Ensure FTP is not enabled"""
        output, _ = self.run_command(
            "systemctl is-enabled vsftpd 2>/dev/null"
        )
        status = "PASS" if "disabled" in output or "not-found" in output else "FAIL"
        self.add_result(
            "2.2.9",
            "Ensure FTP Server is not enabled",
            status,
            output,
            "disabled",
            "High",
            "systemctl disable vsftpd"
        )
    
    # ==========================================
    # SECTION 3 - NETWORK
    # ==========================================
    
    def check_ip_forwarding_disabled(self):
        """CIS 3.1.1 - Ensure IP forwarding is disabled"""
        output, _ = self.run_command(
            "sysctl net.ipv4.ip_forward"
        )
        status = "PASS" if "= 0" in output else "FAIL"
        self.add_result(
            "3.1.1",
            "Ensure IP forwarding is disabled",
            status,
            output,
            "net.ipv4.ip_forward = 0",
            "Medium",
            "sysctl -w net.ipv4.ip_forward=0"
        )
    
    def check_tcp_syncookies(self):
        """CIS 3.2.8 - Ensure TCP SYN Cookies is enabled"""
        output, _ = self.run_command(
            "sysctl net.ipv4.tcp_syncookies"
        )
        status = "PASS" if "= 1" in output else "FAIL"
        self.add_result(
            "3.2.8",
            "Ensure TCP SYN Cookies is enabled",
            status,
            output,
            "net.ipv4.tcp_syncookies = 1",
            "Medium",
            "sysctl -w net.ipv4.tcp_syncookies=1"
        )
    
    def check_firewall_active(self):
        """CIS 3.4.2 - Ensure firewall is active"""
        output, _ = self.run_command(
            "ufw status | grep Status"
        )
        status = "PASS" if "active" in output else "FAIL"
        self.add_result(
            "3.4.2",
            "Ensure firewall is active and enabled",
            status,
            output,
            "Status: active",
            "High",
            "ufw enable"
        )
    
    # ==========================================
    # SECTION 4 - LOGGING
    # ==========================================
    
    def check_auditd_installed(self):
        """CIS 4.1.1.1 - Ensure auditd is installed"""
        output, _ = self.run_command(
            "dpkg -l auditd 2>/dev/null | grep -c auditd"
        )
        try:
            count = int(output.strip())
            status = "PASS" if count > 0 else "FAIL"
        except:
            status = "FAIL"
        self.add_result(
            "4.1.1.1",
            "Ensure auditd is installed",
            status,
            output,
            "1 or more",
            "High",
            "apt install auditd -y"
        )
    
    def check_auditd_running(self):
        """CIS 4.1.1.2 - Ensure auditd service is running"""
        output, _ = self.run_command(
            "systemctl is-active auditd"
        )
        status = "PASS" if "active" in output else "FAIL"
        self.add_result(
            "4.1.1.2",
            "Ensure auditd service is enabled and running",
            status,
            output,
            "active",
            "High",
            "systemctl enable auditd && systemctl start auditd"
        )
    
    def check_rsyslog_installed(self):
        """CIS 4.2.1.1 - Ensure rsyslog is installed"""
        output, _ = self.run_command(
            "dpkg -l rsyslog 2>/dev/null | grep -c rsyslog"
        )
        try:
            count = int(output.strip())
            status = "PASS" if count > 0 else "FAIL"
        except:
            status = "FAIL"
        self.add_result(
            "4.2.1.1",
            "Ensure rsyslog is installed",
            status,
            output,
            "1 or more",
            "High",
            "apt install rsyslog -y"
        )
    
    # ==========================================
    # SECTION 5 - ACCESS CONTROL
    # ==========================================
    
    def check_sudo_installed(self):
        """CIS 5.2.1 - Ensure sudo is installed"""
        output, _ = self.run_command(
            "dpkg -l sudo 2>/dev/null | grep -c sudo"
        )
        try:
            count = int(output.strip())
            status = "PASS" if count > 0 else "FAIL"
        except:
            status = "FAIL"
        self.add_result(
            "5.2.1",
            "Ensure sudo is installed",
            status,
            output,
            "1 or more",
            "High",
            "apt install sudo -y"
        )
    
    def check_password_expiry(self):
        """CIS 5.4.1.1 - Ensure password expiration"""
        output, _ = self.run_command(
            "grep PASS_MAX_DAYS /etc/login.defs"
        )
        try:
            days = int(output.split()[-1])
            status = "PASS" if days <= 365 else "FAIL"
        except:
            status = "FAIL"
            days = "Unknown"
        self.add_result(
            "5.4.1.1",
            "Ensure password expiration is 365 days or less",
            status,
            str(days),
            "365 or less",
            "Medium",
            "sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS 365/' /etc/login.defs"
        )
    
    def check_password_min_length(self):
        """CIS 5.3.1 - Ensure password minimum length"""
        output, _ = self.run_command(
            "grep minlen /etc/security/pwquality.conf"
        )
        try:
            length = int(output.split("=")[-1].strip())
            status = "PASS" if length >= 14 else "FAIL"
        except:
            status = "FAIL"
            length = "Unknown"
        self.add_result(
            "5.3.1",
            "Ensure password minimum length is 14 or more",
            status,
            str(length),
            "14 or more",
            "High",
            "sed -i 's/^.*minlen.*/minlen = 14/' /etc/security/pwquality.conf"
        )
    
    def check_su_restricted(self):
        """CIS 5.6 - Ensure su access is restricted"""
        output, _ = self.run_command(
            "grep pam_wheel /etc/pam.d/su"
        )
        status = "PASS" if "pam_wheel" in output else "FAIL"
        self.add_result(
            "5.6",
            "Ensure access to su command is restricted",
            status,
            output,
            "pam_wheel required",
            "High",
            "echo 'auth required pam_wheel.so use_uid' >> /etc/pam.d/su"
        )
    
    # ==========================================
    # SECTION 6 - SYSTEM MAINTENANCE
    # ==========================================
    
    def check_passwd_permissions(self):
        """CIS 6.1.1 - Ensure permissions on passwd"""
        output, _ = self.run_command(
            "stat /etc/passwd | grep Access | head -1"
        )
        status = "PASS" if "0644" in output else "FAIL"
        self.add_result(
            "6.1.1",
            "Ensure permissions on passwd file are configured",
            status,
            output,
            "0644",
            "High",
            "chmod 644 /etc/passwd && chown root:root /etc/passwd"
        )
    
    def check_shadow_permissions(self):
        """CIS 6.1.2 - Ensure permissions on shadow"""
        output, _ = self.run_command(
            "stat /etc/shadow | grep Access | head -1"
        )
        status = "PASS" if "0640" in output or "0000" in output else "FAIL"
        self.add_result(
            "6.1.2",
            "Ensure permissions on shadow file are configured",
            status,
            output,
            "0640",
            "Critical",
            "chmod o-rwx,g-wx /etc/shadow && chown root:shadow /etc/shadow"
        )
    
    def check_world_writable_files(self):
        """CIS 6.1.7 - Ensure no world writable files"""
        output, _ = self.run_command(
            "find / -xdev -type f -perm -0002 2>/dev/null | wc -l"
        )
        try:
            count = int(output.strip())
            status = "PASS" if count == 0 else "FAIL"
        except:
            status = "FAIL"
            count = "Unknown"
        self.add_result(
            "6.1.7",
            "Ensure no world writable files exist",
            status,
            str(count),
            "0",
            "High",
            "find / -xdev -type f -perm -0002 -exec chmod o-w {} +"
        )
    
    def check_root_uid(self):
        """CIS 6.2.3 - Ensure root is only UID 0 account"""
        output, _ = self.run_command(
            "awk -F: '($3 == 0) { print $1}' /etc/passwd | wc -l"
        )
        try:
            count = int(output.strip())
            status = "PASS" if count == 1 else "FAIL"
        except:
            status = "FAIL"
            count = "Unknown"
        self.add_result(
            "6.2.3",
            "Ensure root is the only UID 0 account",
            status,
            str(count),
            "1",
            "Critical",
            "Review accounts with UID 0 immediately"
        )
    
    # ==========================================
    # RUN ALL CHECKS
    # ==========================================
    
    def run_all_checks(self):
        """Run all CIS benchmark checks"""
        print(f"\nRunning CIS checks on {self.hostname}...")
        print("=" * 50)
        
        checks = [
            self.check_filesystem_cramfs,
            self.check_aslr_enabled,
            self.check_xinetd_not_installed,
            self.check_nfs_not_enabled,
            self.check_ftp_not_enabled,
            self.check_ip_forwarding_disabled,
            self.check_tcp_syncookies,
            self.check_firewall_active,
            self.check_auditd_installed,
            self.check_auditd_running,
            self.check_rsyslog_installed,
            self.check_sudo_installed,
            self.check_password_expiry,
            self.check_password_min_length,
            self.check_su_restricted,
            self.check_passwd_permissions,
            self.check_shadow_permissions,
            self.check_world_writable_files,
            self.check_root_uid,
        ]
        
        passed = 0
        failed = 0
        
        for check in checks:
            try:
                check()
                last = self.results[-1]
                if last['status'] == 'PASS':
                    passed += 1
                    print(f"  ✅ {last['control_id']} - PASS")
                else:
                    failed += 1
                    print(f"  ❌ {last['control_id']} - FAIL - {last['severity']}")
            except Exception as e:
                print(f"  ⚠️  Error running check: {str(e)}")
        
        print("=" * 50)
        print(f"Pass: {passed} | Fail: {failed} | Total: {len(self.results)}")
        
        return self.results
    
    def get_compliance_score(self):
        """Calculate overall compliance score"""
        if not self.results:
            return {'score': 0, 'passed': 0, 'failed': 0, 'total': 0}
        
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        total = len(self.results)
        score = (passed / total * 100)
        
        return {
            'score': round(score, 2),
            'passed': passed,
            'failed': total - passed,
            'total': total
        }
