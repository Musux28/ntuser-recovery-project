# ntuser-recovery-project
# Registry Hive Recovery & Analysis — NTUSER, SYSTEM, SOFTWARE, SECURITY, SAM
Automated / Reproducible workflow to extract, validate and analyse Windows registry hives from a VM image and locate user activity evidence using FTK Imager, FTK Registry Viewer and Python tools.

## Project Overview
This project extracts and analyses core Windows registry hives from a forensic VM image to identify and correlate user activity. Hives of interest are the per-user NTUSER.DAT and the system-level hives SYSTEM, SOFTWARE, SECURITY and SAM. We use FTK Imager / FTK Registry Viewer for safe extraction and visual inspection, and Python utilities for automated dumps and initial parsing (UserAssist, RecentDocs, MountedDevices, ShellBags).

## Relevance
User registry hives contain key forensic traces: recently executed programs, opened documents, mounted devices, and user preferences. Recovering and validating these hives is essential for user activity reconstruction in incident response and forensic investigations.

## Objective
From exported registry hives we aim to automatically and reproducibly:

-Validate hive integrity (REGF header / hbin structure).
-Produce machine-readable exports of key forensic artifacts: UserAssist, RecentDocs, MUICache, MountedDevices, MountPoints2, and ShellBags.
-Extract and hash correlated filesystem artifacts referenced in the registry (LNK, Prefetch).
-Correlate registry + filesystem evidence to build a short timeline of user actions.
-Provide reproducible scripts, logs and a playbook so another examiner can repeat the analysis.

## Results summary (planned vs current status)

|                    Metric / task | Target                                            | Current status (honest)                                                                               |
| -------------------------------: | :------------------------------------------------ | :---------------------------------------------------------------------------------------------------- |
|                  Hives to export | 5 (NTUSER, SYSTEM, SOFTWARE, SECURITY, SAM)       | NTUSER exported (NTUSER.DAT.copy0 + work copy). SYSTEM/SOFTWARE/SECURITY/SAM planned/ready for export |
|             Parsed artifact sets | UserAssist, RecentDocs, ShellBags, MountedDevices | UserAssist & RecentDocs initial dumps completed                                                       |
|  LNK files exported and analysed | ≥ 10                                              | Some LNK names identified via RecentDocs (MRU order `1,0`) — extraction pending                       |
| Prefetch files exported & parsed | All in `Windows\Prefetch`                         | Prefetch visible in FTK; mount/export in progress                                                     |
|        Timeline entries produced | 10–20                                             | Example timeline entries prepared; full timeline pending correlation                                  |


## Quick start — prerequisites & installation
## Prerequisites

-Windows host for analysis (recommended).
-FTK Imager (GUI) — for mounting and exporting hives.
-Python 3.8+ with python-registry installed.
-Optional tools: RegRipper (Perl), Registry Explorer (Eric Zimmerman), HxD (hex editor).
python -m pip install python-registry

## Project structure
/ntuser-registry-project
├─ README.md
├─ acquisition/
│   ├─ VM_Image_A.raw
│   ├─ VM_Image_A.sha256.txt
│   └─ acquisition_log.txt
├─ hives/
│   ├─ NTUSER.DAT.copy0
│   ├─ NTUSER_work.dat
│   ├─ SYSTEM
│   ├─ SOFTWARE
│   ├─ SECURITY
│   └─ SAM
├─ scripts/
│   ├─ dump_user_registry.py
│   ├─ decode_userassist_detailed.py
│   └─ extract_lnks.ps1
├─ artifacts/
│   ├─ lnk/
│   └─ prefetch/
├─ docs/
│   └─ report.pdf
└─ presentation/
    └─ slides.pdf

## Methodology 
## Phase 1 — Acquisition & verification
-Acquire a read-only forensic image of the VM (FTK Imager or dd).
-Compute and record SHA256 for the image. Save acquisition metadata and chain-of-custody notes in acquisition/acquisition_log.txt.

## Phase 2 — Hive extraction & validation
-Mount the image read-only in FTK Imager and export the target hives to hives/.
-Validate regf header (hex 72 65 67 66) and inspect hbin blocks with HxD or python-registry.
-Copy to work files (*_work.dat) and NEVER edit original exports.

## Phase 3 — Automated parsing & dumps
-Run scripts/dump_user_registry.py (python-registry) to export top-level keys and dump UserAssist, RecentDocs, MountedDevices, MountPoints2.
-Run scripts/decode_userassist_detailed.py to search UserAssist blobs for plausible FILETIME and run-count heuristics.

## Phase 4 — Artifact extraction & correlation
-Export LNK / Prefetch referenced by registry values using FTK Search (or mount partition & use PowerShell).
-Compute SHA256 for all exported artifacts.
-Correlate registry timestamps with Prefetch/LNK/MFT data to produce timeline entries.

## Phase 5 — Reporting
-Produce a short report (docs/report.pdf) with key findings, hashes, and a reproducible playbook (commands + scripts used).

## Results
- List of recovered artifacts (paths + SHA256 hashes).
- Screenshots and parsed outputs (inside `/artifacts`).
- Short timeline of noteworthy user activity.

## Technologies
-FTK Imager / FTK Registry Viewer (GUI)
-Python 3.x + python-registry
-PowerShell (Windows host)
-HxD (hex editor)

## Limitations
- Overwritten clusters, SSD TRIM, or secure deletion may prevent full recovery.
- Reassembly accuracy depends on MFT data runs and VSS availability.


## Team
Antonio Musumeci - 
Clark Loeffer (GitHub: `@teammate-username`)
