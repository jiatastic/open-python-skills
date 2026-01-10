#!/usr/bin/env python3
"""Generate a minimal Dockerfile template for Python APIs."""

from textwrap import dedent


def main() -> None:
    dockerfile = dedent(
        """
        FROM python:3.12-slim AS runtime
        ENV PYTHONUNBUFFERED=1
        WORKDIR /app

        COPY pyproject.toml ./
        RUN pip install -U pip && pip install -e .

        COPY . .
        EXPOSE 8000
        CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
        """
    ).strip()
    print(dockerfile)


if __name__ == "__main__":
    main()
