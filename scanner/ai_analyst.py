import requests
import json
from datetime import datetime

class Trinity6AIAnalyst:
    """
    Trinity6 AI Analysis Layer
    Uses local Ollama + Mistral for zero cost
    privacy first AI analysis of scan results
    All processing happens on Trinity6 server
    Client data never leaves your infrastructure
    """
    
    def __init__(self, model="mistral"):
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"
    
    def is_ollama_running(self):
        """Check if Ollama is running"""
        try:
            response = requests.get(
                "http://localhost:11434/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def analyze(self, prompt):
        """Send prompt to local Mistral via Ollama"""
        if not self.is_ollama_running():
            return "AI analysis unavailable - Ollama not running"
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(
                self.ollama_url,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                return f"AI analysis failed: {response.status_code}"
                
        except Exception as e:
            return f"AI analysis error: {str(e)}"
    
    def analyze_scan_results(self, scan_results, hostname):
        """
        Analyze CIS scan results intelligently
        Type 2 AI - LLM reasoning on deterministic results
        """
        
        failed_checks = [
            r for r in scan_results
            if r.get('status') == 'FAIL'
        ]
        
        passed_checks = [
            r for r in scan_results
            if r.get('status') == 'PASS'
        ]
        
        critical_fails = [
            r for r in failed_checks
            if r.get('severity') in ['Critical', 'High']
        ]
        
        prompt = f"""You are a senior cybersecurity expert 
analyzing CIS benchmark scan results for a client server.

SERVER: {hostname}
SCAN DATE: {datetime.now().strftime('%Y-%m-%d %H:%M')}

SCAN SUMMARY:
- Total checks run: {len(scan_results)}
- Passed: {len(passed_checks)}
- Failed: {len(failed_checks)}
- Critical/High failures: {len(critical_fails)}
- Compliance score: {round(len(passed_checks)/len(scan_results)*100, 1)}%

FAILED CONTROLS:
{json.dumps(failed_checks, indent=2)}

Please provide a structured analysis with these sections:

1. OVERALL SECURITY POSTURE
Brief assessment of the server security posture.

2. TOP 3 CRITICAL FINDINGS
The three most important issues that need immediate attention.
For each finding explain:
- What the risk is
- Why it matters to the business
- Specific remediation command

3. QUICK WINS
Failed controls that are easy to fix immediately.

4. COMPLIANCE FRAMEWORK IMPACT
How these failures affect CIS, NIST, and ISO27001 compliance.

5. RECOMMENDED ACTION PLAN
Prioritized list of remediation steps.

Be specific, practical, and avoid unnecessary jargon.
"""
        
        return self.analyze(prompt)
    
    def generate_remediation_plan(self, failed_controls):
        """Generate specific remediation plan for failed controls"""
        
        prompt = f"""You are a Linux security engineer.
        
These CIS benchmark controls have FAILED and need remediation:

{json.dumps(failed_controls, indent=2)}

Create a practical remediation plan:

1. GROUP the fixes by category
   (filesystem, services, network, logging, access control)

2. For each group provide:
   - Exact Linux commands to fix each issue
   - Order to run them safely
   - How to verify each fix worked
   - Any warnings or precautions

3. Estimate time needed for each group

4. Identify any fixes that require server restart

Format as a clear step by step runbook that a 
system administrator can follow directly.
"""
        
        return self.analyze(prompt)
    
    def generate_executive_summary(self,
                                    hostname,
                                    compliance_score,
                                    total_checks,
                                    critical_findings,
                                    framework_coverage):
        """
        Generate executive summary for management
        Non technical language for board and management
        """
        
        prompt = f"""You are a cybersecurity consultant 
writing an executive summary for senior management.
This will be presented to the board of directors.

SERVER AUDITED: {hostname}
AUDIT DATE: {datetime.now().strftime('%Y-%m-%d')}
OVERALL COMPLIANCE SCORE: {compliance_score}%
TOTAL SECURITY CHECKS: {total_checks}
CRITICAL ISSUES FOUND: {len(critical_findings)}

COMPLIANCE FRAMEWORK SCORES:
{json.dumps(framework_coverage, indent=2)}

CRITICAL FINDINGS:
{json.dumps(critical_findings[:5], indent=2)}

Write a professional executive summary that:

1. Opens with a clear one sentence verdict on security posture
2. Explains the compliance score in business terms
3. Describes the top risks in plain English
   (no technical jargon - assume reader has no IT background)
4. States the business impact if issues are not fixed
5. Recommends 3 priority actions with timeline
6. Closes with next steps

Maximum 300 words.
Tone: Professional, clear, and direct.
Do not use technical terms without explanation.
"""
        
        return self.analyze(prompt)
    
    def analyze_trend(self, current_results, previous_results):
        """Compare current scan with previous scan"""
        
        current_score = round(
            sum(1 for r in current_results if r.get('status') == 'PASS') 
            / len(current_results) * 100, 1
        ) if current_results else 0
        
        previous_score = round(
            sum(1 for r in previous_results if r.get('status') == 'PASS') 
            / len(previous_results) * 100, 1
        ) if previous_results else 0
        
        score_change = current_score - previous_score
        
        current_fails = {
            r['control_id'] for r in current_results 
            if r.get('status') == 'FAIL'
        }
        previous_fails = {
            r['control_id'] for r in previous_results 
            if r.get('status') == 'FAIL'
        }
        
        new_failures = current_fails - previous_fails
        fixed_issues = previous_fails - current_fails
        
        prompt = f"""You are a cybersecurity analyst 
reviewing compliance trend data.

COMPLIANCE TREND ANALYSIS:
Previous Score: {previous_score}%
Current Score: {current_score}%
Change: {'+' if score_change >= 0 else ''}{score_change}%

NEW FAILURES SINCE LAST SCAN: {len(new_failures)}
Controls: {list(new_failures)}

ISSUES FIXED SINCE LAST SCAN: {len(fixed_issues)}
Controls: {list(fixed_issues)}

Provide:
1. Trend assessment - improving or deteriorating
2. Most concerning new failures
3. Recognition of fixes made
4. Recommendations going forward

Keep it concise and actionable.
Maximum 150 words.
"""
        
        return self.analyze(prompt)
    
    def suggest_remediation(self, control_id, 
                             description, 
                             current_value,
                             severity):
        """Get specific remediation for a single failed control"""
        
        prompt = f"""You are a Linux security expert.

This CIS benchmark control has FAILED:
Control ID: {control_id}
Description: {description}
Current Value Found: {current_value}
Severity: {severity}

Provide:
1. WHY this matters (one sentence, business impact)
2. EXACT commands to fix this on Ubuntu/Debian Linux
3. VERIFICATION command to confirm fix worked
4. Any RISKS or WARNINGS about making this change

Be specific and practical.
"""
        
        return self.analyze(prompt)
