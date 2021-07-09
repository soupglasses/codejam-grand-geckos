# exploring-git

## Development

### First Time Setup:

```bash
git clone REPO_LINK
cd REPO_NAME
poetry install
pre-commit install
```

### Running the Project:

If you are not using `poetry shell`:
```bash
poetry run task main
```

If you are using `poetry shell`:
```bash
python3 -m REPO_NAME
```

### Running Tests:

```bash
poetry run task test
```

### Before Commiting/Pushing:

You should run it trough the linters:

With poetry:
```bash
poetry run task lint
```

Or run it trough `poetry shell`:
```bash
pre-commit run --all-files
```
