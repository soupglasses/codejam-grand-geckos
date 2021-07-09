# Codejam 8 - Team Grand Geckos

[About Python Discord's Code Jam 8](https://pythondiscord.com/events/code-jams/8/)

## Development

### Dependencies:

To install poetry and pre-commit:
```bash
pip install --user poetry
pip install pre-commit
```

### First Time Setup:

```bash
git clone https://github.com/imsofi/codejam-grand-geckos
cd codejam-grand-geckos
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
python3 -m grand_geckos
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
