"""dlt REST API pipeline: load trace/span data from Pydantic Logfire's Query API into DuckDB.

Logfire's Query API (https://pydantic.dev/docs/logfire/manage/query-api/) exposes a single
POST endpoint (`/v2/query`) that runs a SQL query against the `records` table (spans/traces)
and returns rows as JSON under the `data` key.
"""

import os
from typing import Any, Optional

import dlt
import pendulum
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources
from dotenv import load_dotenv

load_dotenv()


@dlt.source(name="logfire")
def logfire_source(
    access_token: str = dlt.secrets.value,
    base_url: str = "https://logfire-us.pydantic.dev/",
    min_timestamp: Optional[str] = None,
) -> Any:
    """Load trace/span records from Logfire's Query API.

    Args:
        access_token: Logfire read token (Bearer auth). Auto-loaded from secrets.toml.
        base_url: Region-specific Logfire API base URL. Defaults to the US region.
        min_timestamp: ISO8601 lower bound for the query, required by the Logfire API.
            Defaults to 7 days ago.
    """
    if min_timestamp is None:
        min_timestamp = pendulum.now("UTC").subtract(days=7).to_iso8601_string()

    config: RESTAPIConfig = {
        "client": {
            "base_url": base_url,
            "headers": {"Accept": "application/json"},
            "auth": {
                "type": "bearer",
                "token": access_token,
            },
        },
        "resources": [
            {
                "name": "traces",
                "endpoint": {
                    "path": "v2/query",
                    "method": "POST",
                    "json": {
                        "sql": "SELECT * FROM records",
                        "min_timestamp": min_timestamp,
                    },
                    "data_selector": "data",
                },
            },
        ],
    }

    yield from rest_api_resources(config)


def load_traces() -> None:
    access_token = os.environ["LOGFIRE_READ_TOKEN"]

    pipeline = dlt.pipeline(
        pipeline_name="logfire",
        destination="duckdb",
        dataset_name="agent_traces",
    )

    load_info = pipeline.run(
        logfire_source(access_token=access_token),
        write_disposition="replace",
    )
    print(load_info)  # noqa: T201


if __name__ == "__main__":
    load_traces()
