import yaml
import os
import json
from pathlib import Path
from datetime import datetime

class ComplianceEngine:
    """
    Trinity6 Compliance Engine
    Reads compliance as code YAML files
    and executes checks dynamically
    """
    
    def __init__(self, controls_path="compliance"):
        self.controls_path = controls_path
        self.controls = []
    
    def load_controls(self, framework=None, os_type=None):
        """Load all compliance controls from YAML files"""
        self.controls = []
        
        for yaml_file in Path(self.controls_path).rglob("*.yaml"):
            try:
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)
                
                if framework and data.get('framework') != framework:
                    continue
                if os_type and data.get('os') != os_type:
                    continue
                
                for control in data.get('controls', []):
                    control['source_file'] = str(yaml_file)
                    control['framework'] = data.get('framework')
                    control['os'] = data.get('os')
                    control['section'] = data.get('section')
                    control['section_title'] = data.get('title')
                    self.controls.append(control)
                    
            except Exception as e:
                print(f"Error loading {yaml_file}: {str(e)}")
        
        print(f"Loaded {len(self.controls)} compliance controls")
        return self.controls
    
    def execute_check(self, ssh_client, control):
        """Execute a single compliance check"""
        check = control.get('check', {})
        command = check.get('command')
        
        if not command:
            return None
        
        try:
            stdin, stdout, stderr = ssh_client.exec_command(
                command, timeout=10
            )
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            
            passed = self.evaluate_result(output, check)
            
            return {
                'control_id': control['id'],
                'title': control['title'],
                'description': control.get('description', ''),
                'severity': control['severity'],
                'section': control.get('section'),
                'section_title': control.get('section_title'),
                'frameworks': control.get('frameworks', []),
                'status': 'PASS' if passed else 'FAIL',
                'output': output,
                'expected': check.get('expected'),
                'remediation': control.get('remediation', {}),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'control_id': control['id'],
                'title': control['title'],
                'severity': control['severity'],
                'status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def evaluate_result(self, output, check):
        """Evaluate if check output meets expected value"""
        operator = check.get('operator', '==')
        expected = check.get('expected')
        parse = check.get('parse', 'raw')
        
        try:
            if parse == 'last_value':
                value = int(output.split()[-1])
            elif parse == 'value_after_equals':
                value = int(output.split('=')[-1].strip())
            else:
                value = output
            
            if operator == '<=':
                return int(value) <= int(expected)
            elif operator == '>=':
                return int(value) >= int(expected)
            elif operator == '==':
                return str(value) == str(expected)
            elif operator == 'contains':
                return str(expected) in str(value)
            elif operator == 'not_contains':
                return str(expected) not in str(value)
            else:
                return False
                
        except Exception as e:
            return False
    
    def run_all_checks(self, ssh_client, hostname):
        """Run all loaded compliance checks on a server"""
        print(f"\nRunning {len(self.controls)} checks on {hostname}")
        print("=" * 50)
        
        results = []
        passed = 0
        failed = 0
        errors = 0
        
        for control in self.controls:
            result = self.execute_check(ssh_client, control)
            if result:
                results.append(result)
                if result['status'] == 'PASS':
                    passed += 1
                    print(f"  ✅ {control['id']} - PASS")
                elif result['status'] == 'FAIL':
                    failed += 1
                    print(f"  ❌ {control['id']} - FAIL - {control['severity']}")
                else:
                    errors += 1
                    print(f"  ⚠️  {control['id']} - ERROR")
        
        print("=" * 50)
        print(f"Total: {len(results)} | Pass: {passed} | Fail: {failed} | Error: {errors}")
        
        return results
    
    def get_compliance_score(self, results):
        """Calculate overall compliance score"""
        if not results:
            return {
                'score': 0,
                'passed': 0,
                'failed': 0,
                'errors': 0,
                'total': 0
            }
        
        passed = sum(1 for r in results if r['status'] == 'PASS')
        failed = sum(1 for r in results if r['status'] == 'FAIL')
        errors = sum(1 for r in results if r['status'] == 'ERROR')
        total = len(results)
        score = (passed / total * 100) if total > 0 else 0
        
        return {
            'score': round(score, 2),
            'passed': passed,
            'failed': failed,
            'errors': errors,
            'total': total
        }
    
    def get_critical_findings(self, results):
        """Get all critical and high severity failures"""
        return [
            r for r in results 
            if r['status'] == 'FAIL' 
            and r['severity'] in ['Critical', 'High']
        ]
    
    def get_framework_coverage(self, results):
        """Show compliance coverage per framework"""
        frameworks = {}
        
        for result in results:
            for framework in result.get('frameworks', []):
                if isinstance(framework, str):
                    fw_name = framework
                elif isinstance(framework, dict):
                    fw_name = list(framework.keys())[0]
                else:
                    continue
                
                if fw_name not in frameworks:
                    frameworks[fw_name] = {
                        'passed': 0,
                        'failed': 0,
                        'total': 0
                    }
                
                frameworks[fw_name]['total'] += 1
                if result['status'] == 'PASS':
                    frameworks[fw_name]['passed'] += 1
                else:
                    frameworks[fw_name]['failed'] += 1
        
        for fw in frameworks:
            total = frameworks[fw]['total']
            passed = frameworks[fw]['passed']
            frameworks[fw]['score'] = round(
                (passed / total * 100) if total > 0 else 0, 2
            )
        
        return frameworks
    
    def get_section_summary(self, results):
        """Get compliance summary per CIS section"""
        sections = {}
        
        for result in results:
            section = result.get('section', 'Unknown')
            title = result.get('section_title', 'Unknown')
            key = f"Section {section} - {title}"
            
            if key not in sections:
                sections[key] = {
                    'passed': 0,
                    'failed': 0,
                    'total': 0
                }
            
            sections[key]['total'] += 1
            if result['status'] == 'PASS':
                sections[key]['passed'] += 1
            else:
                sections[key]['failed'] += 1
        
        for section in sections:
            total = sections[section]['total']
            passed = sections[section]['passed']
            sections[section]['score'] = round(
                (passed / total * 100) if total > 0 else 0, 2
            )
        
        return sections
    
    def save_results(self, results, hostname, output_dir="results"):
        """Save scan results to JSON file"""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{output_dir}/trinity6_{hostname}_{timestamp}.json"
        
        output = {
            'scan_info': {
                'hostname': hostname,
                'timestamp': datetime.now().isoformat(),
                'total_checks': len(results),
                'framework': 'CIS'
            },
            'compliance_score': self.get_compliance_score(results),
            'framework_coverage': self.get_framework_coverage(results),
            'section_summary': self.get_section_summary(results),
            'critical_findings': self.get_critical_findings(results),
            'all_results': results
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\nResults saved to {filename}")
        return filename
