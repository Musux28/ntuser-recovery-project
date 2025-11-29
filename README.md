# ntuser-recovery-project
# Registry Hive Recovery & Analysis — NTUSER, SYSTEM, SOFTWARE, SECURITY, SAM
Automated / Reproducible workflow to extract, validate and analyse Windows registry hives from a VM image and locate user activity evidence using FTK Imager, FTK Registry Viewer and Python tools.

## Project Overview
This project extracts and analyses core Windows registry hives from a forensic VM image and locates evidence of a user’s actions on the device. Hives of interest: NTUSER.DAT (per-user) and the system hives SYSTEM, SOFTWARE, SECURITY, and SAM. The workflow used in this project is forensic: we mount the Windows partition read-only from Kali Linux (forensic mode), copy the hive files and event logs to a shared folder, then analyse the files on the host using FTK Registry Viewer and other GUI tools.

## Relevance
User registry hives contain key forensic traces: recently executed programs, opened documents, mounted devices, and user preferences. Recovering and validating these hives is essential for user activity reconstruction in incident response and forensic investigations.

## Objective
-Export registry hives from a forensic image (read-only), verify integrity, and examine keys and values that indicate user activity (UserAssist, RecentDocs, MUICache, MountedDevices, MountPoints2, ShellBags).
-Correlate registry findings with exported filesystem artifacts (LNK, Prefetch, event logs) and produce a short timeline of relevant user actions.
-Keep a full acquisition log and file hashes for reproducibility and chain of custody.

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

##  Project Structure
```                         
├-- carved_evidence/                    
│   ├-- carved_jpgs/
│       ├-- 00000879.jpg   
│       ├-- 00000880.jpg 
│       ├-- 00000881.jpg 
│       ├-- 00000882.jpg 
│       ├-- 00000882.jpg 
│       ├-- ...
│       └-- readme.md      
│   ├-- carved_jpgs/
│       ├-- 00000926.pdf  
│       ├-- 00000927.pdf  
│       ├-- 00000928.pdf 
│       ├-- 00000929.pdf 
│       ├-- readme.md 
│       └-- readme.md
│   ├-- audi.txt/
│   ├-- readme.md/
├-- code/
│       └-- reg_carve.py
├-- evidence_export/
│       ├-- Application.evtx   
│       ├-- Hardware Explorer.evtx 
│       ├-- Internet Explorer.evtx
│       ├-- Key Management Service.evtx 
│       ├-- NTUSER.DAT
│       ├-- SAM   
│       ├-- SECURITY
│       ├-- SYSTEM
│       ├-- Security.evtx 
│       ├-- Setup.evtx
│       ├-- System.evtx   
│       └-- readme.md
├-- .gitignore
├-- README.md   # Main documentation (you are here)

```


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
