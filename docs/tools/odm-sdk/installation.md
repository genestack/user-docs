# Installation odm-sdk

## Requirements

- Python 3
- pip

## Instructions

### Install

1. Start a console/terminal:

2. Install the latest version using pip:

    ```shell
    python3 -m pip install odm-sdk
    ```

   To install a specific version of a package, simply append the version number to the package reference in the command. For example: `odm-sdk==1.57.0`

### To check the existing version, and view all available console commands, type

```shell
python3 -m pip show --verbose odm-sdk
```

### You can always remove the package with a help of this command

```shell
python3 -m pip uninstall odm-sdk
```
## Troubleshooting

### Version mismatch

If you encounter an error while working with the SDK, the most common reason is a **version mismatch** between your installed SDK and the ODM.

Reinstall the SDK to match the version deployed in your environment:

```bash
python3 -m pip uninstall odm-sdk
python3 -m pip install odm-sdk==<version>
```

You can verify the currently deployed version by navigating to the ODM homepage.

### Check where the SDK is installed

If you're unsure which environment your SDK was installed in, or if you're dealing with multiple Python installations, use the following commands:

#### macOS / Linux

```bash
python3 -m site
```

Or to see the actual path of the installed SDK:

```bash
pip show odm-sdk
```
Look for the line:

```bash
Location: /path/to/site-packages
```

#### Windows
Open Command Prompt or PowerShell and run:

```bash
py -m site
```

Or check the SDK location directly:
```bash
pip show odm-sdk
```
This helps verify whether the SDK was installed in the correct Python environment (e.g. system Python, virtualenv, conda, etc.).

### Python environment not visible in `ENV`

If you run the `ENV` command (or check environment variables) and don't see your Python environment listed, it may not be properly added to your system's `PATH`.

#### How to locate the Python path

##### macOS / Linux

Use the `which` command:

```bash
which python3
```

Or for pip:

```bash
which pip3
```
This shows the full path of the active Python interpreter or pip binary (e.g., /usr/local/bin/python3).

##### Windows

Use the where command:

```bash
where python
```

Or:

```bash
where pip
```

This returns the full path to the installed Python executable (e.g., C:\Users\yourname\AppData\Local\Programs\Python\Python310\python.exe)

#### Add it to your PATH manually

##### macOS / Linux:

Edit your `~/.bash_profile`, `~/.zshrc`, or `~/.bashrc`:

```bash
export PATH="/path/to/python:$PATH"
```

Then apply the changes:

```bash
source ~/.zshrc  # or source the correct file for your shell
```

##### Windows:

1- Open System Properties > Environment Variables

2 - Under System variables, select Path and click Edit

3 - Click New and add the path to your Python or Scripts folder (e.g., C:\Python310\Scripts)

4 - Click OK and restart your terminal or IDE

After updating `PATH`, restart your shell or command prompt to apply the change.
