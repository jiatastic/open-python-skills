# Docker Builder Pitfalls

## Common Issues

- **Large images**: build deps included in runtime image
- **Slow builds**: cache invalidated by copying source too early
- **Running as root**: avoid privileged containers
- **Broken signals**: shell-form CMD prevents SIGTERM handling

## Fix Patterns

- Use multi-stage builds to separate build/runtime
- Copy lock files first (`requirements.txt`, `pyproject.toml`)
- Add a non-root user for runtime
- Use exec-form `CMD` or `ENTRYPOINT`

## Example: Cache-friendly Ordering

```Dockerfile
COPY pyproject.toml poetry.lock ./
RUN pip install -U pip && pip install -r requirements.txt
COPY . .
```
