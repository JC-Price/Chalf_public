# Running CHalf in Headless Mode

CHalf allows for "Headless" execution via the command line. This is ideal for processing large datasets on remote servers, high-performance computing (HPC) clusters, or for integrating CHalf into automated pipelines.

## 1. Prerequisites
To run in headless mode, you must have the backend script (`CHalf_v4_3_headless.exe`).

**Required Files:**
Before executing the command, ensure you have generated the following configuration files (either manually or by saving them from the GUI):
1.  **Workflow File (`.workflow`):** Contains all analysis parameters (filters, cutoffs, etc.).
2.  **Manifest File (`.manifest`):** Lists the input CSVs and their conditions.
3.  **Visualization Config (`.vis`):** *(Optional)* Required if you want to generate figures automatically.

---

## 2. Command Syntax

Run the software by calling the executable directly with the required arguments.

```bash
CHalf_v4_3_headless.exe --directory <PATH> --workflow <PATH> --manifest <PATH> [options]
```

## 3. Command Options

```
options:
  -h, --help            show this help message and exit
  -w WORKFLOW, --workflow WORKFLOW
                        A .worfklow file containing all of the parameters to be used by CHalf.
  -m MANIFEST, --manifest MANIFEST
                        A .manifest file containing the information about the input files to be used by CHalf.
  -v VISUAL, --visual VISUAL
                        A .vis file used for specifying the parameters of
  -d DIRECTORY, --directory DIRECTORY
                        Working directory for the CHalf project.
  - LOG, --log LOG      For outputing a log file if using command line. Accepts a string as the name of the log file
                        that will be saved as a .txt file in the output directory.
```