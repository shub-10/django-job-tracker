# Job Tracker API

## Requirements

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/)

## Setup

From the `backend` directory:

```bash
uv sync --dev
```

## Run locally

```bash
uv run python manage.py runserver
```

The API is available at <http://127.0.0.1:8000>. The health endpoint is
<http://127.0.0.1:8000/api/health/>.

## Test

```bash
uv run python manage.py test
```
