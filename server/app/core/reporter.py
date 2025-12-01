import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from typing import Dict, Any

class PDFReporter:
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_report(self, scan_data: Dict[str, Any]) -> str:
        """Generate a PDF report for a scan and return the file path."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"vulnora_report_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)

        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title_style = styles['Title']
        story.append(Paragraph("Vulnora AI Security Report", title_style))
        story.append(Spacer(1, 12))

        # Scan Summary
        story.append(Paragraph("Scan Summary", styles['Heading2']))
        summary_data = [
            ["Project Path", scan_data.get("project_path", "N/A")],
            ["Scan Date", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ["Smell Score", f"{scan_data.get('smell_score', 0):.2f} / 100"],
            ["Files Scanned", str(scan_data.get("files_scanned", 0))],
            ["Total Issues", str(len(scan_data.get("issues", [])))]
        ]
        
        t = Table(summary_data, colWidths=[150, 300])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(t)
        story.append(Spacer(1, 24))

        # Issues Detail
        story.append(Paragraph("Detailed Findings", styles['Heading2']))
        
        issues = scan_data.get("issues", [])
        if not issues:
            story.append(Paragraph("No vulnerabilities found. Great job!", styles['Normal']))
        else:
            for i, issue in enumerate(issues, 1):
                # Issue Header
                header_text = f"#{i} [{issue.get('severity', 'Medium')}] {issue.get('vulnerability_type', 'Unknown')}"
                story.append(Paragraph(header_text, styles['Heading3']))
                
                # Issue Details
                details = [
                    f"<b>File:</b> {issue.get('file_path', 'N/A')}:{issue.get('line_number', 0)}",
                    f"<b>Description:</b> {issue.get('description', 'N/A')}",
                    f"<b>Suggested Fix:</b> {issue.get('suggested_fix', 'N/A')}"
                ]
                
                for detail in details:
                    story.append(Paragraph(detail, styles['Normal']))
                    story.append(Spacer(1, 6))
                
                # Code Snippet
                snippet = issue.get('snippet', '')
                if snippet:
                    story.append(Paragraph("<b>Vulnerable Code:</b>", styles['Normal']))
                    code_style = ParagraphStyle('Code', parent=styles['Code'], backColor=colors.whitesmoke, borderPadding=5)
                    story.append(Paragraph(f"<font face='Courier'>{snippet}</font>", code_style))
                
                story.append(Spacer(1, 12))
                story.append(Paragraph("-" * 60, styles['Normal']))
                story.append(Spacer(1, 12))

        doc.build(story)
        return filepath
