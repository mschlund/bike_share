# Setup instructions

## IDE
We recommend using vscode with the python-extension (https://code.visualstudio.com/docs/setup/setup-overview) -- note that you do not want to install this globally (so you do _not_ need admin-privileges!)

## Python and Package installation

### Conda (recommended for Windows Users)

Install Miniconda (https://conda.io/projects/conda/en/stable/user-guide/install/index.html)

First, we will set up a new virtual environment (you should always do this, never install stuff into your "base"-environment! See https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).
From the anaconda-prompt, install the requirements (as layed down in the .yml-file)

1. Set up a virtual environment
```
$ conda env create -f env.yml
```

2. Activate the environment
```
$ conda activate bike_share
```

3. In that environment, install the current package (in editable (-e) mode, i.e. changes made to the code are automatically available)
```
$ (bike_share) python -m pip install . -e
```

4. Open a new notebook in vscode

### Poetry (Linux/Mac-users)

Poetry is a more comfortable package-manager and (in our opinion) superior to conda (e.g. the packages installed into an environment are automatically recorded).
For Linux/Mac-users this might be more comfortable. On the other hand, Poetry and Windows can be a pain sometimes.

First, install poetry (cf. https://python-poetry.org/docs/).

We assume, that you have downloaded the current code (either clone this repository or download the code as a .zip from the github-page) and that you are in the directory where the "pyproject.toml"-file is.

1. Set up the environment

```
$ poetry install
```

2. Open a new notebook in vscode

