#!/usr/bin/env python3
"""Replace only the Week 5 DOCX literature-review paragraph text."""

from pathlib import Path
import sys
from tempfile import NamedTemporaryFile
from zipfile import ZIP_DEFLATED, ZipFile

from lxml import etree


DEFAULT_DOCX = Path(__file__).resolve().parents[1] / "output/docx/Week 5 Report - Mohamed.docx"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

REPLACEMENTS = {
    "Syed asked the team to revisit neural implicit reconstruction with background masking and to identify the level of analysis expected in recent dataset papers. These three methods define the immediate technical comparison.":
        "This week’s reading focused on the colour-correction choices tested in the implementation: when higher-order camera models are justified, how model complexity interacts with limited chart samples, and how colour differences should be interpreted. The literature motivated the held-out comparison rather than assuming that a more flexible model would be better.",
    "Neuralangelo: high-fidelity neural surfaces":
        "Root-polynomial colour correction",
    "Li et al. combine multi-resolution hash grids, numerical gradients, and coarse-to-fine optimization to recover detailed surfaces from multi-view imagery. It is a strong quality-oriented candidate, but the project must verify how specimen masks and our COLMAP outputs enter its preprocessing path.":
        "Finlayson et al. explain that ordinary polynomial colour correction can reduce fitted error but loses the exposure-scaling property of a linear 3 by 3 transform. Their root-polynomial terms retain exposure homogeneity while adding nonlinear capacity. This directly motivated the degree-2 model evaluated this week; our leave-one-patch-out result showed that the theoretical advantage did not generalize on the two available specimens, so the linear model was retained.",
    "Citation: Li, Z. et al. (2023). CVPR, 8456–8465. https://openaccess.thecvf.com/content/CVPR2023/html/Li_Neuralangelo_High-Fidelity_Neural_Surface_Reconstruction_CVPR_2023_paper.html":
        "Citation: Finlayson, G. D., Mackiewicz, M., & Hurlbert, A. (2015). Colour correction using root-polynomial regression. IEEE Transactions on Image Processing, 24(5), 1460–1470. https://doi.org/10.1109/TIP.2015.2405336",
    "NeuS: SDF reconstruction with volume rendering":
        "Polynomial camera characterization and sample support",
    "NeuS represents a surface as the zero level set of a signed distance function and introduces a volume-rendering formulation designed to reduce geometric bias. Although the paper can reconstruct without masks, our turntable backgrounds make a masked comparison important.":
        "Hong et al. study digital-camera characterization with polynomial models and examine how polynomial degree and the number of colour samples affect accuracy. The paper reinforces that additional terms must be supported by enough independent calibration data. With only one 24-patch chart per camera, this supported our decision to use held-out patches and a predeclared adoption gate instead of selecting the model with the lowest fitted error.",
    "Citation: Wang, P. et al. (2021). NeurIPS 34. https://proceedings.neurips.cc/paper_files/paper/2021/hash/e41e164f7485ec4a28741a2d0ea41c74-Abstract.html":
        "Citation: Hong, G., Luo, M. R., & Rhodes, P. A. (2001). A study of digital camera colorimetric characterization based on polynomial modeling. Color Research & Application, 26(1), 76–84. https://doi.org/10.1002/1520-6378(200102)26:1%3C76::AID-COL8%3E3.0.CO;2-3",
    "NeuS2: faster neural implicit surfaces":
        "Interpreting perceptual colour differences",
    "NeuS2 adds multi-resolution hash encoding, CUDA implementation, and progressive training, reporting approximately two orders of magnitude faster training than NeuS. That speed makes it an attractive first masked baseline if its environment can be reproduced reliably.":
        "Sharma et al. document the CIEDE2000 formula, implementation edge cases, and reference test data, showing why colour-difference results depend on the chosen metric and a verified implementation. We retained ΔE76 in this week’s experiment for continuity with the existing PR evidence, but reported the formula explicitly and treated the values as comparative errors rather than universal perceptual thresholds.",
    "Citation: Wang, Y. et al. (2023). ICCV, 3295–3306. https://openaccess.thecvf.com/content/ICCV2023/html/Wang_NeuS2_Fast_Learning_of_Neural_Implicit_Surfaces_for_Multi-view_Reconstruction_ICCV_2023_paper.html":
        "Citation: Sharma, G., Wu, W., & Dalal, E. N. (2005). The CIEDE2000 color-difference formula: Implementation notes, supplementary test data, and mathematical observations. Color Research & Application, 30(1), 21–30. https://doi.org/10.1002/col.20070",
}


def paragraph_text(paragraph):
    return "".join(paragraph.xpath(".//w:t/text()", namespaces=NS))


def replace_paragraph_text(paragraph, replacement):
    nodes = paragraph.xpath(".//w:t", namespaces=NS)
    if not nodes:
        raise RuntimeError("Target paragraph has no text nodes")
    if replacement.startswith("Citation: ") and len(nodes) >= 2:
        nodes[0].text = "Citation: "
        nodes[1].text = replacement.removeprefix("Citation: ")
        start = 2
    else:
        nodes[0].text = replacement
        start = 1
    for node in nodes[start:]:
        node.text = ""


def main():
    docx = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_DOCX
    with ZipFile(docx, "r") as source:
        entries = [(info, source.read(info.filename)) for info in source.infolist()]

    document_index = next(i for i, (info, _) in enumerate(entries) if info.filename == "word/document.xml")
    info, xml = entries[document_index]
    root = etree.fromstring(xml)

    found = set()
    for paragraph in root.xpath("//w:body/w:p", namespaces=NS):
        text = paragraph_text(paragraph)
        if text in REPLACEMENTS:
            replace_paragraph_text(paragraph, REPLACEMENTS[text])
            found.add(text)

    missing = set(REPLACEMENTS) - found
    if missing:
        raise RuntimeError(f"Expected literature-review paragraphs not found: {sorted(missing)}")

    entries[document_index] = (
        info,
        etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes"),
    )

    with NamedTemporaryFile(dir=docx.parent, suffix=".docx", delete=False) as tmp:
        temp_path = Path(tmp.name)
    try:
        with ZipFile(temp_path, "w") as output:
            for entry_info, data in entries:
                output.writestr(entry_info, data, compress_type=entry_info.compress_type or ZIP_DEFLATED)
        temp_path.replace(docx)
    finally:
        temp_path.unlink(missing_ok=True)

    print(f"Updated {len(found)} literature-review paragraphs in {docx}")


if __name__ == "__main__":
    main()
