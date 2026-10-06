#!/usr/bin/env python3
"""Build a Google Docs-targeted Week 4 photogrammetry report draft."""

from pathlib import Path
import sys

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/docx/Week 4 Report - Mohamed - Google Docs Draft.docx"
COMPARISON_IMAGE = ROOT / "outputs/color-calibration-batch-real-images-2026-09-22.jpg"
METRICS_IMAGE = ROOT / "outputs/week4-color-calibration-metrics.png"

SKILL_ROOT = Path(
    "/Users/mderaznasr/.codex/plugins/cache/openai-primary-runtime/"
    "documents/26.630.12135/skills/documents"
)
sys.path.insert(0, str(SKILL_ROOT / "scripts"))
from table_geometry import apply_table_geometry  # noqa: E402


BLACK = "000000"
MUTED = "555555"
BORDER = "DADCE0"


PROGRESS = [
    "Located and verified one genuine 24-patch colour-reference image for each of the three cameras in UF_Herp_3998.",
    "Tested the Imageomics histogram-matching pipeline on the real references and rejected it for production use because improved histogram agreement coincided with visible colour casts and worse patch error.",
    "Implemented augenblick color: it rectifies the chart, samples corresponding patches, fits a regularized 3 by 3 transform in linear RGB, and applies one transform per camera.",
    "Processed all 276 photographs and masks in UF_Herp_3998 with no skipped files while preserving dimensions, masks, and sampled EXIF metadata.",
    "Ran a controlled 36-image masked-COLMAP regression with identical images, masks, and settings except for colour calibration.",
]

RESULT_ROWS = [
    ("Camera 2 mean patch Delta E76 (lower is better)", "9.218", "3.131", "-66.0%"),
    ("Camera 3 mean patch Delta E76 (lower is better)", "3.698", "1.432", "-61.3%"),
    ("Registered images", "36 / 36", "36 / 36", "No change"),
    ("Verified feature inliers", "28,084", "28,658", "+2.0%"),
    ("Sparse points", "3,845", "3,929", "+2.2%"),
    ("Mean reprojection error (px; lower is better)", "0.670", "0.676", "+0.006"),
]

NEXT_WEEK = [
    "Add clipping measurements restricted to specimen masks and define a defensible warning threshold.",
    "Run the same colour and masked-COLMAP checks on a second specimen if per-camera reference-chart images are available.",
    "Confirm the ColorChecker make and patch-value edition before extending relative camera alignment to absolute calibration.",
    "Compare the 3 by 3 linear model with a higher-order method only if held-out evaluation shows a clear gain without clipping or colour casts.",
]

BLOCKERS = [
    (
        "Unknown chart edition",
        "Absolute calibration cannot yet be claimed; the current result is relative camera alignment.",
        "Confirm the physical chart make and patch-value edition.",
    ),
    (
        "Background-dominated clipping",
        "Whole-image clipping percentages cannot serve as an acceptance threshold.",
        "Compute clipping only inside each specimen mask.",
    ),
    (
        "Single-specimen validation",
        "The current evidence does not support a general claim across specimens or dense reconstruction.",
        "Repeat on another specimen and add a dense or mesh-level comparison.",
    ),
]

REFERENCES = [
    "[1] M. A. Barbero-Alvarez, S. Brenner, R. Sablatnig, and J. M. Menendez, “Preserving colour fidelity in photogrammetry,” Heritage, vol. 6, no. 8, pp. 5700-5718, 2023. https://doi.org/10.3390/heritage6080300",
    "[2] G. D. Finlayson, M. Mackiewicz, and A. Hurlbert, “Color correction using root-polynomial regression,” IEEE Transactions on Image Processing, vol. 24, no. 5, pp. 1460-1470, 2015. https://doi.org/10.1109/TIP.2015.2405336",
    "[3] Imageomics Institute, color-calibration software repository. https://github.com/Imageomics/color-calibration (accessed September 23, 2026).",
]


def set_font(run, size=11, *, bold=False, italic=False, color=BLACK):
    run.font.name = "Arial"
    rpr = run._element.get_or_add_rPr()
    fonts = rpr.get_or_add_rFonts()
    fonts.set(qn("w:ascii"), "Arial")
    fonts.set(qn("w:hAnsi"), "Arial")
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor.from_string(color)


def set_cell_border(cell, **edges):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge_name, attrs in edges.items():
        tag = f"w:{edge_name}"
        node = borders.find(qn(tag))
        if node is None:
            node = OxmlElement(tag)
            borders.append(node)
        for key, value in attrs.items():
            node.set(qn(f"w:{key}"), str(value))


def prevent_row_split(row):
    tr_pr = row._tr.get_or_add_trPr()
    node = OxmlElement("w:cantSplit")
    tr_pr.append(node)


def mark_header_row(row):
    tr_pr = row._tr.get_or_add_trPr()
    node = OxmlElement("w:tblHeader")
    node.set(qn("w:val"), "true")
    tr_pr.append(node)


def set_image_alt(inline_shape, description):
    doc_pr = inline_shape._inline.docPr
    doc_pr.set("descr", description)
    doc_pr.set("title", description)


def configure_styles(doc):
    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    normal.font.size = Pt(11)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(8)
    normal.paragraph_format.line_spacing = 1.15

    tokens = {
        "Heading 1": (20, 20, 6, BLACK),
        "Heading 2": (16, 18, 6, BLACK),
        "Heading 3": (14, 16, 4, "434343"),
    }
    for style_name, (size, before, after, color) in tokens.items():
        style = doc.styles[style_name]
        style.font.name = "Arial"
        style._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
        style._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
        style.font.size = Pt(size)
        style.font.bold = False
        style.font.color.rgb = RGBColor.from_string(color)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True

    bullet = doc.styles["List Bullet"]
    bullet.font.name = "Arial"
    bullet._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    bullet._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    bullet.font.size = Pt(11)
    bullet.paragraph_format.left_indent = Inches(0.5)
    bullet.paragraph_format.first_line_indent = Inches(-0.25)
    bullet.paragraph_format.space_after = Pt(4)
    bullet.paragraph_format.line_spacing = 1.15


def add_title(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    set_font(p.add_run("Week 4 Report"), 26)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    set_font(p.add_run("Colour calibration implementation and validation"), 14, color="434343")

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(14)
    set_font(
        p.add_run("Mohamed Deraz Nasr · HAAG Photogrammetry Project · Fall 2026 · September 25, 2026"),
        10,
        color=MUTED,
    )


def add_bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    set_font(p.add_run(text), 11)
    return p


def add_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = False
    set_font(p.add_run(text), 9.5, italic=True, color=MUTED)


def add_quiet_table(doc, headers, rows, widths_dxa, numeric_from=1):
    table = doc.add_table(rows=1, cols=len(headers))
    table.autofit = False
    all_rows = [headers] + rows
    for row_index, values in enumerate(all_rows):
        cells = table.rows[row_index].cells if row_index == 0 else table.add_row().cells
        prevent_row_split(table.rows[row_index])
        for col_index, (cell, value) in enumerate(zip(cells, values)):
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_index < numeric_from else WD_ALIGN_PARAGRAPH.CENTER
            set_font(p.add_run(str(value)), 9.5, bold=row_index == 0)
            set_cell_border(
                cell,
                bottom={"val": "single", "sz": "6", "color": BORDER},
            )
    mark_header_row(table.rows[0])
    apply_table_geometry(
        table,
        widths_dxa,
        table_width_dxa=9360,
        indent_dxa=0,
        cell_margins_dxa={"top": 80, "bottom": 80, "start": 120, "end": 120},
    )
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    return table


def add_labeled_paragraph(doc, label, text):
    p = doc.add_paragraph()
    p.paragraph_format.keep_together = True
    set_font(p.add_run(label + ": "), 11, bold=True)
    set_font(p.add_run(text), 11)


def add_page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def build():
    for path in (COMPARISON_IMAGE, METRICS_IMAGE):
        if not path.exists():
            raise FileNotFoundError(path)

    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.header_distance = Inches(0.492)
    section.footer_distance = Inches(0.492)
    configure_styles(doc)
    add_title(doc)

    doc.add_heading("1. Time Log and Executive Summary", level=1)
    add_labeled_paragraph(
        doc,
        "Bottom line",
        "A corresponding-patch linear colour transform passed the single-specimen pilot and preserved sparse reconstruction behaviour. Histogram matching was rejected because improved histogram agreement did not produce accurate or visually natural colour.",
    )

    doc.add_heading("Progress this week", level=2)
    for item in PROGRESS:
        add_bullet(doc, item)

    doc.add_heading("Key results", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    set_font(p.add_run("Table 1. Colour and sparse-reconstruction results for the controlled pilot."), 9.5, italic=True, color=MUTED)
    add_quiet_table(
        doc,
        ("Metric", "Original", "Calibrated", "Change"),
        RESULT_ROWS,
        (4680, 1560, 1560, 1560),
    )
    add_labeled_paragraph(
        doc,
        "Interpretation",
        "Patch error fell substantially for both non-reference cameras. All 36 images still registered after calibration, while inlier and sparse-point counts increased slightly. The 0.006 px reprojection-error change is small and should be treated as neutral rather than as an improvement.",
    )

    doc.add_heading("Next week", level=2)
    for item in NEXT_WEEK:
        add_bullet(doc, item)

    doc.add_heading("Blockers", level=2)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    set_font(p.add_run("Table 2. Current blockers, their impact, and the evidence needed to resolve them."), 9.5, italic=True, color=MUTED)
    add_quiet_table(
        doc,
        ("Blocker", "Impact", "Resolution"),
        BLOCKERS,
        (2160, 3600, 3600),
        numeric_from=3,
    )

    add_page_break(doc)
    doc.add_heading("2. Literature Review", level=1)

    doc.add_heading("Preserving colour fidelity in photogrammetry [1]", level=2)
    add_labeled_paragraph(
        doc,
        "Question and method",
        "Barbero-Alvarez et al. examine how acquisition, RAW development, colour spaces, chart-based calibration, and texture generation affect colour fidelity in cultural-heritage photogrammetry.",
    )
    add_labeled_paragraph(
        doc,
        "Finding",
        "Colour must be treated as a controlled and measurable property of the pipeline. Visual appearance alone is insufficient; known chart patches should be evaluated after processing.",
    )
    add_labeled_paragraph(
        doc,
        "Relevance",
        "This supports reporting patch error and clipping alongside qualitative before-and-after images, and it argues for preserving a reproducible record of every colour transformation.",
    )

    doc.add_heading("Root-polynomial colour correction [2]", level=2)
    add_labeled_paragraph(
        doc,
        "Question and method",
        "Finlayson et al. compare ordinary 3 by 3 linear correction with polynomial and root-polynomial alternatives for mapping camera RGB values to reference values.",
    )
    add_labeled_paragraph(
        doc,
        "Finding",
        "A linear transform is simple and exposure-independent. Ordinary polynomial terms may introduce exposure-dependent hue shifts, whereas root-polynomial terms retain exposure scaling while offering additional flexibility.",
    )
    add_labeled_paragraph(
        doc,
        "Relevance",
        "The pilot deliberately begins with the lower-complexity 3 by 3 model. A higher-order method should only replace it if held-out chart patches show a meaningful gain without increased clipping or visible artefacts.",
    )

    doc.add_heading("Imageomics colour-calibration software [3]", level=2)
    add_labeled_paragraph(
        doc,
        "Method",
        "The Imageomics package uses segmented colour cards and per-channel histogram matching to normalize a target image to a reference image.",
    )
    add_labeled_paragraph(
        doc,
        "Evaluation",
        "On the museum reference images, histogram distances improved but patch accuracy and full-image appearance did not improve consistently. Visible colour casts appeared in corrected images.",
    )
    add_labeled_paragraph(
        doc,
        "Decision",
        "Histogram matching was rejected for the current capture process. Corresponding chart patches provide a stronger calibration signal because the optimization is tied to known colour locations rather than only to global channel distributions.",
    )

    add_page_break(doc)
    doc.add_heading("3. What I Did and How I Verified It", level=1)

    doc.add_heading("3.1 Located the usable reference data", level=2)
    add_labeled_paragraph(doc, "Objective", "Determine whether the specimen archive contained a real colour reference for each camera.")
    add_labeled_paragraph(doc, "Method", "Searched the repository and archived specimen data, then visually checked the candidate frames and masks.")
    add_labeled_paragraph(doc, "Evidence", "One genuine 24-patch chart frame was confirmed for each of cameras 1, 2, and 3 in UF_Herp_3998.")
    add_labeled_paragraph(doc, "Decision", "Use camera 1 as the relative target until the physical chart model and reference-value edition are confirmed.")

    doc.add_heading("3.2 Evaluated the existing Imageomics approach", level=2)
    add_labeled_paragraph(doc, "Objective", "Test whether the available open-source pipeline could be adopted directly.")
    add_labeled_paragraph(doc, "Method", "Ran the software on explicit chart masks and compared channel histograms, chart-patch error, and the appearance of full corrected images.")
    add_labeled_paragraph(doc, "Evidence", "Histogram convergence improved, but camera 2 patch error rose from 12.39 to 17.99 Delta E76 and the corrected images showed visible casts. Camera 3 improved only modestly, from 25.61 to 23.05.")
    add_labeled_paragraph(doc, "Decision", "Reject histogram matching as the production method for this dataset.")

    doc.add_heading("3.3 Implemented corresponding-patch calibration", level=2)
    add_labeled_paragraph(doc, "Objective", "Align the three cameras using measurements from corresponding chart patches.")
    add_labeled_paragraph(doc, "Method", "Rectify each chart from four reviewed corners, sample the 24 patch interiors, convert RGB values to linear light, and fit one regularized 3 by 3 transform per non-reference camera.")
    add_labeled_paragraph(doc, "Evidence", "Camera 2 mean patch error fell from 9.218 to 3.131 Delta E76 and camera 3 fell from 3.698 to 1.432.")
    add_labeled_paragraph(doc, "Decision", "Accept the linear relative-calibration method for wider testing while retaining the unmodified originals.")

    doc.add_heading("3.4 Validated file preservation and reconstruction behaviour", level=2)
    add_labeled_paragraph(doc, "Objective", "Ensure that calibration does not damage the dataset contract or destabilize sparse reconstruction.")
    add_labeled_paragraph(doc, "Method", "Processed all 276 image-mask pairs and ran original versus calibrated masked-COLMAP reconstructions on the same 36-image subset.")
    add_labeled_paragraph(doc, "Evidence", "No photographs were skipped; reference-camera files and masks remained byte-identical; corrected JPEG dimensions and sampled EXIF fields were preserved. Both COLMAP runs registered 36 of 36 images.")
    add_labeled_paragraph(doc, "Decision", "The pilot passes the file-integrity and sparse-reconstruction gate. Dense or mesh-level evaluation remains future work.")

    add_page_break(doc)
    doc.add_heading("4. Results Visualization", level=1)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    shape = p.add_run().add_picture(str(COMPARISON_IMAGE), width=Inches(4.75))
    set_image_alt(shape, "Representative original and calibrated museum specimen images from three cameras")
    add_caption(
        doc,
        "Figure 1. Representative images from the three-camera batch before and after corresponding-patch calibration. The accepted method reduces cross-camera disagreement without the visible cast produced by histogram matching.",
    )

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    shape = p.add_run().add_picture(str(METRICS_IMAGE), width=Inches(6.5))
    set_image_alt(shape, "Chart showing patch colour-error reductions and masked-COLMAP regression metrics")
    add_caption(
        doc,
        "Figure 2. Calibration reduced mean chart-patch Delta E76 by 66.0% for camera 2 and 61.3% for camera 3. The controlled masked-COLMAP regression retained 36 of 36 registrations and changed sparse reconstruction metrics only slightly.",
    )

    add_page_break(doc)
    doc.add_heading("5. Conclusions and Decisions", level=1)
    conclusions = [
        "Adopt corresponding-patch, per-camera linear calibration as the current pilot method.",
        "Do not adopt per-channel histogram matching for this dataset; histogram agreement was not a reliable proxy for colour accuracy.",
        "Describe the current output as relative camera alignment, not absolute calibration, until the chart edition is confirmed.",
        "Treat sparse reconstruction as preserved rather than improved; the small metric changes do not establish a geometric benefit.",
        "Require specimen-mask clipping, a second specimen, and dense or mesh-level evaluation before making a general production recommendation.",
    ]
    for item in conclusions:
        add_bullet(doc, item)

    doc.add_heading("Evidence and artifacts", level=2)
    artifacts = [
        ("Pilot and decision record", "documentation/color-calibration-pilot-2026-09-21.md"),
        ("Implementation", "team-repo/src/augenblick/preparation/color.py"),
        ("Example configuration", "team-repo/examples/color/uf_herp_3998.json"),
        ("Full-batch evidence", "outputs/color-calibration-report-uf-herp3998-full-2026-09-22.json"),
        ("COLMAP regression", "outputs/color-calibration-colmap-regression-2026-09-22.json"),
        ("Visual comparison", "outputs/color-calibration-batch-real-images-2026-09-22.jpg"),
    ]
    for label, path in artifacts:
        add_labeled_paragraph(doc, label, path)

    doc.add_heading("6. References", level=1)
    for reference in REFERENCES:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        p.paragraph_format.space_after = Pt(8)
        set_font(p.add_run(reference), 10)

    doc.core_properties.title = "Week 4 Report - Colour Calibration"
    doc.core_properties.author = "Mohamed Deraz Nasr"
    doc.core_properties.subject = "HAAG Photogrammetry Project"
    doc.core_properties.keywords = "photogrammetry, colour calibration, ColorChecker, COLMAP"

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    build()
