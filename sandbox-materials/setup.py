from setuptools import find_packages, setup

setup(
    name="demo_utils",
    version="0.1.0",
    description="Helper package for Genestack ODM demo notebooks",
    packages=find_packages(include=["demo_utils", "demo_utils.*"]),
    python_requires=">=3.10",
    install_requires=[
        # core scientific libraries
        "numpy>=1.24",
        "pandas>=2.1",
        "scipy>=1.11",

        # plotting
        "matplotlib>=3.7",
        "seaborn>=0.13",
        "plotly>=5.18",

        # notebook / jupyter
        "ipykernel>=6.0",
        "ipython>=8.0",
        "jinja2>=3.0",
        "nbformat>=4.2.0",

        # config / auth
        "azure-identity>=1.15",
        "python-dotenv>=1.0",

        # bioinformatics / single-cell
        "pydeseq2>=0.4",
        "gseapy>=1.1",
        "anndata>=0.10",
        "scanpy>=1.10",

        # genestack odm sdk
        "odm-sdk>=1.63.4",
    ],
)
