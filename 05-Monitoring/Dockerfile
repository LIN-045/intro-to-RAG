FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked --no-install-project

COPY 05-Monitoring/*.py ./05-Monitoring/

WORKDIR /app/05-Monitoring

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]