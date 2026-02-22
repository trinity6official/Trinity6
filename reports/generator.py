import json
import os
from datetime import datetime

class ReportGenerator:
    """
    Trinity6 Report Generator
    Generates professional compliance reports
    in HTML and JSON formats
    PDF support coming in Phase 2
    """
    
    def __init__(self, results, output_dir="reports/output"):
        self.results = results
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_html_report(self, hostname):
        """Generate professional HTML report"""
        
        score = self.results.get('compliance_score', {})
        critical = self.results.get('critical_findings', [])
        checks = self.results.get('checks', [])
        framework = self.results.get('framework_coverage', {})
        sections = self.results.get('section_summary', {})
        ai_analysis = self.results.get('ai_analysis', '')
        executive = self.results.get('executive_summary', '')
        
        passed = score.get('passed', 0)
        failed = score.get('failed', 0)
        total = score.get('total', 0)
        compliance_score = score.get('score', 0)
        
        if compliance_score >= 80:
            score_color = "#00ff99"
            score_status = "GOOD"
        elif compliance_score >= 60:
            score_color = "#ffaa00"
            score_status = "NEEDS IMPROVEMENT"
        else:
            score_color = "#ff4444"
            score_status = "CRITICAL"
        
        failed_checks = [
            c for c in checks 
            if c.get('status') == 'FAIL'
        ]
        passed_checks = [
            c for c in checks 
            if c.get('status') == 'PASS'
        ]
        
        framework_html = ""
        for fw, data in framework.items():
            fw_score = data.get('score', 0)
            fw_color = "#00ff99" if fw_score >= 80 else "#ffaa00" if fw_score >= 60 else "#ff4444"
            framework_html += f"""
            <div class="framework-card">
                <h3>{fw}</h3>
                <div class="fw-score" style="color:{fw_color}">
                    {fw_score}%
                </div>
                <div class="fw-detail">
                    {data.get('passed', 0)} passed / 
                    {data.get('failed', 0)} failed
                </div>
            </div>
            """
        
        section_html = ""
        for section, data in sections.items():
            sec_score = data.get('score', 0)
            sec_color = "#00ff99" if sec_score >= 80 else "#ffaa00" if sec_score >= 60 else "#ff4444"
            section_html += f"""
            <tr>
                <td>{section}</td>
                <td style="color:{sec_color}">{sec_score}%</td>
                <td style="color:#00ff99">{data.get('passed', 0)}</td>
                <td style="color:#ff4444">{data.get('failed', 0)}</td>
                <td>{data.get('total', 0)}</td>
            </tr>
            """
        
        critical_html = ""
        for finding in critical:
            critical_html += f"""
            <div class="critical-card">
                <div class="finding-header">
                    <span class="control-id">{finding.get('control_id', '')}</span>
                    <span class="severity severity-{finding.get('severity', '').lower()}">
                        {finding.get('severity', '')}
                    </span>
                </div>
                <div class="finding-title">{finding.get('title', '')}</div>
                <div class="finding-detail">
                    <strong>Current Value:</strong> 
                    {finding.get('output', 'N/A')}
                </div>
                <div class="finding-remediation">
                    <strong>Fix:</strong> 
                    <code>{finding.get('remediation', {}).get('description', 'See documentation')}</code>
                </div>
            </div>
            """
        
        failed_html = ""
        for check in failed_checks:
            failed_html += f"""
            <tr class="fail-row">
                <td><span class="control-id">{check.get('control_id', '')}</span></td>
                <td>{check.get('title', '')}</td>
                <td><span class="severity severity-{check.get('severity', '').lower()}">{check.get('severity', '')}</span></td>
                <td><span class="status-fail">FAIL</span></td>
                <td><code>{check.get('output', '')[:50]}</code></td>
            </tr>
            """
        
        passed_html = ""
        for check in passed_checks:
            passed_html += f"""
            <tr class="pass-row">
                <td><span class="control-id">{check.get('control_id', '')}</span></td>
                <td>{check.get('title', '')}</td>
                <td><span class="severity severity-{check.get('severity', '').lower()}">{check.get('severity', '')}</span></td>
                <td><span class="status-pass">PASS</span></td>
                <td><code>{check.get('output', '')[:50]}</code></td>
            </tr>
            """
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trinity6 Compliance Report - {hostname}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: #0a0e1a;
            color: #e0e6f0;
            padding: 40px 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 1px solid #1e2f42;
        }}
        .logo {{
            font-size: 1.5rem;
            font-weight: 900;
            color: #ffffff;
            letter-spacing: 3px;
        }}
        .logo span {{ color: #00d4ff; }}
        .report-meta {{
            text-align: right;
            color: #4a6a86;
            font-size: 0.8rem;
        }}
        
        .score-hero {{
            background: #0f1724;
            border: 1px solid #1e2f42;
            border-radius: 16px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
        }}
        .score-circle {{
            font-size: 5rem;
            font-weight: 900;
            color: {score_color};
            line-height: 1;
            margin: 20px 0;
        }}
        .score-status {{
            font-size: 1rem;
            letter-spacing: 3px;
            color: {score_color};
            margin-bottom: 20px;
        }}
        .score-breakdown {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 20px;
        }}
        .score-stat {{ text-align: center; }}
        .score-stat .number {{
            font-size: 2rem;
            font-weight: 700;
        }}
        .score-stat .label {{
            font-size: 0.75rem;
            color: #4a6a86;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .passed {{ color: #00ff99; }}
        .failed {{ color: #ff4444; }}
        .total {{ color: #00d4ff; }}
        
        .section-title {{
            font-size: 0.75rem;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: #00d4ff;
            margin-bottom: 16px;
            margin-top: 40px;
        }}
        
        .framework-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 16px;
            margin-bottom: 30px;
        }}
        .framework-card {{
            background: #0f1724;
            border: 1px solid #1e2f42;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }}
        .framework-card h3 {{
            font-size: 0.8rem;
            color: #7a8fa6;
            margin-bottom: 8px;
        }}
        .fw-score {{
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 4px;
        }}
        .fw-detail {{
            font-size: 0.7rem;
            color: #4a6a86;
        }}
        
        .executive-box {{
            background: linear-gradient(135deg, #0d1528, #150d2a);
            border: 1px solid #7b2ff733;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            white-space: pre-wrap;
            line-height: 1.8;
            color: #c0c8d8;
            font-size: 0.9rem;
        }}
        
        .ai-box {{
            background: #0f1724;
            border: 1px solid #00d4ff22;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            white-space: pre-wrap;
            line-height: 1.8;
            color: #c0c8d8;
            font-size: 0.85rem;
        }}
        
        .critical-card {{
            background: #1a0f0f;
            border: 1px solid #ff444433;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 12px;
        }}
        .finding-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
        }}
        .control-id {{
            font-family: monospace;
            color: #00d4ff;
            font-size: 0.85rem;
        }}
        .severity {{
            padding: 2px 10px;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 1px;
        }}
        .severity-critical {{
            background: #ff000033;
            color: #ff4444;
        }}
        .severity-high {{
            background: #ff444433;
            color: #ff8800;
        }}
        .severity-medium {{
            background: #ffaa0033;
            color: #ffaa00;
        }}
        .severity-low {{
            background: #00ff9933;
            color: #00ff99;
        }}
        .finding-title {{
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 8px;
        }}
        .finding-detail {{
            font-size: 0.8rem;
            color: #4a6a86;
            margin-bottom: 6px;
        }}
        .finding-remediation {{
            font-size: 0.8rem;
            color: #7a8fa6;
        }}
        .finding-remediation code {{
            background: #0a0e1a;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.75rem;
            color: #00ff99;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
            font-size: 0.82rem;
        }}
        th {{
            background: #0f1724;
            padding: 12px 16px;
            text-align: left;
            color: #00d4ff;
            font-size: 0.75rem;
            letter-spacing: 1px;
            text-transform: uppercase;
            border-bottom: 1px solid #1e2f42;
        }}
        td {{
            padding: 10px 16px;
            border-bottom: 1px solid #0f1724;
            color: #7a8fa6;
        }}
        .fail-row td {{ background: #1a0a0a; }}
        .pass-row td {{ background: #0a1a0a; }}
        
        .status-pass {{
            color: #00ff99;
            font-weight: 700;
        }}
        .status-fail {{
            color: #ff4444;
            font-weight: 700;
        }}
        
        code {{
            font-family: monospace;
            background: #0a0e1a;
            padding: 2px 6px;
            border-radius: 4px;
            color: #00d4ff;
        }}
        
        footer {{
            text-align: center;
            padding: 30px;
            color: #1e2f42;
            font-size: 0.75rem;
            border-top: 1px solid #1e2f42;
            margin-top: 40px;
        }}
        
        @media print {{
            body {{ background: white; color: black; }}
        }}
    </style>
</head>
<body>
<div class="container">

    <header>
        <div class="logo">TRINITY<span>6</span></div>
        <div class="report-meta">
            <div>CIS Benchmark Compliance Report</div>
            <div>Host: {hostname}</div>
            <div>Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
            <div>Framework: CIS Benchmark v2.0</div>
        </div>
    </header>

    <div class="score-hero">
        <div style="color:#7a8fa6;font-size:0.8rem;
        letter-spacing:2px;text-transform:uppercase">
            Overall Compliance Score
        </div>
        <div class="score-circle">{compliance_score}%</div>
        <div class="score-status">{score_status}</div>
        <div class="score-breakdown">
            <div class="score-stat">
                <div class="number passed">{passed}</div>
                <div class="label">Passed</div>
            </div>
            <div class="score-stat">
                <div class="number failed">{failed}</div>
                <div class="label">Failed</div>
            </div>
            <div class="score-stat">
                <div class="number total">{total}</div>
                <div class="label">Total Checks</div>
            </div>
            <div class="score-stat">
                <div class="number" style="color:#ff8800">
                    {len(critical)}
                </div>
                <div class="label">Critical Issues</div>
            </div>
        </div>
    </div>

    <p class="section-title">Framework Coverage</p>
    <div class="framework-grid">
        {framework_html}
    </div>

    <p class="section-title">Executive Summary</p>
    <div class="executive-box">{executive if executive else 'AI analysis not available'}</div>

    <p class="section-title">Section by Section Results</p>
    <table>
        <tr>
            <th>Section</th>
            <th>Score</th>
            <th>Passed</th>
            <th>Failed</th>
            <th>Total</th>
        </tr>
        {section_html}
    </table>

    <p class="section-title">Critical and High Findings</p>
    {critical_html if critical_html else 
     '<div style="color:#00ff99;padding:20px">No critical findings!</div>'}

    <p class="section-title">AI Security Analysis</p>
    <div class="ai-box">{ai_analysis if ai_analysis else 'AI analysis not available'}</div>

    <p class="section-title">All Failed Controls</p>
    <table>
        <tr>
            <th>Control ID</th>
            <th>Description</th>
            <th>Severity</th>
            <th>Status</th>
            <th>Current Value</th>
        </tr>
        {failed_html}
    </table>

    <p class="section-title">All Passed Controls</p>
    <table>
        <tr>
            <th>Control ID</th>
            <th>Description</th>
            <th>Severity</th>
            <th>Status</th>
            <th>Value</th>
        </tr>
        {passed_html}
    </table>

    <footer>
        © {datetime.now().year} Trinity6 · 
        Intelligent Security · trinity6.com · 
        Report generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </footer>

</div>
</body>
</html>"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.output_dir}/trinity6_{hostname}_{timestamp}.html"
        
        with open(filename, 'w') as f:
            f.write(html)
        
        print(f"HTML report saved to {filename}")
        return filename
    
    def generate_json_report(self, hostname):
        """Generate JSON report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.output_dir}/trinity6_{hostname}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"JSON report saved to {filename}")
        return filename
    
    def generate_all(self, hostname):
        """Generate all report formats"""
        print(f"\nGenerating Trinity6 reports for {hostname}...")
        
        html_file = self.generate_html_report(hostname)
        json_file = self.generate_json_report(hostname)
        
        print(f"\nReports generated:")
        print(f"  HTML: {html_file}")
        print(f"  JSON: {json_file}")
        
        return {
            'html': html_file,
            'json': json_file
        }


if __name__ == "__main__":
    with open('results/sample.json', 'r') as f:
        results = json.load(f)
    
    generator = ReportGenerator(results)
    generator.generate_all('192.168.1.100')
