# Codejam 8 - Team Grand Geckos

[About Python Discord's Code Jam 8](https://pythondiscord.com/events/code-jams/8/)

## Development

Requires Python 3.8 or higher

### Dependency:

```bash
pip install --user poetry
```

### First Time Setup:

```bash
git clone https://github.com/imsofi/codejam-grand-geckos
cd codejam-grand-geckos
poetry install
poetry run pre-commit install
```

### Running the Project:

Using poetry run:
```bash
poetry run task main
```

If you are in a `poetry shell`:
```bash
python3 -m grand_geckos
```

### Before Commiting/Pushing:

Its reccomended to run it trough the linters manually:

With poetry:
```bash
poetry run task lint
```

Or run it trough `poetry shell`:
```bash
pre-commit run --all-files
```
