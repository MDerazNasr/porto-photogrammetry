# Meeting 2 Transcript and Notes

**Date:** September 4, 2026
**Project:** Open-source photogrammetry pipeline
**Source quality:** AI-generated transcript supplied after the meeting. The recording begins mid-discussion, speaker labels are missing, and several technical names were transcribed incorrectly. This document is an edited, speaker-agnostic record that preserves the substance without pretending uncertain wording is exact.

## Geometry validation and specimen stability

- Recreating an object's original geometry may be impossible if the physical specimen has moved or changed since the photographs were taken.
- The team can explain in the paper that its current validation is the best possible without recollecting the photography and reference data together.
- Wet specimens are particularly difficult. They may shrink, dry, flex, or change pose between photography and reference scanning. Even small changes, such as a displaced tail or limb, can produce a large geometric-distance error unrelated to reconstruction quality.
- Hanging and scanning a specimen in exactly the same configuration as the photogrammetry capture would be difficult and impractical.
- Image-side validation remains possible for wet specimens: omit held-out photographs and test novel-view reconstruction while the object is stable during a single photography session.
- Final mesh-to-reference geometry validation is much less defensible when the specimen has changed between sessions.
- Skeletal and other dry, rigid specimens should remain comparatively stable over time and are therefore the preferred initial benchmark.
- The current selection contains dry specimens, primarily skulls or skeletal material.
- The group agreed to begin with these dry specimens. Wet specimens and greater taxonomic diversity can be added opportunistically if new photography and surface scans can be collected together.
- Arthur will ask Zach about opportunities to collect new wet material, possibly connected to ongoing fish work, while the specimens are already being digitized.
- Anthropology collections could provide other hard objects, but human and international material introduces regulatory and access complications.
- Fossil data may also be difficult to release because collections can be protective of fossil scans.

## Dataset size and diversity

- Common reconstruction benchmarks often use relatively small numbers of scenes or objects.
- Tanks and Temples was described as commonly evaluated on approximately 15 meshes/scenes.
- SALVE was described as having only three or four wound specimens.
- DTU was described as having roughly 15–21 commonly used objects/scenes.
- The project has approximately 40 or 41 candidate specimens. The team believes this is quantitatively competitive if the specimens can all be obtained and processed.
- After confirming availability, the team can choose a diverse subset instead of treating all specimens identically.
- Desired diversity includes birds, mammals, dry reptiles, fossils where possible, and potentially wet specimens captured under a new controlled protocol.

## Pose estimation and view-count ablation

- COLMAP works well on the project's current turntable captures largely because adjacent photographs have substantial overlap.
- In sparse-view settings with only eight or nine views and little overlap, foundation models may outperform COLMAP.
- Models mentioned included VGGT, a newer VGGT-family or related model transcribed as “PGT Omega,” and another recent 3D model referenced through an Atlas evaluation. Exact model names need verification before citation.
- A proposed experiment is to reduce the number of input images and measure whether modern foundation models recover geometry better than COLMAP under limited overlap.
- The present capture protocol is highly idealized: the specimen is on a turntable and images are captured at roughly eight-degree intervals.
- View-count and overlap ablations could make the paper more useful by showing where classical and learned pose methods succeed or fail.

## Reference scanning and geometry evaluation

- Structured-light or surface scanning may be an especially appropriate reference because it measures the external surface without capturing internal anatomy.
- Specimens photographed in two passes, such as top and bottom orientations, can also be scanned in multiple passes and registered into a complete object.
- Artec scanner software can perform much of this registration automatically or semi-automatically.
- Large openings and tunnels in skulls, such as the foramen magnum, can produce uncertain scanner geometry because there is no directly visible surface through the passage.
- Scanner cleanup may be semi-automatic, with user refinement.
- If reference scanners provide confidence maps, evaluation may be restricted to high-confidence surface regions.
- Reference meshes and reconstructed meshes will still need alignment. Arthur is experienced with object registration and is not especially concerned about solving the alignment problem.
- RealityScan and similar tools allow manual metric scaling by selecting points with a known distance.
- Coded scale markers could potentially be recognized automatically in the pipeline.

## Metric scale and color calibration

- Existing photography includes color charts and scale markers.
- The group raised two contained software tasks:
  1. Restore or add color correction using the photographed color chart.
  2. Restore or add metric-scale calibration using coded scale markers.
- Color correction may be performed as preprocessing before reconstruction rather than inside every reconstruction backend.
- Automatic scale-marker recognition could provide models in real physical units and reduce dependence on post-hoc similarity scaling.
- Metric scale would make evaluation and downstream biological measurement more meaningful.
- Color is a major advantage of photogrammetry over CT and some surface-scanning workflows.
- Scanner vertex colors may be too low-resolution to serve as a strong texture reference. The team needs to determine whether scanner software offers useful UV-wrapped texture output.
- Existing evaluation practice emphasizes geometry. Novel-view metrics incorporate image/color fidelity, but the team needs to research how reconstructed color itself should be calibrated and evaluated.

## Direct analysis of Gaussian splats

- Another possible subproject is extracting useful information directly from Gaussian splats rather than first converting them into meshes.
- Potential targets include color measurements and other specimen attributes.
- This could preserve information that is lost or degraded during mesh extraction and texture transfer.
- It is a possible later subproject within the larger pipeline rather than the immediate onboarding task.

## Roles, coursework, and expected outputs

- Longer-standing researchers will spearhead the larger dataset and manuscript effort.
- Mohamed and Om are expected to contribute through smaller subprojects that integrate with the larger project, without being limited to purely supporting roles.
- Course requirements were discussed. The research-project course appears to require weekly reports and a final report similar to CS 8903, while master's-project or thesis work may require a more substantial independent deliverable. The exact course numbers and requirements should be verified rather than relying on the automated transcript.
- A significant software contribution or paper contribution can satisfy or support the final course deliverable.

## Guidance given directly to Mohamed

- Continue learning the codebase and understand how its stages connect.
- At the beginning of the semester, join concrete tasks that both help the project and force practical familiarity with the pipeline.
- Color calibration and metric-size calibration were recommended as strong initial subprojects.
- Start by building a solid foundation in the existing code, data, methods, and workflow.
- After becoming comfortable with the complete system, identify a larger independent direction that aligns with and strengthens the team's manuscript.
- Arthur encouraged independent thinking and exploration of personally interesting directions.
- The minimum shared goal is an open-source pipeline that produces 3D models of objects in natural-history collections.
- Broader directions are welcome, including direct use of Gaussian splats, color-aware analysis, collection digitization infrastructure, and downstream biological analysis.

## Mohamed's meeting update

Mohamed reported that he had:

- Spent the week reading reports and project overviews.
- Looked at papers, especially material related to COLMAP and reconstruction.
- Developed a general understanding of the project.
- Identified the need to study the codebase more deeply.
- Identified the need to request or confirm access to the datasets discussed by the team.

## Action items

### Mohamed — next week

1. Obtain and inspect the canonical codebase.
2. Trace how data moves through its major stages and document the relevant modules, inputs, outputs, configurations, and environments.
3. Confirm access to the photography, masks, scale/color charts, reference models, and compute/storage needed for development.
4. Investigate the current handling of color charts, color correction, coded scale markers, and metric scaling.
5. Select an initial integration task, with color calibration or size calibration as the recommended choices.
6. Define a small deliverable and acceptance test before implementing it.
7. Review literature on color calibration and color evaluation for photogrammetry/3D reconstruction.
8. Continue the weekly progress report, including evidence and blockers.

### Arthur

- Talk to Zach about dataset availability, collection of reference surface scans, possible wet specimens, and whether someone can collect or prepare the required models.

### Team

- Start with the available dry, rigid specimen set.
- Determine which of the approximately 40–41 candidates can actually be used.
- Explore diversity after availability is confirmed.
- Consider a view-count/overlap ablation comparing COLMAP with modern foundation models.
- Research color evaluation, scanner color/UV output, scale-marker support, and confidence-aware geometry comparison.

## Decisions versus proposals

### Agreed direction

- Begin with dry, rigid skeletal specimens for defensible geometry validation.
- Mohamed should first integrate into and understand the codebase.
- Color calibration and size calibration are suitable initial subprojects.
- Weekly reports and a final deliverable remain expected.

### Still proposed or unresolved

- Adding newly captured wet specimens.
- The final taxonomic composition and size of the benchmark.
- Fine-tuning foundation models.
- The limited-view/overlap ablation design.
- Whether Mohamed starts with color calibration or metric-scale calibration.
- How reconstructed color should be quantitatively evaluated.
- Direct measurement from Gaussian splats.
- The exact publication venue and submission schedule.
