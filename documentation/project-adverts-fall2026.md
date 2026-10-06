# HAAG project adverts, Fall 2026

| Lead | Project |
|---|---|
| Dr. Ben Freeman | [Behavior Analysis of Hume's Leaf Warbler Bird from Camera Traps](#behavior-analysis-of-humes-leaf-warbler-bird-from-camera-traps) |
| Dr. James Stroud | [Automation of Lizard Landmark Analysis](#automation-of-lizard-landmark-analysis) |
| Dr. Ben Freeman | [Audio Analysis of Hume's Leaf Warbler](#audio-analysis-of-humes-leaf-warbler) |
| Dr. Arthur Porto | [Photogrammetry Project](#photogrammetry-project) |
| Dr. Jenny McGuire | [Detection of Wildlife from Camera Traps at Stone Mountain](#detection-of-wildlife-from-camera-traps-at-stone-mountain) |
| Dr. Anind Dey | [AI for Mental Health Sensing](#ai-for-mental-health-sensing) |
| Dr. Steve Mussmann | [Data Process Modelling with iNaturalist](#data-process-modelling-with-inaturalist) |
| Dr. Steve Mussmann | [Searching for Novel Materials for Environmental Clean-Up](#searching-for-novel-materials-for-environmental-clean-up) |
| Dr. James Stroud | [Terrestrial LiDAR Vegetation Analysis](#terrestrial-lidar-vegetation-analysis) |
| Dr. Breanna Shi | [Historical Preservation by Digitizing Historic Artifacts](#historical-preservation-by-digitizing-historic-artifacts) |
| Dr. Arthur Porto | [Porto-Manafzadeh Vertebrate Joints](#porto-manafzadeh-vertebrate-joints) |
| Dr. Marco Postiglione | [Black-Box Interpretability of Large Language Models](#black-box-interpretability-of-large-language-models) |
| Dr. Patrick McGrath | [Open-Source Annotation Tool](#open-source-annotation-tool) |
| Dr. Heru Handika | [Digital Cataloging (NAHPU)](#digital-cataloging-nahpu) |
| Dr. Breanna Shi | [Unit Research Collaboration](#unit-research-collaboration) |
| Dr. Breanna Shi | [HPC Training](#hpc-training) |
| Dr. Supratik Mukhopadhyay | [Advanced Generative Models for 3D Biological Shape Completion](#advanced-generative-models-for-3d-biological-shape-completion) |
| Dr. Tuan-Anh Vu | [Robust & Calibrated 3D Human Motion for Cross-Site Parkinson's Gait Assess](#robust--calibrated-3d-human-motion-for-cross-site-parkinsons-gait-assess) |
| Dr. Tuan-Anh Vu | [Auditing Fairness Under Informative Missingness in Multimodal EHR Models](#auditing-fairness-under-informative-missingness-in-multimodal-ehr-models) |
| Dr. Steve Mussmann | [Vector DB Methods](#vector-db-methods) |
| Dr. Steve Mussmann | [Understanding the Predictability of Rail Crossing Delays](#understanding-the-predictability-of-rail-crossing-delays) |
| Dr. Steve Mussmann | [Light-Weight Training Batch Selection](#light-weight-training-batch-selection) |

## Behavior Analysis of Hume's Leaf Warbler Bird from Camera Traps

**Lead:** Dr. Ben Freeman

This project aims to develop and implement advanced computer vision algorithms for automated detection and analysis of Hume's Leaf Warbler behavior captured through camera trap footage across the Himalayas. The project will analyze an extensive dataset of camera trap recordings by employing sophisticated motion detection, object tracking, and behavioral classification techniques. The project extends beyond simple presence/absence detection to include detailed behavioral analysis using machine learning approaches and animal reidentification. We will track feeding patterns, predator-prey interactions, and other behaviors. Advanced pose estimation and trajectory analysis will be employed to identify patterns in movement behaviors.

Researchers’ goals will be:

Implementing an object detection pipeline that can determine the presence of the bird in frame with high accuracy

Adding temporal tracking feature to track multiple birds in frames and duration of presence

Comparing the quality of different detection models.

Additional Resources:

https://ieeexplore.ieee.org/document/7532575

https://elifesciences.org/articles/79305

https://openreview.net/pdf?id=9AcG3Tsyoq

**Recommended skills**

- Machine Learning/Deep Learning
- Computer Vision
- Python + ML ecosystem

## Automation of Lizard Landmark Analysis

**Lead:** Dr. James Stroud

A researcher will develop an automated machine learning pipeline that applies morphometric measurements to lizard toepad scans, building directly on the framework used for the lizard x-ray project. We currently perform this process manually, but now have a large, annotated dataset available for researchers to use in developing and refining an automated pipeline. The same pipeline architecture and graphical user interface (GUI) from the lizard x-ray project will be leveraged for consistency and efficiency. At present, a YOLO model has already been trained to detect and localize the toepads in images. Students will have the opportunity to iterate on and improve this model to increase accuracy and robustness. The next step in the pipeline will involve building a model capable of automatically placing thin-plate spline (TPS) landmark points on the detected toepads, enabling high-throughput morphometric analysis. We also are building an interactive web-based platform for visualizing, annotating, and analyzing X-ray images of lizards. The platform supports landmark-based annotation workflows, session-based history tracking, and integrates with backend data pipelines to support ongoing research. So far, the team has made strong progress on the frontend using React + TypeScript + Vite, connected to a Flask backend. Key features like persistent session support and per-session history tracking are already in place. We continue to improve usability, modularity, and backend communication, and are actively addressing any remaining bugs. We're also exploring the potential use of the Model Context Protocol (MCP) to enhance future integration capabilities.

We are working toward deploying the platform so it can be accessed and used by researchers for real-time annotation and analysis.

**Recommended skills**

- Experience with Flask or Python-based web services
- Familiarity with React, TypeScript, or other frontend frameworks
- Interest in biological data, morphology, or research tool development

## Audio Analysis of Hume's Leaf Warbler

**Lead:** Dr. Ben Freeman

This project aims to develop, evaluate, and deploy/productionize machine learning methods for detecting specific bird vocalizations, with a focus on the buzz call of the Hume’s Leaf Warbler (HLW). We are addressing an understudied problem for which no curated public dataset currently exists. As part of this effort, we are curating the first publicly available dataset of HLW buzz vocalizations using field data collected across the Himalayas.

BirdNET is currently used in the community for general bird detection, but it does not distinguish between buzz and call vocalizations of HLW. Our work develops new models that specifically detect the HLW buzz, enabling new ecological and behavioral insights.

We will benchmark and compare three modeling approaches:

BirdNET (as a community benchmark),

An object detection (OD) model trained to localize buzz events in spectrograms, and

An Audio Spectrogram Transformer (AST) model trained for classification.

We will conduct ablation studies (e.g., with and without source separation preprocessing) and assess how preprocessing affects performance. Our ultimate goal is to set up an inference system for ongoing field data analysis using the best-performing model. Currently, we are in the deployment/productionization phase.

Researchers’ work will seek to answer the following questions:

Can we develop a detector for the HLW buzz vocalization that outperforms BirdNET on thistask?

Which approach—OD or AST—performs best in terms of precision and recall on noisy field recordings?

How does audio preprocessing (e.g., noise suppression or source separation) affect model performance?

How do buzz vocalizations vary across space and time? Can these detections help test ecological hypotheses related to mate attraction and seasonality?

Additional Resources:

https://www.sciencedirect.com/science/article/pii/S1574954121000273

https://onlinelibrary.wiley.com/doi/pdfdirect/10.1111/ibi.13193

https://besjournals.onlinelibrary.wiley.com/doi/pdfdirect/10.1111/2041-210X.14003

**Recommended skills**

- Machine Learning/Deep Learning
- UI/UX Design and Development
- App Productionization/Deployment

## Photogrammetry Project

**Lead:** Dr. Arthur Porto

Contained in the vaults of museums and labs across the world, billions of specimens lie stacked in endless rows of trays and jars, their insights locked away to all but a few curious researchers who dare to brave the archives. The digital revolution brought with it the ability to bring these vast collections to life through photogrammetric techniques that allow research labs to scan physical specimens into 3D models. With this came endless opportunity for science, whether through morphological analysis, simulation, or even public education through animations and interactive exhibits.

The daunting task ahead of photogrammetry labs is now to find a way to process the decades, if not centuries, of specimens in their collections. Traditional photogrammetry techniques are historically very time and labor intensive, requiring extensive manual intervention for model rectification, calibration, and cleanup, in addition to complex photography and scanning setups that require careful manipulation of often fragile objects. The result is a never-ending backlog of objects to scan, and a constant cost-benefit analysis behind what gets priority. In recent years, major advances in machine learning-assisted computer vision open new doors for high-quality, automated, efficient 3D reconstruction processes. Transformer models from major AI studios such as Meta allow for rapid point cloud generation and novel-view synthesis. Neural network-based approaches can be used for high-quality convergence of SDF representations of objects. GPU-enabled compute using CUDA unlocks massive efficiency gains.

The goal of this project is to deliver an end-to-end pipeline that takes 2D images captured at labs and museums and convert them to high-quality, museum-grade models with rich color information, for use in anything from morphological analysis to CGI animation. A collaboration between Georgia Tech, the University of Florida, and the Florida NaturalHistory Museum, this project offers an exciting opportunity to get hands-on experience building cutting-edge ML/CV pipelines in close collaboration with end users.

Additional resources:

https://github.com/CKunhardt/augenblick

https://vgg-t.github.io/

https://github.com/NVlabs/neuralangelo

https://github.com/NVlabs/instant-ngp

**Recommended skills**

- Software Engineering experience in:
- Python
- C++/CUDA
- DevOps (Docker, Kubernetes, CI/CD pipelines)
- Computer Graphics experience
- 3D rendering, especially raymarching/SDFs and computational graphics
- Neural graphics techniques such as NeRF, Gaussian splatting, tiny-cuda-nn,InstantNGP
- Machine Learning experience
- Deep Learning using PyTorch
- Working with large, open-source datasets, such as those on HuggingFace

## Detection of Wildlife from Camera Traps at Stone Mountain

**Lead:** Dr. Jenny McGuire

Background and Goals: This project focuses on the identification of species from camera trapping images using computer vision. 5 motion activated camera traps have been set up in different ecosystems across Stone Mountain. Previously, a team of researchers have tried using publicly available ML processes for species identification of individual animals. However, they found their solution to be more time consuming and less accurate than manual identification. Our objective is to find a regionally specific training data set and come up with a more effective strategy to identify species in the camera trap images. The current pipeline follows a two-stage architecture: identify animal vs. empty frame and then species classification.

**Recommended skills**

- Python
- ML concepts, Deep Learning Architecture
- CNNs, YOLO, GPT4 API

## AI for Mental Health Sensing

**Lead:** Dr. Anind Dey

Mobile phones and wearable devices are increasingly used to model human behavior and predict health outcomes. While classical machine learning has shown success in predicting behaviors, routines, depression, and sleep from passive sensing data, it often requires time-consuming manual feature extraction. Deep-CNN architectures, however, have revolutionized computer vision by learning features automatically. This project aims to bridge this gap by encoding multi-variate time-series data from sensors into image representations (e.g., using Gramian Angular Fields or Markov Transition Fields). These images will then train robust Deep CNN models to predict well-being indicators like depression, sleep quality, and stress, as well as outcomes like GPA. Our goal is to develop a ”CT scan” for mental health—a non-invasive, accurate tool for diagnosis using passive sensing data.

Key Responsibilities

Conduct literature reviews on time-series encoding and deep learning architectures.

Benchmark existing algorithms using the Research Study Datasets.

Develop and fine-tune novel CNN architectures (inspired by medical imaging models like U-Net) for health outcome prediction.

Explore advanced encoding techniques to improve model performance.

**Recommended skills**

- Machine Learning & Deep Learning:
- Python (PyTorch or TensorFlow)
- Experience with CNNs and Computer Vision
- Understanding of Time-Series Analysis
- Data Science:
- Data visualization and preprocessing
- Experience with sensor data (accelerometer, physiological signals) is a plus
- Research:
- Ability to read and implement papers
- Strong analytical skills

## Data Process Modelling with iNaturalist

**Lead:** Dr. Steve Mussmann

iNaturalist is a citizen science platform where users upload and tag images of organisms including plants and animals. Unlocking biology insight from this enormous repository of ecological and environmental data is challenging due to many data quality and sampling issues. For data quality, observations often have missing features and may be incorrectly labeled. For data sampling, observations are biased by where users spend time and what they are interested in photographing. Furthermore, observations can be correlated (e.g., from BioBlitzes) and a single individual organism could have many observations (e.g., from a school field trip). These data challenges limit the scientific usefulness of iNaturalist data.The goal of this project is to survey and analyze these various data issues and test ideas to correct them. This first semester would be spent building data infrastructure, exploring related work, and creating preliminary analyses.

The goal of this project is to survey and analyze these various data issues and test ideas to correct them. This first semester would be spent building data infrastructure, exploring related work, and creating preliminary analyses.

**Recommended skills**

- Data processing and management
- Familiarity with data quality and sampling bias

## Searching for Novel Materials for Environmental Clean-Up

**Lead:** Dr. Steve Mussmann

PFAS are a ubiquitous environmental contaminant. A GTRI analytical chemist is looking to design and test new materials to absorb this contaminant. Chemical simulation software exists to test properties of compounds, such as binding affinity to PFAS, which can be used to screen candidates for lab tests. While large libraries (10^8) of chemical compounds exist, this is far too many to simulate (each simulation takes hours). The goal of this project is to use ML predictive chemical modelling and Bayesian Optimization to interactively simulate and find good chemical candidates while avoiding an exhaustive search. The first semester will be spent building and integrating the experimental pipeline, designing and analyzing multiple fidelity levels of ML chemical modelling, and exploring related work.

**Recommended skills**

- Integrating 3rd-party software tools
- Software engineering to build complex experimental pipelines
- (preferred) Experience with chemistry

## Terrestrial LiDAR Vegetation Analysis

**Lead:** Dr. James Stroud

This project is building new computational tools to extract and analyze vegetation structure from terrestrial LiDAR scans. The goal is to create open-source software that makes it easy to measure habitat structure, things like the number, size, and orientation of nearby branches, around any point in space. By doing this, researchers will be able to quantify habitat complexity at very fine spatial scales, which opens the door to answering ecological questions about how animals interact with their environments.

The project aims to make high-resolution vegetation structural analysis accessible through:

Automated segmentation of trees and branches in terrestrial LiDAR scans

Extraction of geometric features (e.g., branch length, diameter, angles)

Modular open-source software package in Python

Collaboration with biological and ecological scientists

**Recommended skills**

- Software engineering
- Python (packaging, PyInstaller, CI)
- Desktop GUI work, ideally PySide6 / Qt
- Spatial data structures (KD-trees, octrees, voxel grids), out-of-core algorithms, query performance
- 3D viz (Open3D, PyVista) and numerics (NumPy, SciPy, Numba)
- Point-cloud and geospatial
- Terrestrial or airborne LiDAR (.las / .laz) at scale, tiled workflows
- Segmentation, registration, and survey-grade georeferencing (GCPs, pyproj)
- Machine learning
- Deep learning on 3D point clouds (PyTorch, PyTorch Geometric, DGL)
- Familiarity with modern TLS methods (TreeLearn, SmartQSM, ForAINet, FSCT) and the tradecraft of training and evaluating them on real field scans
- Building evaluation harnesses that score models by downstream task accuracy

## Historical Preservation by Digitizing Historic Artifacts

**Lead:** Dr. Breanna Shi

The Georgia Trust for Historic Preservation works to preserve and revitalize Georgia’s historic resources and to increase public appreciation, protection, and use of historic places. The organization also operates historic house museums and develops educational and preservation resources. This project will support the digitization of historic artifacts associated with the Georgia Trust. Researchers will help develop a consistent process for creating, organizing, and documenting digital representations of collection materials so they can be preserved, studied, and made more accessible.

**Recommended skills**

- Interest in history
- Procedure development

## Porto-Manafzadeh Vertebrate Joints

**Lead:** Dr. Arthur Porto

The problem

Almost everything animals do — slithering, sprinting, swimming, soaring — runs through their joints, the places where skeleton meets skeleton and movement actually happens. You'd think we'd understand them well by now, but outside of human medicine we mostly don't: across the vast range of animal life, the basic link between how a joint is built and how it moves is still poorly understood. That gap matters, because without it you can't cleanly separate what an animal does because of its anatomy from what it does out of habit or choice, explain how skeletal shape underpins adaptation, or predict how animals will cope moving through changing and sometimes dangerous environments.

The project

This project studies one of the most fundamental questions in vertebrate biology — how joints work and where they come from, both across evolution and across an animal's development. It centers on XROMM (X-Ray Reconstruction of Moving Morphology), a technology that peers inside living animals to reconstruct skeletal motion in four dimensions at sub-millimeter precision. In collaboration with the Manafzadeh Lab, the work extends what XROMM can do and fuses it with comparative anatomy, so that internal joint motion can be read against the structure that produces it across many species. The aim is a clearer, more general account of the morphological foundations of vertebrate movement — the anatomical rules that connect how a joint is shaped to how it can move.

What you'd work with

XROMM-based 4D skeletal motion reconstruction, comparative vertebrate anatomy, and the analysis and visualization of high-precision 3D/4D morphological data — in close collaboration across two labs studying the structure-function basis of animal motion. A good fit for students drawn to the meeting point of biology, biomechanics, and quantitative methods.

**Recommended skills**

- XROMM modeling
- Data visualization

## Black-Box Interpretability of Large Language Models

**Lead:** Dr. Marco Postiglione

Large language models (LLMs) have achieved remarkable performance across diverse tasks, yet their opacity presents significant challenges for deployment in high-stakes domains such as medicine and law, where explainability is essential. Traditional interpretability methods that examine model internals—including attention mechanisms and gradient analyses—are unavailable for closed APIs and often inadequately capture the complex, emergent behaviors characteristic of large-scale models. Currently, we lack robust tools to predict when or why an LLM will exhibit specific behaviors. This project addresses these limitations through a comprehensive model-agnostic interpretability framework that operates without access to internal architecture or weights.

The objectives of this project are listed below:

Benchmarking. We will evaluate recent advances in LLM black-box interpretability (e.g., DBSA1, TokenSHAP2), establishing performance baselines across diverse tasks and model architectures.

Resource Development. We will create an open-source GitHub repository featuring intuitive interfaces that enable researchers and practitioners to apply state-of-the-art interpretability techniques to any LLM, democratizing access to explanation tools.

Novel Methodology. Drawing from established explainable AI approaches (e.g., counterfactual explanations), we will develop and validate a novel black-box interpretability technique designed to surpass current state-of-the-art performance.

Resources:

https://openreview.net/forum?id=ilNQ2m4GTy2

https://arxiv.org/abs/2407.10114

**Recommended skills**

- Machine learning, deep learning
- Experience with eXplainable AI, statistical analysis and hypothesis testing
- Experience with version control and collaborative development

## Open-Source Annotation Tool

**Lead:** Dr. Patrick McGrath

The problem

Studying how behavior evolves means watching a lot of animals — worms feeding, fish interacting — and turning hours of video into data a model can learn from. That labelling step is the bottleneck: someone has to mark what's happening, frame by frame, across images, video, and 3D recordings, and the lab's machine-learning and automated-behavior work is only as good as the annotations feeding it. General-purpose tools exist, but a lab studying two very different organisms with its own capture setups and its own definitions of behavior needs something that fits how it actually works, rather than bending the science to fit the tool.

The project

This project builds an open-source annotation tool for the McGrath Lab, which studies the genomic and neural basis of social and feeding behavior in C. elegans and East African cichlid fishes. The team uses the Computer Vision Annotation Tool (CVAT) — a mature platform for labelling images, video, and 3D data — as its reference point, learning from its design before tailoring an annotation workflow to the lab's specific organisms, recording formats, and behavioral labels. The first half is understanding the annotation problem the lab faces and the patterns CVAT already solves well; the second half is making it usable — a working, documented, open-source tool the lab can run on its own data and other behavior researchers can adopt.

What you'd work with

Full-stack and open-source software development, computer-vision annotation workflows for images, video, and 3D data, and the CVAT codebase as a reference architecture — plus close collaboration with a working biology lab to translate its real research needs into tooling. A good fit for students who want to ship usable software alongside science.

**Recommended skills**

- Full-stack software development
- Computer Vision (2D and 3D)
- Version control and collaborative development

## Digital Cataloging (NAHPU)

**Lead:** Dr. Heru Handika

The NAHPU project is a collaborative initiative to develop a high-performance, cross-platform digital catalog app and supporting software suites. Our mission is to develop software solutions to digitize natural history collections and deliver real-time data insights at the point of specimen collection. The real-world impact ranges from simply minimizing data entry errors, improving host-parasite data collection to accelerating the discovery of new species.

Motivation

Natural history museums host critical information about past and present biological diversity, yet most still rely on centuries-old, paper-based catalog methods. This traditional approach requires manual digitization, often via tedious Excel data entry, before records are added to permanent museum databases, such as Arctos or Specify. This process is inefficient and error-prone, creating a critical bottleneck for modern research involving natural history collections.

Our Goals

NAHPU streamlines the data pipeline from the field or lab directly to museum databases, ensuring consistency and predictability for downstream research in parasites, genomics, and biodiversity.

Short-Term Goals: Enable museums to eliminate errors in secondary data entry and simplify complex fieldwork records, including voucher specimens, ecological data, and derivative media such as photos, video, and audio.

Long-Term Goals: Create an integrated app suite for field data digitization and mobilization, featuring real-time analytics utilizing both conventional and advanced machine-learning methods.

Scientific Contribution

Given the complexity of natural history museum studies, this project is envisioned as a lifetime project, targeting regular, feature-based scientific publications.

Current key development areas:

AI/ML Integration: Implementing OCR to scan printed catalogs, automated field note translation, and computer vision for extracting HEX color values from specimen photos.

Core Systems: Enhancing data validation (outlier detection), synchronization features, and compliance with FAIR principles and DarwinCore standards.

GIS & Visualization: Improving coordinate support, bulk import from GPX/CSV, and leveraging GeoRust for spatial analysis.

UX/UI Design: Developing adaptive interfaces, advanced data visualization, and improving record exports.

Additional Resources:

https://nahpu.app/

https://github.com/nahpu

https://burn.dev/

https://github.com/huggingface/candle

https://arctosdb.org/

https://www.specifysoftware.org/

https://www.go-fair.org/fair-principles/

**Recommended skills**

- Software engineering experience
- Rust
- Flutter and Dart
- SQLite and an in-device vector database, such as LanceDB
- DevOps
- Mobile software development
- Machine learning experience
- Working with open-source SLMs
- Training computer vision models
- UX/UI experience
- Adaptive UI design
- Designing an accessible user interface, preferably with experience in Material Design
- State management, preferably with experience in using Riverpod

## Unit Research Collaboration

**Lead:** Dr. Breanna Shi

Research programs frequently contain multiple projects that share intellectual themes, methodological challenges, and dependencies while continuing to operate as distinct teams. Without effective coordination, potentially valuable knowledge can remain isolated, risks may become visible too late, and faculty or advisors may receive an incomplete picture of progress across the broader research portfolio. This project investigates HAAG’s unit-based coordination model, in which related projects participate in recurring cross-project discussions, exchange feedback, and share responsibility for maintaining information flow. The researcher will examine how coordination structures, representative roles, feedback cycles, accountability mechanisms, and cross-team working sessions influence knowledge integration and collective project delivery. The project will develop a rigorous framework for understanding how lightweight governance can strengthen visibility, learning, and coordination across a portfolio of research projects while preserving team-level autonomy.

**Recommended skills**

- Project management
- Collaborative leadership

## HPC Training

**Lead:** Dr. Breanna Shi

High-performance computing is essential to research that relies on large-scale data processing, computational modeling, reproducible workflows, and specialized CPU or GPU resources. Within HAAG, PACE ICE supports these activities through Slurm-based computing, interactive environments, research storage, and applications such as Jupyter, RStudio, and VS Code. Effective HPC training is therefore not simply a matter of teaching commands; it must also help researchers understand how to access the system, select appropriate tools, and use shared resources responsibly and confidently. This project examines how HPC training can be designed and managed to support consistent adoption across research teams. The researcher will study the technical and organizational factors that shape the training experience, including access requirements, user readiness, support structures, and coordination between researchers, advisors, and technical staff. The aim is to develop a practical, evidence-based framework for reducing barriers to entry, improving researcher preparedness, and strengthening the effective use of shared computational infrastructure.

**Recommended skills**

- Experience with high-performance computing (HPC)
- Documenting processes and procedures

## Advanced Generative Models for 3D Biological Shape Completion

**Lead:** Dr. Supratik Mukhopadhyay

This project aims to develop a state-of-the-art predictive tool that, given a partial or sparse 3D scan of a biological specimen, can generate a complete and anatomically coherent 3D structure. Moving beyond the linear limitations of traditional Statistical Shape Models (SSM) and PCA-based registration, this work will leverage the power of Conditional Denoising Diffusion Models (CDDMs).

The core of the project involves training a CDDM to learn the complex, non-linear deformation patterns required to warp a mean template shape to any complete sample in our dataset. By conditioning this process on a partial input scan, the model will learn to generate the most probable full deformation field, resulting in a high-fidelity shape completion. This generative approach is designed to produce reconstructions that are not only consistent with the provided data but are also more biologically plausible than those from methods constrained by linear assumptions.

This is a computationally intensive project that will require significant resources. Researchers will be expected to utilize the Partnership for an Advanced Computing Environment (PACE) resources provided by Georgia Tech for model training and inference.

Additional resources:

https://github.com/alannadels/CDDM_Point_Set_Registration/

https://arxiv.org/abs/2311.14960

**Recommended skills**

- Software Engineering/Data Science experience in:
- Python (NumPy, PyTorch or TensorFlow
- 3D Slicer for visualization and data handling (Qt for front-end development is a plus)
- Machine Learning/Computer Vision experience:
- Experience training deep generative models (e.g., Diffusion Models, VAEs, GANs).
- Familiarity with high-performance computing clusters (e.g., PACE).
- Proficiency working with 3D point cloud and mesh datasets (e.g., .ply files).

## Robust & Calibrated 3D Human Motion for Cross-Site Parkinson's Gait Assess

**Lead:** Dr. Tuan-Anh Vu

Robust and Calibrated 3D Human Motion Understanding for Cross-Site Parkinson's Gait Assessment

Overview

Parkinson's disease (PD) affects movement, and clinicians rate its severity using the Unified Parkinson's Disease Rating Scale (UPDRS) — including a 0–3 score for gait. These ratings are subjective and require an in-person assessment by a specialist. Our goal is to build AI models that estimate UPDRS gait severity directly from 3D human motion (anonymized SMPL body-model sequences reconstructed from video), so that assessment can be objective, remote, and privacy-preserving.

The hard part is not fitting a single dataset — it is generalizing to a new clinic that the model has never seen. Different sites use different cameras, capture protocols, and motion-reconstruction pipelines, and patient populations differ. A model that looks excellent on the data it was trained on can collapse on a genuinely new site. This "cross-site generalization" problem is the central research theme of this project, and it is exactly the kind of open problem that separates a leaderboard trick from a real scientific contribution.

This project builds directly on our recent work for the MoCHA 2026 Challenge (an ECCV 2026 workshop) on the CARE-PD benchmark, where our system ranked among the top entries among international teams. Students will help turn that empirical success — and, just as importantly, its failures — into publishable research targeting top-tier venues (e.g., CVPR 2027).

What we have found so far

Our challenge study produced several findings that motivate this project:

Diversity beats richness for cross-site transfer. Ensembling motion encoders across different training objectives (a standard classifier + a walk-level multiple-instance-learning model) generalized to unseen sites far better than making any single model larger or "cleaner." Simply adding capacity or averaging away noise hurts generalization.

Offline validation does not predict real cross-site performance. Standard leave-one-dataset-out validation on the known cohorts was not a reliable predictor of accuracy on a truly held-out, unseen clinic. Configurations that looked best offline were sometimes the worst in reality.

Hand-crafted clinical features anti-transfer. A model using expert gait features (cadence, step length, asymmetry, etc.) performed strongly in offline validation but crashed on the unseen site — it had latched onto site-specific capture artifacts rather than the disease signal.

The bottleneck is a motion-reconstruction domain gap. Much of the cross-site error traces to how the underlying 3D body model is fit to each site's video — a harmonization gap between capture pipelines, not just a "different patients" problem.

Severe cases are extremely rare. The most severe gait class appears in only ~1.5% of walks and is absent from half the training cohorts, so a naive classifier rarely predicts it, which caps the (class-balanced) clinical accuracy metric no matter how good the model is.

These are the open problems the project attacks.

Research Directions

Direction A — Robust cross-site generalization for clinical 3D motionGoal: build models whose accuracy survives deployment to an unseen clinic.Motivation: Findings 2–4 above show today's models are fragile across sites, and the root cause is a reconstruction or domain gap rather than raw model quality. We want to move from diagnosing this gap to closing it.What students will explore: domain-generalization and test-time-adaptation techniques for 3D human motion; harmonizing or normalizing SMPL-based motion representations across capture setups; representation-learning objectives that are invariant to site while staying sensitive to disease; and rigorous evaluation protocols that actually correlate with unseen-site performance.

Direction B — Label-shift-aware and calibrated clinical decision-makingGoal: make the model's decisions trustworthy when the class balance at test time is unknown and severe cases are rare.Motivation: Finding 5 shows that class imbalance and unknown test-time label distributions distort predictions and metrics. A model can be accurate yet systematically miss the rare, clinically critical severe cases.What students will explore: principled label-shift estimation and prior adaptation (e.g., EM-based / black-box shift estimators), probability calibration for imbalanced ordinal severity scores, and data-centric fixes for rare severe cases (including pathology-conditioned synthetic motion augmentation). The aim is a decision rule that is both well-calibrated and robust to unknown deployment distributions.

What you will do & gain

Implement and train deep learning models for 3D human motion understanding in PyTorch on GPU clusters.

Design experiments, run rigorous cross-site evaluations, and analyze why methods succeed or fail (not just chase a number).

Contribute to a research paper aimed at a top-tier conference and to an active international benchmark.

Learn modern 3D human pose/motion representation, domain generalization, and the realities of clinical/health-AI research.

**Recommended skills**

- Currently majoring in Computer Science, Computer Engineering, or a related field.
- Experience with or strong interest in Python.
- Familiarity with AI / deep learning and 3D reconstruction / 3D human pose & motion (e.g., SMPL).
- Hands-on experience with PyTorch (or another deep-learning framework).
- Comfort with Git, Linux, and running jobs on GPUs / HPC clusters (e.g., SLURM).
- Coursework or projects in machine learning, computer vision, or statistics.
- Interest in health/clinical applications of AI.

## Auditing Fairness Under Informative Missingness in Multimodal EHR Models

**Lead:** Dr. Tuan-Anh Vu

Who Gets an X-Ray? Auditing Fairness Under Informative Missingness in Multimodal EHR Models

Background

Modern clinical AI increasingly fuses several kinds of hospital data — structured vitals and labs, free-text clinical notes, and medical images such as chest X-rays — into a single model that predicts patient outcomes like in-hospital mortality or readmission. A large and fast-moving research literature now competes to build fusion models that "degrade gracefully": models that keep working even when part of a patient's record is missing.

Missing data is the normal case, not the exception. Hospitals don't run every test on every patient — a chest X-ray gets ordered when someone looks sick enough to warrant one, and a detailed note gets written when a case is complex. In the widely used multimodal datasets built from real intensive-care records, a majority of admissions are missing at least one modality (chest X-rays in particular are absent for most patients). So any model destined for real deployment must operate under pervasive missingness, and the field has responded with an array of missing-modality techniques — modality dropout, learnable "absence" embeddings, mixture-of-experts routing, and shared/specific representation learning.

The pivotal fact this project is built around is that this missingness is not random. A patient lacks an X-ray because of a clinical decision — which means the pattern of what's present in a record is itself informative, and reflects the biases in who historically received attention. That single fact turns "handling missing data" from a purely technical concern into a question about equity.

Motivation

Several independent, well-documented lines of evidence combine into a concern that no one has yet audited end-to-end:

Data availability is patterned by demographics, not just by medical need. Large studies of emergency-department care find that Black patients receive significantly less diagnostic imaging than white patients — roughly 20% lower odds in a national adult sample, and about 32% lower odds of advanced imaging in a Medicare population, even after adjustment. The same disparity appears in pediatric care. Crucially, it also appears inside the exact datasets used to train these models: audits of MIMIC-IV find Black and publicly-insured patients undergo fewer lab tests and receive fewer medications, meaning their records are systematically thinner across multiple modalities at once.

The modalities themselves encode who the patient is. Deep models can recover a patient's self-reported race from a chest X-ray with high accuracy, even when expert radiologists cannot and after controlling for confounders. More recent work suggests even socioeconomic proxies such as insurance type may be partially predictable from imaging. So a "race-blind" or "insurance-blind" model isn't blind at all.

Downstream models already underperform for under-served groups. Chest X-ray classifiers have been shown to systematically under-diagnose — label as "No Finding" — female, Black, and low-income patients, with the worst effects at the intersections of those groups.

Put these together and a troubling hypothesis emerges: if under-served patients have more missing modalities, then a model praised for "graceful degradation" may be degrading most for the patients who can least afford it. And the field's standard way of testing robustness — removing modalities at random — is structurally unable to detect this, because real missingness is anything but random. This project asks a question that is at once a rigorous machine-learning problem and a health-equity problem: when clinical data goes missing for reasons correlated with race, insurance, and language, do our best multimodal models quietly become unfair — and would current evaluation practice even notice?

Helpful References:

Gichoya et al. (2022), AI recognition of patient race in medical imaging: a modelling study, The Lancet Digital Health. https://www.thelancet.com/journals/landig/article/PIIS2589-7500(22)00063-2/fulltext . The single most striking motivator: models read race off an X-ray that humans can't.

Choi et al. (2025), ICYM2I: The Illusion of Multimodal Informativeness under Missingness, arXiv:2505.16953 . The methodological anchor for evaluating under informative missingness.

Yin et al. (2026), When Does Multimodal Learning Help in Healthcare? (CareBench), arXiv:2602.23614 . The closest related benchmark; shows fusion doesn't inherently improve fairness, which is exactly the gap we plan to extend.

**Recommended skills**

- Python and a deep-learning framework (PyTorch preferred): the core implementation environment for the models and evaluation harness.
- Machine-learning fundamentals, especially classification metrics, calibration, and evaluation. This project lives or dies on evaluation rigor rather than raw model-building.
- Comfort with messy, real-world multimodal and tabular data: cohort construction, joining across data sources, and handling missingness.
- A statistical mindset: subgroup analysis, adjustment and confounding, and ideally exposure to missing-data or causal-inference ideas (missing-at-random vs. not-at-random, inverse-probability weighting), or eagerness to learn them.
- Reproducible-research and engineering habits: Git, containerization, experiment tracking, clean code — since a goal is to ship a reusable open-source toolkit.
- Genuine interest in health equity and clinical AI: the fairness questions are central to the science here, not an add-on.
- Nice to have: clinical NLP (encoding notes), medical-imaging encoders (chest X-rays), or experience running jobs on GPU/HPC clusters.

## Vector DB Methods

**Lead:** Dr. Steve Mussmann

Vector databases build an index from a dataset of vectors so that they can quickly respond to “most similar” vector search queries. Currently, the SOTA methods have no theoretical guarantees (retrieval accuracy or resource usage). Theoreticians have focused on LSH methods with both guarantees but perform empirically poorly. A key challenge is that generic vectors (e.g. isotropically distributed) are a difficult but unrealistic case. Thus, SOTA algorithms are effective due to special properties (e.g., manifold) of the vectors, which are hard to quantify and verify in practice.

In this project, we attempt a method that breaks this tension by providing retrieval performance guarantees but without any resource usage guarantees (e.g., brute force resource usage for isotropic vectors). I have an idea for a “ball tree” which is a tree-based method over a metric space.

**Recommended skills**

- Downloading, integrating, and encoding public datasets
- A good understanding of high dimensional methods (e.g. PCA, cosine similarity)
- A good understanding of tree-based methods (e.g., recursion, branch-and-bound)
- The ability to implement and test novel mathematical algorithms

## Understanding the Predictability of Rail Crossing Delays

**Lead:** Dr. Steve Mussmann

Charleston, SC is a port city requiring many train lines. Due to the restrictive geography of the area (rivers, wetlands), there are many rail crossings even on busy roads near downtown Charleston, which causes many bus delays, truck delivery delays, and emergency vehicle delays. Ideally, bridges would be built to avoid the train crossing, but these are very expensive. The city of Charleston wants to explore the predictability of train crossing delay timing and duration. If delays are predictable, then alternative routing systems and electronic signs informing the public could be deployed. Unfortunately, at this time, it is not known to what extent thecrossings are predictable.

In this project, we will use data from (1) historical bus GPS and (2) historical bus operator’s noticed delays to predict the frequency and duration of delays at different times of year, week, and day. Additionally, due to some bus crossings being on the same rail line, we may be able to predict train crossing delays from other train crossing delays.

**Recommended skills**

- Interpreting, transforming, and integrating data
- Working with geospatial data tools for visualization and featurization
- Running (simpler) ML models such as conditional density estimation and linear, high-dimensional classifiers

## Light-Weight Training Batch Selection

**Lead:** Dr. Steve Mussmann

Over the past 5 or so years, there has been a grow interesting in selecting the data to train models. Intuitively, training on high-quality, diverse data is more computationally efficient than training on noisy, redundant data. Despite the large body of work in this area, such methods have seen minimal use, perhaps due to the overhead of selection. Most methods perform additional neural network operations on data points (e.g., a forward pass) to guide selection, greatly limiting the potential speed-up.In this project, we attempt to design and test a batch selection method that only uses the computation from past iterations and thus has minimal overhead. While ideas from previous work (e.g., selecting points with a large loss gradient) can be used, the implementation of such ideas using only past iterations creates challenges such as handling stale statistics.

**Recommended skills**

- Ability to read and compare research papers
- Familiarity with the implementation of the training loop in neural networks (e.g., data loaders, gradients)
- Downloading and integrating public datasets
