import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle

def md_to_pdf(input_md_path, output_pdf_path):
    print(f"Converting {input_md_path} -> {output_pdf_path}...")
    with open(input_md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=18, leading=22,
        textColor=colors.HexColor('#1e3a8a'), spaceAfter=8
    )
    h1_style = ParagraphStyle(
        'H1', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=13, leading=16,
        textColor=colors.HexColor('#1e3a8a'), spaceBefore=12, spaceAfter=6
    )
    h2_style = ParagraphStyle(
        'H2', parent=styles['Heading3'],
        fontName='Helvetica-Bold', fontSize=11, leading=14,
        textColor=colors.HexColor('#0284c7'), spaceBefore=8, spaceAfter=4
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=12,
        textColor=colors.HexColor('#1e293b'), spaceAfter=4
    )
    code_style = ParagraphStyle(
        'Code', parent=styles['Code'],
        fontName='Courier', fontSize=7.5, leading=9.5,
        textColor=colors.HexColor('#334155'), backColor=colors.HexColor('#f1f5f9')
    )

    story = []

    in_code_block = False
    code_lines = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code_block:
                in_code_block = False
                code_text = "<br/>".join(code_lines)
                story.append(Paragraph(code_text, code_style))
                story.append(Spacer(1, 6))
                code_lines = []
            else:
                in_code_block = True
                code_lines = []
            continue

        if in_code_block:
            safe_l = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").rstrip()
            code_lines.append(safe_l)
            continue

        if not stripped:
            story.append(Spacer(1, 4))
            continue

        if stripped.startswith("# "):
            clean = stripped[2:].replace("**", "").replace("*", "")
            story.append(Paragraph(clean, title_style))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#3b82f6"), spaceAfter=8))
        elif stripped.startswith("## "):
            clean = stripped[3:].replace("**", "").replace("*", "")
            story.append(Paragraph(clean, h1_style))
        elif stripped.startswith("### "):
            clean = stripped[4:].replace("**", "").replace("*", "")
            story.append(Paragraph(clean, h2_style))
        elif stripped.startswith("---"):
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceBefore=4, spaceAfter=6))
        else:
            # Format basic bold / code cleanly without tag entanglement
            clean = stripped.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            # Replace code blocks with unique tokens first
            code_tokens = []
            def save_code(m):
                code_tokens.append(m.group(1))
                return f"___CODE_TOKEN_{len(code_tokens)-1}___"
            clean = re.sub(r'`(.+?)`', save_code, clean)
            clean = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', clean)
            for idx, ctext in enumerate(code_tokens):
                clean = clean.replace(f"___CODE_TOKEN_{idx}___", f'<font face="Courier" color="#0369a1">{ctext}</font>')
            story.append(Paragraph(clean, body_style))

    doc.build(story)
    print(f"  [✓] Successfully generated {output_pdf_path} ({os.path.getsize(output_pdf_path)} bytes)")

# Map empty or incomplete evidence phases to their respective markdown files
PHASE_MAPPINGS = [
    ("evidence/phase-01/phase-01-agile.pdf", "docs/phase-01-agile/agile-approach.md"),
    ("evidence/phase-03/phase-03-uml.pdf", "docs/phase-03-uml/use-cases.md"),
    ("evidence/phase-04/phase-04-data-flow.pdf", "docs/phase-04-data-flow/er-dfd-trust-boundaries.md"),
    ("evidence/phase-05/phase-05-architecture.pdf", "docs/phase-05-architecture/architecture.md"),
    ("evidence/phase-11/phase-11-secure-build.pdf", "docs/phase-11-secure-build/secure-build-sast.md"),
    ("evidence/phase-13/phase-13-docker-kubernetes.pdf", "docs/phase-13-docker-kubernetes/docker-kubernetes.md"),
    ("evidence/phase-14/phase-14-testing-cicd.pdf", "docs/phase-14-cicd-testing/testing-cicd.md")
]

for pdf_out, md_in in PHASE_MAPPINGS:
    os.makedirs(os.path.dirname(pdf_out), exist_ok=True)
    md_to_pdf(md_in, pdf_out)

print("[✓] All missing evidence PDFs generated successfully.")
