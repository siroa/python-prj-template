## Require
- poetry (version1.8.3)
- python (version 3.12)

- charliermarsh.ruff(2024.42.0)
- ms-python.mypy-type-checker (v2023.6.0)

## Setup
- Normal
```
poetry install
```
- no dev
```
poetry install --without dev
```
※Deprecated: ```poetry install --no-dev```

## Add package
```
poetry add <package-name>
```

## Update package
```
poetry update --dry-run
poetry update
```

## Run
```
poetry run python <python-file>
```

## Test
```
export test=test
poetry run pytest --cov=python_prj_template
```