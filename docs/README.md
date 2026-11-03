# DMJO-MEC Research Documentation Index

Welcome to the comprehensive documentation for the **Priority-Aware Multi-UAV Joint Optimization (PA-MUJO)** research project.

---

## Documentation Roadmap

### 1. Setup & Execution Guides
* **[`docs/setup/RUN_ON_CAMPUS_MACHINE.md`](setup/RUN_ON_CAMPUS_MACHINE.md)**:
  * Hardware requirements, campus GPU proxy setup (`172.31.2.4:8080`), and PyTorch CUDA installation.
  * Step-by-step training runbook inside `tmux` sessions.
  * Monitoring commands, troubleshooting tips, and checkpoint recovery.

### 2. Theoretical Methodology & Context
* **[`docs/methodology/AI_AGENT_CONTEXT.md`](methodology/AI_AGENT_CONTEXT.md)**:
  * Comprehensive technical handoff detailing system models, A2G channel formulas, analytical bisection root-finding, and reward formulations.
  * Guidance on continuous action mappings, GAE advantage updates, and cooperative caching.

### 3. Architecture & Tracking
* **[`docs/architecture/REPOSITORY_STRUCTURE.md`](architecture/REPOSITORY_STRUCTURE.md)**:
  * Complete directory breakdown, module responsibilities, and import conventions.
* **[`docs/architecture/MAPPO_Project_Tracker.md`](architecture/MAPPO_Project_Tracker.md)**:
  * Algorithmic direction, locked interfaces, and verification scope.

### 4. Academic Reports & IEEE Publications
* **[`docs/reports/paper/`](reports/paper/)**:
  * Publication draft formatted in IEEEtran double-column style (`paper.tex`).
  * System model diagrams, priority computation flowcharts, and bibliography (`ref.bib`).
  * Author biography metadata and pre-compiled PDF (`paper.pdf`).
* **[`docs/reports/templates/`](reports/templates/)**:
  * Course presentation template and legacy benchmark files.

### 5. Scientific Literature
* **[`docs/research_papers/base_papers/`](research_papers/base_papers/)**:
  * Foundational literature on 3D DRL UAV trajectory design (Li et al.) and services computing.
* **[`docs/research_papers/reference_papers/`](research_papers/reference_papers/)**:
  * 16 reference papers covering NOMA aerial networks, priority-differentiated scheduling, rotary-wing aerodynamics, and Gauss-Markov mobility.

---

## Quick Reference Links
* **Root Execution Entrypoint**: [`train.py`](../train.py)
* **Configuration Parameters**: [`src/dmjo_mec/config.py`](../src/dmjo_mec/config.py)
* **IEEE Figure Generator**: [`plot_ieee.py`](../plot_ieee.py)
* **Recent GPU Training Report**: [`POST_TRAINING_REPORT.md`](../POST_TRAINING_REPORT.md)
