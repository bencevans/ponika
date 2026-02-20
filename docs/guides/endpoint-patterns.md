# Endpoint Patterns

Ponika maps device API paths into endpoint classes attached to `PonikaClient`.

## Structure

- Top-level client attributes represent endpoint groups (`gps`, `messages`, `modems`).
- Nested endpoint objects represent deeper API paths (`gps.position`, `wireless.interfaces`).
- Endpoint methods commonly follow `get_status()`, `get_config()`, or `post_*` naming.

## Response Modeling

- Each endpoint method returns `ApiResponse[T]`.
- `success` indicates request status.
- `data` carries typed payloads using Pydantic models.
- `errors` contains API error details when `success` is false.

## Example: Nested Endpoint Access

```python
response = client.gps.position.get_status()
if response.success and response.data:
    print(response.data.latitude, response.data.longitude)
```

## Adding a New Endpoint

1. Add a new endpoint module under `src/ponika/endpoints`.
2. Create response models with `pydantic.BaseModel`.
3. Use `_client._get(...)` or `_client._post(...)` inside endpoint methods.
4. Register the endpoint in `PonikaClient.__init__`.
5. Add tests that validate both successful and error responses.

API docs are generated from code, so new classes and methods appear automatically after build.
