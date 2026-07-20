import marimo

__generated_with = "0.23.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import altair as alt
    import dlt

    return alt, dlt, mo


@app.cell
def _(dlt):
    pipeline = dlt.attach("claude_logs")
    dataset = pipeline.dataset()
    return (dataset,)


@app.cell
def _(mo):
    mo.md("""
    # Claude Code Usage Report
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Activity Timeline
    """)
    return


@app.cell
def _(dataset):
    df_chart1 = dataset("""
        SELECT
            DATE_TRUNC('minute', timestamp) AS minute,
            type,
            COUNT(*) AS events
        FROM events
        WHERE timestamp IS NOT NULL
        GROUP BY 1, 2
        ORDER BY 1
    """).df()
    return (df_chart1,)


@app.cell
def _(alt, df_chart1):
    _chart = alt.Chart(df_chart1).mark_bar().encode(
        x=alt.X("minute:T", title="Time"),
        y=alt.Y("events:Q", title="Events"),
        color=alt.Color("type:N", title="Event type"),
        tooltip=["minute:T", "type:N", "events:Q"]
    ).properties(title="Activity Timeline")
    _chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## Event Type Breakdown
    """)
    return


@app.cell
def _(dataset):
    df_chart2 = dataset("""
        SELECT type, COUNT(*) AS events
        FROM events
        GROUP BY 1
        ORDER BY events DESC
    """).df()
    return (df_chart2,)


@app.cell
def _(alt, df_chart2):
    _chart = alt.Chart(df_chart2).mark_bar().encode(
        x=alt.X("events:Q", title="Events"),
        y=alt.Y("type:N", sort="-x", title="Event type"),
        tooltip=["type:N", "events:Q"]
    ).properties(title="Event Type Breakdown")
    _chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## Message Role Distribution
    """)
    return


@app.cell
def _(dataset):
    df_chart3 = dataset("""
        SELECT message__role AS role, COUNT(*) AS messages
        FROM events
        WHERE message__role IS NOT NULL
        GROUP BY 1
        ORDER BY messages DESC
    """).df()
    return (df_chart3,)


@app.cell
def _(alt, df_chart3):
    _chart = alt.Chart(df_chart3).mark_bar().encode(
        x=alt.X("role:N", title="Role"),
        y=alt.Y("messages:Q", title="Messages"),
        color=alt.Color("role:N", legend=None),
        tooltip=["role:N", "messages:Q"]
    ).properties(title="Message Role Distribution")
    _chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## Token Usage Breakdown
    """)
    return


@app.cell
def _(dataset):
    df_chart4 = dataset("""
        SELECT 'input' AS token_type, SUM(message__usage__input_tokens) AS tokens FROM events
        UNION ALL
        SELECT 'output', SUM(message__usage__output_tokens) FROM events
        UNION ALL
        SELECT 'cache_read', SUM(message__usage__cache_read_input_tokens) FROM events
        UNION ALL
        SELECT 'cache_creation', SUM(message__usage__cache_creation_input_tokens) FROM events
    """).df()
    return (df_chart4,)


@app.cell
def _(alt, df_chart4):
    _chart = alt.Chart(df_chart4).mark_bar().encode(
        x=alt.X("tokens:Q", title="Tokens"),
        y=alt.Y("token_type:N", sort="-x", title="Token type"),
        tooltip=["token_type:N", "tokens:Q"]
    ).properties(title="Token Usage Breakdown")
    _chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## Tool Usage Frequency
    """)
    return


@app.cell
def _(dataset):
    df_chart5 = dataset("""
        SELECT name AS tool, COUNT(*) AS uses
        FROM events__message__content
        WHERE type = 'tool_use'
        GROUP BY 1
        ORDER BY uses DESC
    """).df()
    return (df_chart5,)


@app.cell
def _(alt, df_chart5):
    _chart = alt.Chart(df_chart5).mark_bar().encode(
        x=alt.X("uses:Q", title="Uses"),
        y=alt.Y("tool:N", sort="-x", title="Tool"),
        tooltip=["tool:N", "uses:Q"]
    ).properties(title="Tool Usage Frequency")
    _chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## Session Activity
    """)
    return


@app.cell
def _(dataset):
    df_chart6 = dataset("""
        SELECT
            SUBSTR(session_id, 1, 8) AS session,
            cwd,
            COUNT(*) AS events
        FROM events
        WHERE session_id IS NOT NULL
        GROUP BY 1, 2
        ORDER BY events DESC
    """).df()
    return (df_chart6,)


@app.cell
def _(alt, df_chart6):
    _chart = alt.Chart(df_chart6).mark_bar().encode(
        x=alt.X("events:Q", title="Events"),
        y=alt.Y("session:N", sort="-x", title="Session"),
        color=alt.Color("cwd:N", title="Working dir"),
        tooltip=["session:N", "cwd:N", "events:Q"]
    ).properties(title="Session Activity")
    _chart
    return


if __name__ == "__main__":
    app.run()
