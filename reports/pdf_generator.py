import json
import os
from datetime import datetime

class PDFReportGenerator:
    """
    Trinity6 PDF Report Generator
    Uses ReportLab to create professional
    compliance reports for clients
    """
    
    def __init__(self, results, output_dir="reports/output"):
        self.results = results
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Trinity6 Colors
        self.color_dark = (10/255, 14/255, 26/255)
        self.color_blue = (0/255, 212/255, 255/255)
        self.color_green = (0/255, 255/255, 153/255)
        self.color_red = (255/255, 68/255, 68/255)
        self.color_orange = (255/255, 170/255, 0/255)
        self.color_grey = (74/255, 106/255, 134/255)
        self.color_white = (1, 1, 1)
    
    def get_score_color(self, score):
        """Get color based on compliance score"""
        if score >= 80:
            return self.color_green
        elif score >= 60:
            return self.color_orange
        else:
            return self.color_red
    
    def generate(self, hostname):
        """Generate complete PDF report"""
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm
        from reportlab.pdfgen import canvas
        from reportlab.lib.colors import Color, HexColor
        
        score = self.results.get('compliance_score', {})
        critical = self.results.get('critical_findings', [])
        checks = self.results.get('checks', [])
        framework = self.results.get('framework_coverage', {})
        sections = self.results.get('section_summary', {})
        executive = self.results.get('executive_summary', '')
        
        compliance_score = score.get('score', 0)
        passed = score.get('passed', 0)
        failed = score.get('failed', 0)
        total = score.get('total', 0)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.output_dir}/trinity6_{hostname}_{timestamp}.pdf"
        
        width, height = A4
        c = canvas.Canvas(filename, pagesize=A4)
        
        # ==========================================
        # PAGE 1 - COVER PAGE
        # ==========================================
        
        # Dark background
        c.setFillColorRGB(*self.color_dark)
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        # Blue accent bar top
        c.setFillColorRGB(*self.color_blue)
        c.rect(0, height - 8*mm, width, 8*mm, fill=1, stroke=0)
        
        # Trinity6 Logo Text
        c.setFillColorRGB(*self.color_white)
        c.setFont("Helvetica-Bold", 36)
        c.drawString(20*mm, height - 50*mm, "TRINITY")
        c.setFillColorRGB(*self.color_blue)
        c.drawString(95*mm, height - 50*mm, "6")
        
        # Tagline
        c.setFillColorRGB(*self.color_grey)
        c.setFont("Helvetica", 10)
        c.drawString(20*mm, height - 58*mm, "INTELLIGENT SECURITY")
        
        # Report Title
        c.setFillColorRGB(*self.color_white)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(20*mm, height - 90*mm, "CIS Benchmark")
        c.drawString(20*mm, height - 100*mm, "Compliance Report")
        
        # Score Circle Area
        score_color = self.get_score_color(compliance_score)
        c.setFillColorRGB(*score_color)
        c.setFont("Helvetica-Bold", 72)
        c.drawString(20*mm, height - 155*mm, f"{compliance_score}%")
        
        c.setFillColorRGB(*self.color_grey)
        c.setFont("Helvetica", 12)
        c.drawString(20*mm, height - 165*mm, "OVERALL COMPLIANCE SCORE")
        
        # Stats Row
        c.setFillColorRGB(*self.color_green)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(20*mm, height - 190*mm, str(passed))
        c.setFillColorRGB(*self.color_grey)
        c.setFont("Helvetica", 9)
        c.drawString(20*mm, height - 196*mm, "PASSED")
        
        c.setFillColorRGB(*self.color_red)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(55*mm, height - 190*mm, str(failed))
        c.setFillColorRGB(*self.color_grey)
        c.setFont("Helvetica", 9)
        c.drawString(55*mm, height - 196*mm, "FAILED")
        
        c.setFillColorRGB(*self.color_blue)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(90*mm, height - 190*mm, str(total))
        c.setFillColorRGB(*self.color_grey)
        c.setFont("Helvetica", 9)
        c.drawString(90*mm, height - 196*mm, "TOTAL CHECKS")
        
        c.setFillColorRGB(*self.color_orange)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(130*mm, height - 190*mm, str(len(critical)))
        c.setFillColorRGB(*self.color_grey)
        c.setFont("Helvetica", 9)
        c.drawString(130*mm, height - 196*mm, "CRITICAL ISSUES")
        
        # Divider
        c.setStrokeColorRGB(*self.color_blue)
        c.setLineWidth(0.5)
        c.line(20*mm, height - 205*mm, width - 20*mm, height - 205*mm)
        
        # Report Details
        c.setFillColorRGB(*self.color_grey)
        c.setFont("Helvetica", 9)
        c.drawString(20*mm, height - 215*mm, f"Host: {hostname}")
        c.drawString(20*mm, height - 221*mm, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        c.drawString(20*mm, height - 227*mm, "Framework: CIS Benchmark v2.0")
        c.drawString(20*mm, height - 233*mm, "Generated by: Trinity6 AI Scanner")
        
        # Blue accent bar bottom
        c.setFillColorRGB(*self.color_blue)
        c.rect(0, 0, width, 8*mm, fill=1, stroke=0)
        
        c.setFillColorRGB(*self.color_dark)
        c.setFont("Helvetica", 8)
        c.drawString(20*mm, 3*mm, "trinity6.com  |  Intelligent Security  |  Confidential")
        
        c.showPage()
        
        # ==========================================
        # PAGE 2 - EXECUTIVE SUMMARY
        # ==========================================
        
        c.setFillColorRGB(*self.color_dark)
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        # Header bar
        c.setFillColorRGB(*self.color_blue)
        c.rect(0, height - 20*mm, width, 20*mm, fill=1, stroke=0)
        
        c.setFillColorRGB(*self.color_dark)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(20*mm, height - 13*mm, "TRINITY6  |  EXECUTIVE SUMMARY")
        
        # Section Title
        c.setFillColorRGB(*self.color_blue)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(20*mm, height - 35*mm, "Executive Summary")
        
        # Executive summary text
        c.setFillColorRGB(*self.color_white)
        c.setFont("Helvetica", 9)
        
        if executive:
            lines = []
            words = executive.split()
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                if len(test_line) < 90:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            
            y_pos = height - 45*mm
            for line in lines[:40]:
                c.drawString(20*mm, y_pos, line)
                y_pos -= 5*mm
        
        # Framework Coverage
        c.setFillColorRGB(*self.color_blue)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(20*mm, height - 155*mm, "Framework Coverage")
        
        y_fw = height - 165*mm
        for fw_name, fw_data in framework.items():
            fw_score = fw_data.get('score', 0)
            fw_color = self.get_score_color(fw_score)
            
            c.setFillColorRGB(*self.color_white)
            c.setFont("Helvetica", 9)
            c.drawString(20*mm, y_fw, fw_name)
            
            c.setFillColorRGB(*fw_color)
            c.setFont("Helvetica-Bold", 9)
            c.drawString(80*mm, y_fw, f"{fw_score}%")
            
            c.setFillColorRGB(*self.color_grey)
            c.setFont("Helvetica", 8)
            c.drawString(100*mm, y_fw,
                f"{fw_data.get('passed', 0)} passed / {fw_data.get('failed', 0)} failed")
            
            y_fw -= 7*mm
        
        # Footer
        c.setFillColorRGB(*self.color_blue)
        c.rect(0, 0, width, 8*mm, fill=1, stroke=0)
        c.setFillColorRGB(*self.color_dark)
        c.setFont("Helvetica", 8)
        c.drawString(20*mm, 3*mm, f"trinity6.com  |  {hostname}  |  Page 2")
        
        c.showPage()
        
        # ==========================================
        # PAGE 3 - CRITICAL FINDINGS
        # ==========================================
        
        c.setFillColorRGB(*self.color_dark)
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        c.setFillColorRGB(*self.color_blue)
        c.rect(0, height - 20*mm, width, 20*mm, fill=1, stroke=0)
        
        c.setFillColorRGB(*self.color_dark)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(20*mm, height - 13*mm, "TRINITY6  |  CRITICAL FINDINGS")
        
        c.setFillColorRGB(*self.color_red)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(20*mm, height - 35*mm, "Critical and High Severity Findings")
        
        y_pos = height - 50*mm
        
        if not critical:
            c.setFillColorRGB(*self.color_green)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(20*mm, y_pos, "No critical findings!")
        
        for finding in critical[:8]:
            if y_pos < 40*mm:
                break
            
            severity = finding.get('severity', '')
            sev_color = self.color_red if severity == 'Critical' else self.color_orange
            
            c.setFillColorRGB(*sev_color)
            c.rect(20*mm, y_pos - 2*mm, width - 40*mm, 7*mm, fill=1, stroke=0)
            
            c.setFillColorRGB(*self.color_dark)
            c.setFont("Helvetica-Bold", 9)
            c.drawString(22*mm, y_pos + 1*mm,
                f"{finding.get('control_id', '')}  |  {finding.get('title', '')[:60]}")
            
            y_pos -= 10*mm
            
            c.setFillColorRGB(*self.color_white)
            c.setFont("Helvetica", 8)
            c.drawString(22*mm, y_pos,
                f"Severity: {severity}")
            
            y_pos -= 5*mm
            
            remediation = finding.get('remediation', {})
            if isinstance(remediation, dict):
                rem_text = remediation.get('description', 'See documentation')
            else:
                rem_text = str(remediation)
            
            c.setFillColorRGB(*self.color_grey)
            c.drawString(22*mm, y_pos, f"Fix: {rem_text[:80]}")
            
            y_pos -= 10*mm
        
        c.setFillColorRGB(*self.color_blue)
        c.rect(0, 0, width, 8*mm, fill=1, stroke=0)
        c.setFillColorRGB(*self.color_dark)
        c.setFont("Helvetica", 8)
        c.drawString(20*mm, 3*mm, f"trinity6.com  |  {hostname}  |  Page 3")
        
        c.showPage()
        
        # ==========================================
        # PAGE 4 - SECTION SUMMARY
        # ==========================================
        
        c.setFillColorRGB(*self.color_dark)
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        c.setFillColorRGB(*self.color_blue)
        c.rect(0, height - 20*mm, width, 20*mm, fill=1, stroke=0)
        
        c.setFillColorRGB(*self.color_dark)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(20*mm, height - 13*mm, "TRINITY6  |  SECTION RESULTS")
        
        c.setFillColorRGB(*self.color_blue)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(20*mm, height - 35*mm, "CIS Benchmark Section Results")
        
        # Table header
        c.setFillColorRGB(*self.color_blue)
        c.rect(20*mm, height - 47*mm, width - 40*mm, 8*mm, fill=1, stroke=0)
        
        c.setFillColorRGB(*self.color_dark)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(22*mm, height - 43*mm, "SECTION")
        c.drawString(100*mm, height - 43*mm, "SCORE")
        c.drawString(120*mm, height - 43*mm, "PASSED")
        c.drawString(140*mm, height - 43*mm, "FAILED")
        c.drawString(160*mm, height - 43*mm, "TOTAL")
        
        y_pos = height - 55*mm
        row = 0
        
        for section, data in sections.items():
            sec_score = data.get('score', 0)
            sec_color = self.get_score_color(sec_score)
            
            if row % 2 == 0:
                c.setFillColorRGB(15/255, 23/255, 36/255)
                c.rect(20*mm, y_pos - 2*mm,
                    width - 40*mm, 7*mm, fill=1, stroke=0)
            
            c.setFillColorRGB(*self.color_white)
            c.setFont("Helvetica", 8)
            c.drawString(22*mm, y_pos, section[:45])
            
            c.setFillColorRGB(*sec_color)
            c.setFont("Helvetica-Bold", 8)
            c.drawString(100*mm, y_pos, f"{sec_score}%")
            
            c.setFillColorRGB(*self.color_green)
            c.drawString(120*mm, y_pos, str(data.get('passed', 0)))
            
            c.setFillColorRGB(*self.color_red)
            c.drawString(140*mm, y_pos, str(data.get('failed', 0)))
            
            c.setFillColorRGB(*self.color_white)
            c.drawString(160*mm, y_pos, str(data.get('total', 0)))
            
            y_pos -= 8*mm
            row += 1
        
        c.setFillColorRGB(*self.color_blue)
        c.rect(0, 0, width, 8*mm, fill=1, stroke=0)
        c.setFillColorRGB(*self.color_dark)
        c.setFont("Helvetica", 8)
        c.drawString(20*mm, 3*mm, f"trinity6.com  |  {hostname}  |  Page 4")
        
        c.showPage()
        
        # Save PDF
        c.save()
        print(f"PDF report saved to {filename}")
        return filename


if __name__ == "__main__":
    with open('results/sample.json', 'r') as f:
        results = json.load(f)
    
    generator = PDFReportGenerator(results)
    generator.generate('192.168.1.100')
