# ntuser-recovery-project
# Registry Hive Recovery & Analysis — NTUSER, SYSTEM, SOFTWARE, SECURITY, SAM
Automated / Reproducible workflow to extract, validate and analyse Windows registry hives from a VM image and locate user activity evidence using FTK Imager, FTK Registry Viewer and Python tools.

## Project Overview

This project extracts and analyses Windows registry hives and application/event logs from a forensic VM image to identify user activity. The primary objective is to locate and document user actions (web history, recently accessed files, and mounted removable media) by examining the per-user hive (NTUSER.DAT) and system hives (SYSTEM, SOFTWARE, SECURITY, SAM), and by correlating those registry findings with exported files and event logs.

## Project Relevance
Windows registry hives are a rich source of forensic evidence: they capture user activity (recent documents, typed URLs, run counts), device mounts (USB drives), and system state. Recovering and interpreting this data matters in cases such as incident response, insider threat investigations, and digital forensic coursework.
 ## Why this project?
-Demonstrates a repeatable, forensically-sound extraction workflow (read-only mount → copy → offline analysis).
-Teaches core forensic skills: safe acquisition, registry structure inspection, artifact correlation (Registry ↔ LNK/Prefetch/EVTX).
-Produces experience with common forensic tools (Kali Live in forensic mode, FTK Imager / FTK Registry Viewer, hex checks)
---
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
---

## Methodology 
## Setup & environment
-Acquisition host: Kali Linux (booted in forensic mode / Live ISO) used to mount Windows partition read-only.
-Analysis host: Windows host running FTK Imager / FTK Registry Viewer (offline analysis of copied files).
-Storage: a shared folder between the forensic VM and host was used to transfer exported hives & logs.

## Tools & datasets used
-Kali Linux (forensic mode) — read-only mounting and copying.
-ntfs-3g / mount — to mount NTFS partition read-only.
-FTK Imager / FTK Registry Viewer — open and inspect registry hives visually; export screenshots, .reg or text.
-Hex editor (HxD) — verify signatures and offsets where necessary.
-sha256sum / CertUtil — compute & record file hashes.
-Source dataset: Windows VM image created for the lab; exported hive files (NTUSER.DAT, SYSTEM, SOFTWARE, SECURITY, SAM) and event logs (EVTX).

## Architecture / workflow (high-level)
-Run scripts/dump_user_registry.py (python-registry) to export top-level keys and dump UserAssist, RecentDocs, MountedDevices, MountPoints2.
-Run scripts/decode_userassist_detailed.py to search UserAssist blobs for plausible FILETIME and run-count heuristics.

[VM disk image]  --(Kali forensic read-only mount)-->  /mnt/windows
    |
    +-- copy Windows/System32/config/* (SYSTEM, SOFTWARE, SECURITY, SAM)
    +-- copy Users/<user>/NTUSER.DAT and winevt logs --> /mnt/shared
    |
[Host] <- shared folder <- copied hives & logs
    |
    +-- Open hives in FTK Registry Viewer -> inspect & export artifacts
    +-- Correlate with exported LNK / Prefetch / EVTX -> timeline


## Step-by-step process (reproducible)
1)Boot Kali in forensic mode; identify the Windows partition (fdisk -l, lsblk -f).
2)Mount read-only:
sudo mkdir -p /mnt/windows
sudo mount -o ro /dev/sdXN /mnt/windows

```
# or: sudo ntfs-3g -o ro /dev/sdXN /mnt/windows

```
3)Create and mount a shared folder to transfer files to the host, e.g. /mnt/shared.
4)Copy hives & logs:

```
sudo cp /mnt/windows/Windows/System32/config/SYSTEM /mnt/shared/
sudo cp /mnt/windows/Windows/System32/config/SOFTWARE /mnt/shared/
sudo cp /mnt/windows/Windows/System32/config/SECURITY /mnt/shared/
sudo cp /mnt/windows/Windows/System32/config/SAM /mnt/shared/
sudo cp "/mnt/windows/Users/<username>/NTUSER.DAT" /mnt/shared/
sudo cp /mnt/windows/Windows/System32/winevt/Logs/*.evtx /mnt/shared/

```
5)On the host, compute and record SHA-256 for each exported file:

```
sha256sum /path/to/shared/NTUSER.DAT > NTUSER.DAT.sha256.txt

```
Add all metadata (operator, date/time, tool) to acquisition/acquisition_log.txt.

6)Analyse exported hives in FTK Registry Viewer: open hive files and inspect keys of interest (UserAssist, RecentDocs, TypedURLs, MountPoints2, MUICache). Export screenshots and text for reporting.


---

## Results — key findings & evidence
The report includes multiple FTK Registry Viewer screenshots and parsed observations showing clear user activity. Key findings extracted from the NTUSER.DAT hive:

-Typed Internet Explorer URLs (Software → Microsoft → Internet Explorer → TypedURLs)
 The TypedURLs entries list websites visited by the user (recent → older). This confirms web activity and specific domains visited (see screenshot and hex view).

-Mounted devices evidence (Software → Microsoft → Windows → CurrentVersion → Explorer → MountPoints2 → {GUID} → _Autorun → DefaultIcon / DefaultLabel)
 The DefaultIcon contains the mount point E:\ and DefaultLabel contains the device name DEFT_8. This indicates the user mounted and used an export drive (evidence the examiner used to copy data off the system). See screenshot(s) in the report showing the MountPoints2 entries and hex details.

 -RecentDocs evidence (Software → Microsoft → Windows → CurrentVersion → Explorer → RecentDocs → .jpg/.png/.pdf/Folder)
 The RecentDocs keys include entries for image files (.jpg, .png) and PDFs — implying the user accessed or downloaded these files (report suggests they were saved in a OneDrive folder and then transferred to the export drive). Screenshots of RecentDocs entries and hex blob values are provided in the report.


---
## Visual evidence included
 Multiple FTK Registry Viewer screenshots displaying TypedURLs, MountPoints2 (DefaultIcon, DefaultLabel), and RecentDocs entries; hex pane and key properties are captured in the PDF.

| Artifact location (hive path)                       |       Evidence type | Finding / interpretation                                                               |
| --------------------------------------------------- | ------------------: | -------------------------------------------------------------------------------------- |
| `Software\Microsoft\Internet Explorer\TypedURLs`    |         Web history | List of visited URLs (recent → older).                                                 |
| `Explorer\MountPoints2\{GUID}\_Autorun\DefaultIcon` | Mounted device path | Contains `E:\` (mount point) — shows external drive usage.                             |
| `Explorer\RecentDocs` (.jpg/.pdf)                   |        Recent files | Names of images and PDFs accessed — likely downloaded to OneDrive and later exported.  |

---
## Conclusion, lessons learned & next steps
 ## Conclusion
 The registry analysis successfully identified web activity (IE typed URLs), recently accessed documents (images/PDFs), and a mounted removable device used to export evidence (device label DEFT_8, mount E:\). These  items provide corroborating artifacts for reconstructing a short user activity timeline.

 ## Lessons learned
 -Always perform acquisition in true forensic mode (read-only) to avoid modifying evidence.
-Registry keys such as MountPoints2 and RecentDocs are high-value, quickly actionable sources for linking user activity and removable media use.
-Preserve original exported hive files as immutable — perform analysis only on copies (e.g., NTUSER_work.dat).

---
## Team
Antonio Musumeci - 
Clark Loeffer (GitHub: `@teammate-username`)
