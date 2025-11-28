# ntuser-recovery-project
NTUSER.DAT recovery and analysis for System Administration course
# NTUSER.DAT Recovery & Analysis

## Project Overview
This project focuses on recovering deleted or corrupted NTUSER.DAT hive files from a VM image with Windows 10 and extracting user activity artifacts (UserAssist, RecentDocs, ShellBags). We then correlate registry artifacts with file system artifacts (LNK, Prefetch, MFT) to build a timeline of user actions.

## Relevance
User registry hives contain key forensic traces: recently executed programs, opened documents, mounted devices, and user preferences. Recovering and validating these hives is essential for user activity reconstruction in incident response and forensic investigations.

## Methodology
- **Environment**
  - VirtualBox Windows VM (Windows 10), FTK Imager on host, Python 3.x on host.
- **Tools**
  - FTK Imager, HxD, python-registry, regipy (optional), RegRipper, Eric Zimmerman utilities.
- **Workflow**
  1. Acquire disk image (image_A.raw) and record hashes.
  2. Mount image in FTK / carve `regf` headers if file deleted.
  3. Extract NTUSER.DAT and any logs (.LOG1/.LOG2).
  4. Parse UserAssist / RecentDocs; export `.lnk` and Prefetch files.
  5. Correlate registry + filesystem artifacts and build a timeline.

## Results
- List of recovered artifacts (paths + SHA256 hashes).
- Screenshots and parsed outputs (inside `/artifacts`).
- Short timeline of noteworthy user activity.

## Limitations
- Overwritten clusters, SSD TRIM, or secure deletion may prevent full recovery.
- Reassembly accuracy depends on MFT data runs and VSS availability.

## Reproducibility
Step-by-step commands and scripts are included in `/scripts`. Use the work copy files in `/hives` and the acquisition images in `/acquisition`.

## Team
Antonio Musumeci - 
Clark Loeffer (GitHub: `@teammate-username`)
