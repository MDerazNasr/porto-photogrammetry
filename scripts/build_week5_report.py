#!/usr/bin/env python3
"""Build Mohamed's Fall 2026 Week 5 report and an internal QA PDF."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image as RLImage, ListFlowable, ListItem, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / "output/docx/Week 5 Report - Mohamed.docx"
PDF = ROOT / "output/pdf/Week 5 Report - Mohamed.pdf"
FIG = ROOT / "outputs/week5-results-summary-2026-10-02.png"
FISH = ROOT / "outputs/multicolor-fish-pipeline-previews-2026-10-02/fish01-GT_fish_Mchenga_male1_lowpoly_diffuse.1001.jpg"

NAVY = "1F4E79"
BLUE = "2E74B5"
GREY = "666666"
LIGHT = "F2F4F7"
IDENTITY = ["Mohamed Deraz Nasr", "HAAG Photogrammetry Project", "Fall 2026", "October 2, 2026"]

PROGRESS = [
    "Reviewed Ihor's coded-marker scale implementation and PR 19 against the colour-calibration branch. The scale protocol is complementary to PR 18 and has no direct file conflict, but I identified two edge cases that should be resolved before relying on its train/held-out split.",
    "Audited every locally available PLY and documented a dense-geometry validation protocol. The named VGGT/COLMAP files are sparse and the historical meshes are unlabeled, so none can support a defensible anatomical comparison; PACE was also unreachable during the check.",
    "Recovered real chart references for UF_Herp_3998 and UF_birds_ivory2 and compared the current linear 3 by 3 correction with a degree-2 root-polynomial model using leave-one-patch-out evaluation.",
    "Stress-tested the complete directory-calibration pipeline on eight real multicolour fish texture maps under two controlled camera responses. All 16 outputs completed with no skips or clipping increase.",
    "Updated the research database with Meeting 4, the available transcript excerpts, the latest Slack decisions, team reports, blockers, and the Week 6 handoff list.",
]

RESULTS = [
    ("Held-out chart predictions", "96", "2 specimens × 4 camera cases"),
    ("Linear mean held-out ΔE76", "2.573", "Current PR 18 method"),
    ("Root-polynomial mean ΔE76", "2.791", "+8.4% worse"),
    ("Fish textures / calibrated outputs", "8 / 16", "Two camera responses"),
    ("Fish mean foreground ΔE76", "3.136 → 0.158", "95.7% reduction"),
    ("Worst fish-case improvement", "89.2%", "All cases improved"),
    ("Clipping increase", "0.000 pp", "Both camera responses"),
]

BLOCKERS = [
    "Absolute calibration is still waiting on the physical ColorChecker manufacturer, model, and patch-value edition. A Slack follow-up was posted September 30; no confirmed identity was available by October 2.",
    "Dense geometry validation still needs a labeled, densely tessellated structured-light or CT reference paired with the same specimen's photographs. The current sparse-Delaunay result is only a coarse reconstruction check.",
    "The fish archive contains finished OBJ/texture assets, not raw camera photographs or chart frames. This week's fish result is therefore a controlled pipeline stress test, not an independent field-calibration result.",
]

PAPERS = [
    ("Neuralangelo: high-fidelity neural surfaces", "Li et al. combine multi-resolution hash grids, numerical gradients, and coarse-to-fine optimization to recover detailed surfaces from multi-view imagery. It is a strong quality-oriented candidate, but the project must verify how specimen masks and our COLMAP outputs enter its preprocessing path.", "Li, Z. et al. (2023). CVPR, 8456–8465. https://openaccess.thecvf.com/content/CVPR2023/html/Li_Neuralangelo_High-Fidelity_Neural_Surface_Reconstruction_CVPR_2023_paper.html"),
    ("NeuS: SDF reconstruction with volume rendering", "NeuS represents a surface as the zero level set of a signed distance function and introduces a volume-rendering formulation designed to reduce geometric bias. Although the paper can reconstruct without masks, our turntable backgrounds make a masked comparison important.", "Wang, P. et al. (2021). NeurIPS 34. https://proceedings.neurips.cc/paper_files/paper/2021/hash/e41e164f7485ec4a28741a2d0ea41c74-Abstract.html"),
    ("NeuS2: faster neural implicit surfaces", "NeuS2 adds multi-resolution hash encoding, CUDA implementation, and progressive training, reporting approximately two orders of magnitude faster training than NeuS. That speed makes it an attractive first masked baseline if its environment can be reproduced reliably.", "Wang, Y. et al. (2023). ICCV, 3295–3306. https://openaccess.thecvf.com/content/ICCV2023/html/Wang_NeuS2_Fast_Learning_of_Neural_Implicit_Surfaces_for_Multi-view_Reconstruction_ICCV_2023_paper.html"),
]

VERIFICATION = [
    ("Coded-marker integration review", "Ran the focused scale and mesh suites: 26 tests passed, 6 were skipped, and 3 unrelated failures came from macOS lacking os.sched_getaffinity. Flagged repeated short rings and one-ring captures as protocol edge cases."),
    ("Geometry-readiness audit", "Classified six historical dense-looking meshes as unlabeled and the named VGGT/COLMAP outputs as sparse. Preserved the earlier 33/36 registration comparison as coarse evidence only and wrote the exact future reference-mesh protocol."),
    ("Held-out colour-model comparison", "Used leave-one-patch-out predictions across two specimens and four non-reference camera cases. Root polynomial worsened mean ΔE76 by 0.217; the paired bootstrap 95% interval was −0.017 to +0.454, and three of four camera cases worsened."),
    ("Multicolour pipeline stress test", "Downsampled eight real 8192×8192 RGBA fish textures to 1024 pixels, retained alpha masks, synthesized two camera responses from real fitted matrices, and invoked the full production calibrate_directory path. All eight preview strips were visually inspected."),
    ("Project record and coordination", "Ingested the available Meeting 4 transcript excerpts and Slack sweep. Recorded Syed's request for a masked neural-implicit revisit, the need for publication-quality failure analysis, dataset-hosting decisions, and the agreed PR merge order."),
]

DECISIONS = [
    "Retain the linear 3 by 3 model in PR 18. The higher-order model did not show a reliable held-out gain and was worse on average.",
    "Use the fish result as evidence that the implementation handles high-resolution, multicolour RGBA assets and masks; do not present it as independent biological colour validation.",
    "Keep colour calibration, metric scale, and geometry validation as separate provenance-controlled stages, then test their interaction after each stage is individually accepted.",
    "Do not make dense or anatomical geometry claims until a paired structured-light/CT reference becomes available.",
]

ARTIFACTS = [
    ("Higher-order model report", "documentation/root-polynomial-held-out-comparison-2026-10-02.md"),
    ("Model comparison data", "outputs/color-model-held-out-comparison-2026-10-02.json"),
    ("Fish stress-test report", "documentation/multicolor-fish-pipeline-stress-test-2026-10-02.md"),
    ("Fish stress-test data", "outputs/multicolor-fish-pipeline-stress-test-2026-10-02.json"),
    ("Scale integration review", "documentation/coded-marker-scale-integration-review-2026-10-02.md"),
    ("Geometry readiness", "documentation/color-calibration-dense-geometry-readiness-2026-10-02.md"),
    ("Meeting and Slack record", "documentation/meeting4-transcript.md; documentation/slack/raw/refresh-2026-10-02.md"),
]

NEXT = [
    "Complete the reviewer/Slack handoff for PR 18, then rebase and resolve it after PRs 19, 17, and 20 land, following Syed's requested merge order.",
    "Confirm ownership with Syed and Om for the neural-implicit sweep; review Neuralangelo, NeuS2, NeuS, and newer candidates, then select one reproducible masked baseline.",
    "Review the recent dataset/benchmark papers Syed shortlisted and extract concrete failure-analysis, ablation, and qualitative-comparison requirements for our publication.",
    "Compare MorphoSource and Hugging Face for public release: supported formats, 3D preview, metadata, versioning, licenses, citations, and download ergonomics.",
    "Rerun absolute colour calibration when the chart edition is confirmed, and run dense reference-mesh validation when a matched specimen becomes available.",
]


def font(size, bold=False):
    names = ["Arial Bold.ttf", "Arial.ttf"] if bold else ["Arial.ttf"]
    for name in names:
        for base in ("/System/Library/Fonts/Supplemental", "/Library/Fonts"):
            p = Path(base) / name
            if p.exists():
                return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def build_figure():
    canvas = Image.new("RGB", (1800, 850), "white")
    d = ImageDraw.Draw(canvas)
    navy, orange, blue, grey = (31, 78, 121), (237, 125, 49), (91, 155, 213), (95, 95, 95)
    d.text((60, 35), "Week 5 validation summary", font=font(50, True), fill=navy)
    d.line((60, 105, 1740, 105), fill=navy, width=4)
    d.rounded_rectangle((60, 145, 865, 785), radius=22, fill=(242, 246, 250))
    d.text((95, 175), "Held-out chart error", font=font(38, True), fill=navy)
    d.text((95, 225), "Mean ΔE76 — lower is better", font=font(27), fill=grey)
    for i, (label, value, color) in enumerate((("Linear 3×3", 2.573, blue), ("Root polynomial", 2.791, orange))):
        y = 315 + i * 150
        d.text((95, y + 12), label, font=font(30), fill=(35, 35, 35))
        d.rounded_rectangle((350, y, 350 + int(value * 130), y + 62), radius=12, fill=color)
        d.text((730, y + 10), f"{value:.3f}", font=font(31, True), fill=navy)
    d.text((95, 660), "Decision", font=font(26), fill=grey)
    d.text((95, 704), "Retain the linear model", font=font(37, True), fill=navy)
    d.rounded_rectangle((905, 145, 1740, 785), radius=22, fill=(247, 247, 247))
    d.text((940, 175), "Multicolour fish stress test", font=font(38, True), fill=navy)
    d.text((940, 225), "Mean foreground ΔE76", font=font(27), fill=grey)
    for i, (label, value, color) in enumerate((("Before", 3.136, orange), ("After", 0.158, blue))):
        y = 315 + i * 150
        d.text((940, y + 12), label, font=font(30), fill=(35, 35, 35))
        d.rounded_rectangle((1130, y, 1130 + max(20, int(value * 155)), y + 62), radius=12, fill=color)
        d.text((1640, y + 10), f"{value:.3f}", font=font(31, True), fill=navy)
    d.text((940, 660), "95.7% reduction", font=font(42, True), fill=navy)
    d.text((940, 718), "8 textures · 16 outputs · no clipping increase", font=font(25), fill=grey)
    FIG.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(FIG, optimize=True)


def set_font(run, size=11, bold=False, italic=False, color=None):
    run.font.name = "Calibri"
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), "Calibri")
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), "Calibri")
    run.font.size, run.bold, run.italic = Pt(size), bold, italic
    if color: run.font.color.rgb = RGBColor.from_string(color)


def pf(p, before=0, after=6, line=1.10):
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = line


def shade(cell, fill):
    pr = cell._tc.get_or_add_tcPr(); shd = OxmlElement("w:shd"); shd.set(qn("w:fill"), fill); pr.append(shd)


def cell_margins(cell, top=80, start=120, bottom=80, end=120):
    pr = cell._tc.get_or_add_tcPr(); mar = OxmlElement("w:tcMar"); pr.append(mar)
    for side, val in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        x = OxmlElement(f"w:{side}"); x.set(qn("w:w"), str(val)); x.set(qn("w:type"), "dxa"); mar.append(x)


def set_table_geometry(table, widths):
    table.autofit = False
    pr = table._tbl.tblPr
    w = pr.first_child_found_in("w:tblW") or OxmlElement("w:tblW")
    if w.getparent() is None: pr.append(w)
    w.set(qn("w:w"), str(sum(widths))); w.set(qn("w:type"), "dxa")
    ind = OxmlElement("w:tblInd"); ind.set(qn("w:w"), "120"); ind.set(qn("w:type"), "dxa"); pr.append(ind)
    grid = table._tbl.tblGrid
    for child in list(grid): grid.remove(child)
    for width in widths:
        col = OxmlElement("w:gridCol"); col.set(qn("w:w"), str(width)); grid.append(col)
    for row in table.rows:
        for cell, width in zip(row.cells, widths):
            tcw = cell._tc.get_or_add_tcPr().first_child_found_in("w:tcW")
            tcw.set(qn("w:w"), str(width)); tcw.set(qn("w:type"), "dxa")


def add_identity(doc):
    for line in IDENTITY:
        p = doc.add_paragraph(); pf(p, after=0, line=1.0); set_font(p.add_run(line), 9.5, color=GREY)


def heading(doc, text, level=1):
    p = doc.add_paragraph(text, style=f"Heading {level}")
    return p


def bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet"); p.add_run(text); return p


def table(doc, headers, rows, widths):
    t = doc.add_table(rows=1, cols=len(headers)); t.alignment = WD_TABLE_ALIGNMENT.LEFT
    for i, (c, h) in enumerate(zip(t.rows[0].cells, headers)):
        shade(c, LIGHT); cell_margins(c); c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT if i == 0 else WD_ALIGN_PARAGRAPH.CENTER
        set_font(c.paragraphs[0].add_run(h), 9, True, color=NAVY)
    for row in rows:
        cells = t.add_row().cells
        for i, (c, value) in enumerate(zip(cells, row)):
            cell_margins(c); c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT if i == 0 else WD_ALIGN_PARAGRAPH.CENTER
            set_font(c.paragraphs[0].add_run(value), 9)
    set_table_geometry(t, widths)
    return t


def page(doc): doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def caption(doc, text):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; pf(p, 2, 8, 1.0); set_font(p.add_run(text), 9, italic=True, color=GREY)


def configure(doc):
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.left_margin = sec.right_margin = Inches(1)
    sec.top_margin = sec.bottom_margin = Inches(1)
    sec.header_distance = sec.footer_distance = Inches(0.492)
    normal = doc.styles["Normal"]; normal.font.name = "Calibri"; normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(6); normal.paragraph_format.line_spacing = 1.10
    for name, size, color, before, after in (("Heading 1",16,BLUE,16,8),("Heading 2",13,BLUE,12,6),("Heading 3",12,NAVY,8,4)):
        st = doc.styles[name]; st.font.name = "Calibri"; st.font.size = Pt(size); st.font.bold = True; st.font.color.rgb = RGBColor.from_string(color)
        st.paragraph_format.space_before = Pt(before); st.paragraph_format.space_after = Pt(after); st.paragraph_format.keep_with_next = True
    lst = doc.styles["List Bullet"]; lst.font.name = "Calibri"; lst.font.size = Pt(11)
    lst.paragraph_format.left_indent = Inches(.5); lst.paragraph_format.first_line_indent = Inches(-.25)
    lst.paragraph_format.space_after = Pt(8); lst.paragraph_format.line_spacing = 1.167
    header = sec.header.paragraphs[0]; header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_font(header.add_run("HAAG PHOTOGRAMMETRY · WEEK 5"), 8.5, True, color=GREY)
    footer = sec.footer.paragraphs[0]; footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_font(footer.add_run("Mohamed Deraz Nasr · Fall 2026"), 8.5, color=GREY)


def build_docx():
    doc = Document(); configure(doc); add_identity(doc)
    p = doc.add_paragraph(); pf(p, 20, 3); set_font(p.add_run("Week 5 Report"), 26, True, color=NAVY)
    p = doc.add_paragraph(); pf(p, 0, 14); set_font(p.add_run("Held-out colour-model selection and multicolour pipeline validation"), 12, color=GREY)
    heading(doc, "Progress this week")
    for x in PROGRESS: bullet(doc, x)
    heading(doc, "Key results", 2)
    table(doc, ("Metric", "Result", "Interpretation"), RESULTS, (4200, 2100, 3060))
    heading(doc, "Blockers and limits", 2)
    for x in BLOCKERS: bullet(doc, x)

    page(doc); add_identity(doc); heading(doc, "2. Literature review")
    p = doc.add_paragraph("Syed asked the team to revisit neural implicit reconstruction with background masking and to identify the level of analysis expected in recent dataset papers. These three methods define the immediate technical comparison."); pf(p)
    for title, summary, cite in PAPERS:
        heading(doc, title, 3)
        doc.add_paragraph(summary)
        p = doc.add_paragraph(); pf(p, 0, 8, 1.0); set_font(p.add_run("Citation: "), 9, True, color=GREY); set_font(p.add_run(cite), 9, color=GREY)

    page(doc); add_identity(doc); heading(doc, "3. What I did and how I verified it")
    for title, detail in VERIFICATION:
        heading(doc, title, 3); doc.add_paragraph(detail)
    heading(doc, "Workload", 2)
    doc.add_paragraph("The work represents approximately 20 hours: coded-marker integration review (4 h), geometry audit and protocol (3.5 h), held-out model evaluation (5 h), fish-asset recovery and stress testing (4 h), and Slack/database/documentation updates (3.5 h).")

    page(doc); add_identity(doc); heading(doc, "4. Results visualization")
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.add_run().add_picture(str(FIG), width=Inches(6.45))
    caption(doc, "Figure 1. The more complex root-polynomial model was worse on held-out chart patches, while the production pipeline sharply reduced controlled colour error across eight multicolour fish textures.")
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.add_run().add_picture(str(FISH), width=Inches(6.15))
    caption(doc, "Figure 2. Representative preview strip: target texture followed by camera-2 before/after and camera-3 before/after. This is a controlled stress test using real texture content, not an independent field capture.")

    page(doc); add_identity(doc); heading(doc, "5. Conclusions and decisions")
    for x in DECISIONS: bullet(doc, x)
    heading(doc, "Evidence and artifacts", 2)
    table(doc, ("Artifact", "Location"), ARTIFACTS, (2850, 6510))
    heading(doc, "Meeting and Slack decisions", 2)
    doc.add_paragraph("Meeting 4 records that publication will require more than a benchmark table: we need compelling failure analysis, ablations, and qualitative explanations of where methods fail. The dataset must also be public, with MorphoSource and Hugging Face as the current hosting candidates. Slack added a direct request to revisit Neuralangelo, NeuS2, NeuS, and newer methods with background masking. PR 18 should be updated after PRs 19, 17, and 20 land.")

    page(doc); add_identity(doc); heading(doc, "Next week")
    for x in NEXT: bullet(doc, x)
    heading(doc, "Definition of a showable outcome", 2)
    doc.add_paragraph("The target is a reviewable artifact rather than exploratory notes alone: a reproducible masked neural-implicit baseline with command, environment, specimen output, runtime, geometry/coverage metrics, failure cases, and a concise comparison against the current photogrammetry baseline. If data access remains blocked, the minimum deliverable is the completed method-selection memo plus an executable experiment plan and ownership agreement.")
    heading(doc, "Open confirmations", 2)
    for x in ("Who owns each neural-implicit implementation between Mohamed and Om?", "Which specimen and mask set should be the shared baseline?", "Which public host should be treated as primary, and what metadata/license schema is required?", "When will the chart edition and matched dense reference become available?"): bullet(doc, x)
    for shape, alt in zip(doc.inline_shapes, ("Two-panel chart comparing held-out colour model error and multicolour fish stress-test error.", "Representative five-panel multicolour fish pipeline preview.")):
        shape._inline.docPr.set("descr", alt); shape._inline.docPr.set("title", alt)
    doc.core_properties.title = "Week 5 Report"; doc.core_properties.author = "Mohamed Deraz Nasr"; doc.core_properties.subject = "HAAG Photogrammetry Project"
    DOCX.parent.mkdir(parents=True, exist_ok=True); doc.save(DOCX)


def build_pdf():
    base = getSampleStyleSheet()["Normal"]
    body = ParagraphStyle("body", parent=base, fontName="Helvetica", fontSize=9.6, leading=12, textColor=colors.HexColor("#222222"), spaceAfter=5)
    ident = ParagraphStyle("ident", parent=body, fontSize=8.8, leading=10, textColor=colors.HexColor("#666666"), spaceAfter=0)
    h1 = ParagraphStyle("h1", parent=body, fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=colors.HexColor("#2E74B5"), spaceBefore=14, spaceAfter=7)
    h2 = ParagraphStyle("h2", parent=h1, fontSize=12, leading=15, spaceBefore=9, spaceAfter=5)
    title = ParagraphStyle("title", parent=body, fontName="Helvetica-Bold", fontSize=26, leading=30, textColor=colors.HexColor("#1F4E79"), spaceBefore=18, spaceAfter=3)
    sub = ParagraphStyle("sub", parent=body, fontSize=11, textColor=colors.HexColor("#666666"), spaceAfter=12)
    cap = ParagraphStyle("cap", parent=body, fontSize=8.4, leading=10, alignment=1, textColor=colors.HexColor("#666666"), spaceAfter=6)
    def ids(s): s.extend(Paragraph(x, ident) for x in IDENTITY)
    def bullets(items): return ListFlowable([ListItem(Paragraph(x, body), leftIndent=18) for x in items], bulletType="bullet", leftIndent=18, bulletFontSize=8)
    def tab(headers, rows, widths):
        t=Table([list(headers)]+[list(r) for r in rows], colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#F2F4F7")),("TEXTCOLOR",(0,0),(-1,0),colors.HexColor("#1F4E79")),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTNAME",(0,1),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),7.7),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("GRID",(0,0),(-1,-1),.35,colors.HexColor("#C7CDD4")),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)])); return t
    story=[]; ids(story); story += [Paragraph("Week 5 Report",title),Paragraph("Held-out colour-model selection and multicolour pipeline validation",sub),Paragraph("Progress this week",h1),bullets(PROGRESS),Paragraph("Key results",h2),tab(("Metric","Result","Interpretation"),RESULTS,[2.8*inch,1.35*inch,2.35*inch]),Paragraph("Blockers and limits",h2),bullets(BLOCKERS)]
    story += [PageBreak()]; ids(story); story += [Paragraph("2. Literature review",h1),Paragraph("Syed asked the team to revisit neural implicit reconstruction with background masking and to identify the level of analysis expected in recent dataset papers.",body)]
    for a,b,c in PAPERS: story += [Paragraph(a,h2),Paragraph(b,body),Paragraph("<b>Citation:</b> "+c,ParagraphStyle("cite"+str(len(story)),parent=body,fontSize=8,leading=9.5,textColor=colors.HexColor("#666666")))]
    story += [PageBreak()]; ids(story); story += [Paragraph("3. What I did and how I verified it",h1)]
    for a,b in VERIFICATION: story += [Paragraph(a,h2),Paragraph(b,body)]
    story += [Paragraph("Workload",h2),Paragraph("Approximately 20 hours: scale review 4 h; geometry audit 3.5 h; model evaluation 5 h; fish stress test 4 h; project records 3.5 h.",body)]
    story += [PageBreak()]; ids(story); story += [Paragraph("4. Results visualization",h1),RLImage(str(FIG),6.35*inch,3.0*inch),Paragraph("Figure 1. Held-out model selection and multicolour pipeline stress results.",cap),RLImage(str(FISH),6.0*inch,3.0*inch),Paragraph("Figure 2. Representative controlled fish-texture preview strip.",cap)]
    story += [PageBreak()]; ids(story); story += [Paragraph("5. Conclusions and decisions",h1),bullets(DECISIONS),Paragraph("Evidence and artifacts",h2),tab(("Artifact","Location"),ARTIFACTS,[2.05*inch,4.45*inch]),Paragraph("Meeting and Slack decisions",h2),Paragraph("Publication needs failure analysis, ablations, and qualitative explanations—not only a benchmark table. The dataset must be public. Slack added a masked neural-implicit revisit, and PR 18 follows PRs 19, 17, and 20 in the merge order.",body)]
    story += [PageBreak()]; ids(story); story += [Paragraph("Next week",h1),bullets(NEXT),Paragraph("Definition of a showable outcome",h2),Paragraph("A reproducible masked neural-implicit baseline with command, environment, specimen output, runtime, geometry/coverage metrics, failure cases, and a concise comparison against the current photogrammetry baseline.",body),Paragraph("Open confirmations",h2),bullets(("Ownership split with Om.","Shared specimen and mask set.","Primary public host and metadata/license schema.","Chart edition and matched dense-reference availability."))]
    PDF.parent.mkdir(parents=True,exist_ok=True); SimpleDocTemplate(str(PDF),pagesize=letter,leftMargin=inch,rightMargin=inch,topMargin=.72*inch,bottomMargin=.72*inch,title="Week 5 Report",author="Mohamed Deraz Nasr").build(story)


if __name__ == "__main__":
    if not FISH.exists(): raise FileNotFoundError(FISH)
    build_figure(); build_docx(); build_pdf(); print(DOCX); print(PDF); print(FIG)
