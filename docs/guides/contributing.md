# Contributing

## Setup

/// tab | SSH

    :::bash
    git clone git@github.com:bencevans/ponika.git
    cd ponika
    uv sync
///

/// tab | HTTPS

    :::bash
    git clone git@github.com:bencevans/ponika.git
    cd ponika
    uv sync
///


## Code Structure

Key project paths:

- `src/ponika/__init__.py`: exports `PonikaClient` and wires endpoint groups onto the client.
- `src/ponika/models.py`: shared response and error models (`ApiResponse`, `TeltonikaApiError`, `Token`).
- `src/ponika/endpoints/`: endpoint modules grouped by API area (for example `gps.py`, `modems.py`, `wireless.py`).
- `src/ponika/test_client.py`: integration-style tests that exercise endpoint methods against a device.

When adding new functionality:

1. Add request/response models and endpoint methods in `src/ponika/endpoints/<area>.py`.
2. Register the endpoint on `PonikaClient` in `src/ponika/__init__.py` if it is a new top-level group.
3. Add or extend tests in `src/ponika/test_client.py`.
4. Run lint and tests before opening a PR.

## Run Tests

The test suite is designed to run against a real Teltonika device. To run tests, set the following environment variables with the appropriate connection parameters:

```bash
export TELTONIKA_HOST=192.168.1.1
export TELTONIKA_USERNAME=admin
export TELTONIKA_PASSWORD=password
```

Optionally set `MOBILE_NUMBER` to a number you can receive SMS on for testing SMS functionality.

Run tests:

```bash
uv run pytest
```

## Lint

Ponika uses Ruff for linting. To check for linting issues, run:

```bash
uv run ruff check .
```

## Build Docs

Serve docs locally:

```bash
uv run mkdocs serve
```

Build static docs:

```bash
uv run mkdocs build --strict
```

The API reference section is generated automatically from the package modules.
