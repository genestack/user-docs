---
diataxis: reference
tab: api-libraries
---

# Troubleshoot ODM SDK installation

This reference covers common installation issues with the ODM SDK and their resolutions.

## Version mismatch

**Cause:** The installed SDK version does not match the version of ODM deployed in your environment.

**Resolution:** Reinstall the SDK to match the deployed version:

```bash
python3 -m pip uninstall odm-sdk
python3 -m pip install odm-sdk==<version>
```

You can verify the currently deployed ODM version by navigating to the ODM homepage.

---

## Finding the installed SDK location

If you are unsure which Python environment contains your SDK installation, use the following commands.

**macOS / Linux:**

```bash
python3 -m site
```

Or to see the actual path:

```bash
pip show odm-sdk
```

Look for the `Location:` line in the output.

**Windows:**

```bash
py -m site
```

Or:

```bash
pip show odm-sdk
```

This helps verify whether the SDK was installed in the correct Python environment (system Python, virtualenv, conda, etc.).

---

## Python environment not visible in PATH

If your Python environment is not listed in your system's PATH, the SDK commands may not be found after installation.

**How to locate the Python path:**

macOS / Linux:

```bash
which python3
which pip3
```

Windows:

```bash
where python
where pip
```

**Add Python to PATH manually:**

macOS / Linux, edit `~/.bash_profile`, `~/.zshrc`, or `~/.bashrc`:

```bash
export PATH="/path/to/python:$PATH"
```

Then apply the change:

```bash
source ~/.zshrc
```

(or source the correct file for your shell)

Windows:

1. Open System Properties and select Environment Variables.
2. Under System variables, select Path and click Edit.
3. Click New and add the path to your Python or Scripts folder (for example, `C:\Python310\Scripts`).
4. Click OK and restart your terminal or IDE.

After updating PATH, restart your shell or command prompt to apply the change.
