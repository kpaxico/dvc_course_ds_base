# course-ds-base

## Preparation

### 1. Fork / Clone this repository

```bash
git clone https://github.com/iterative/course-ds-base.git
cd course-ds-base
```

### 2. Create and activate virtual environment

Create virtual environment named `dvc-venv` (you may use other name)

```bash
python3 -m venv dvc-venv
echo "export PYTHONPATH=$PWD" >> dvc-venv/bin/activate
source dvc-venv/bin/activate
```

Install python libraries

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Add Virtual Environment to Jupyter Notebook

```bash
python -m ipykernel install --user --name=dvc-venv
```

Configure ToC for jupyter notebook (optional)

```bash
jupyter contrib nbextension install --user
jupyter nbextension enable toc2/main
```

## 3. Run Jupyter Notebook

```bash
jupyter notebook
```

## 4. Push DVC data

If you'd like to test commands like [`dvc push`](https://man.dvc.org/push),
that require write access to the remote storage, the easiest way would be to set
up a "local remote" on your file system:

> This kind of remote is located in the local file system, but is external to
> the DVC project.

```console
mkdir -p /tmp/dvc_course_ds_base_storage
dvc remote add -d local /tmp/dvc_course_ds_base_storage
```

You should now be able to run:

```console
dvc push
```

Or by specifying the remote:

```console
dvc push -r local
```

## 5. NOTES

## 5.1 `dvc status`

`dvc status` (by default) only checks your local workspace against `dvc.lock`.

> It does not check whether your data or outputs are pushed to the remote DVC storage.

To check if your outputs are pushed to the remote storage, you need to run:

```bash
dvc status -c
```

## 5.2 Depndency to the code files

for example for the `data_load` stage `src/stages/data_load.py` is a dependency. So, it's tracked by DVC. But I think it's also tracked by Git.

You are absolutely correct!

`data_load.py` is listed as a dependency (dep) in your `dvc.yaml` for the `data_load` stage.
DVC tracks it as a **dependency** for pipeline execution: if this file changes, DVC knows to rerun the stage.
However, DVC does not store or version-control the actual contents of .py scripts or code files. It just monitors them for changes.
The actual version control (history, diffs, etc.) for data_load.py is handled by Git, not DVC.

Summary:

Code files (like .py scripts) are tracked by Git.
DVC tracks them as dependencies for pipeline logic, but does not store their contents in DVC storage.
Data files (outputs, large datasets, models, etc.) are tracked and stored by DVC.
