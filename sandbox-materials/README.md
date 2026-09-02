# ODM Demo Notebooks

Jupyter notebooks for the Genestack ODM (Open Data Manager) demo sessions.

---

## Prerequisites

Complete the steps below before opening a notebook. You need **Python 3.10 or higher** and `pip`. The helper package `demo_utils` (and its scientific / ODM dependencies) is installed from this folder.

These instructions use a **fresh virtual environment** and the classic **Jupyter Notebook** server. You can use another tool (for example VS Code) if you prefer; the same kernel name is used in either case.

### 1. Open a terminal in this folder

```bash
cd /path/to/demo/notebooks/folder
```

Use the real path on your machine. The working directory must contain `setup.py` and `demo_utils/`.

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Your prompt should show `(.venv)` after activation. Leave this environment active for the remaining commands.

### 3. Install the demo package and Jupyter Notebook

Upgrade `pip`, then install this project in editable mode (`-e .`). That installs `demo_utils` and the libraries listed in `setup.py` (including `odm-sdk`, `scanpy`, and `ipykernel`).

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -e .
python3 -m pip install notebook
```

`notebook` is installed separately so you can launch the Jupyter Notebook application (`jupyter notebook`). `ipykernel` is already a dependency of `demo_utils`.

### 4. Register a Jupyter kernel

Register the virtual environment so notebooks can select it by name:

```bash
python3 -m ipykernel install --user \
  --name=odm-demo \
  --display-name="Python (odm-demo)"
```

`--name=odm-demo` is the internal kernel id. `--display-name="Python (odm-demo)"` is the label shown in the Jupyter UI.

### 5. Launch Jupyter Notebook

```bash
jupyter notebook
```

A browser window opens with the Jupyter file browser. Stay in this folder (or navigate to it in the UI) so you can open the included `.ipynb` files.

### 6. Select the kernel in the notebook

1. Open a notebook, for example `single_cell_transformations.ipynb`.
2. Choose the kernel **Python (odm-demo)**.

In Jupyter Notebook you can do this from **Kernel → Change kernel → Python (odm-demo)**. On first open you may also be prompted to pick a kernel; select **Python (odm-demo)** rather than a system Python.

If the kernel is missing from the list, confirm that the venv is still active and re-run the `ipykernel install` command from step 4.

---

## Optional: VS Code

Jupyter notebooks can also be run in **Visual Studio Code**.

1. Install the Jupyter extension (you are prompted the first time you open a `.ipynb` file).
2. Register the same kernel as in step 4 if you have not already.
3. Open the notebook and select **Python (odm-demo)** via **Select Kernel** in the top-right corner.

---

## After installation

Each demo notebook includes a short **Prerequisites → Installation** cell that checks whether `demo_utils` is already installed in the **active kernel**. If you followed the steps above and selected **Python (odm-demo)**, that cell should print `demo_utils already installed`.

---

## Authentication

The notebooks talk to an ODM instance. If you have a permanent **Genestack API token**, paste the token into the input form that appears below the cell (in Jupyter Notebook) or at the top of the notebook (in VS Code). You can also store the token in a `.env` file in this folder as `ODM_API_TOKEN=...` (do not commit that file).

---

**Contact:** support@genestack.com · © 2026 Genestack.
