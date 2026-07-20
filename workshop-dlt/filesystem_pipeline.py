"""dlt filesystem pipeline: load Claude Code session logs (JSONL) from ~/.claude/projects into DuckDB."""

import dlt
from dlt.sources.filesystem import filesystem, read_jsonl


def load_events() -> None:
    """Load Claude Code session log events into DuckDB.

    bucket_url is read from .dlt/config.toml under [sources.filesystem].
    file_glob is set inline so it lives next to the code that depends on it.
    """
    pipeline = dlt.pipeline(
        pipeline_name="claude_logs",
        destination="duckdb",
        dataset_name="claude_logs",
        dev_mode=True,  # fresh dataset on every run during dev
    )

    reader = (filesystem(file_glob="**/*.jsonl") | read_jsonl()).with_name("events")

    load_info = pipeline.run(reader, write_disposition="replace")
    print(load_info)
    print(pipeline.last_trace.last_normalize_info)


if __name__ == "__main__":
    load_events()
