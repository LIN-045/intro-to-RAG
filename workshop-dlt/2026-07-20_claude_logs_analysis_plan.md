# Analysis Plan: claude_logs

## Connection
pipeline: claude_logs
dataset: claude_logs_20260720091230
destination: duckdb

## Profile Summary
| table | rows | key columns | notes |
|-------|------|-------------|-------|
| events | 163 | type, timestamp, session_id, message__role, message__model, message__usage__* | temporal: timestamp; sensitive: cwd (local file paths), message__content/attachment__content (raw text/code) — not used as chart dimensions |
| events__message__content | 101 | type, name (tool name), tool_use_id | tool_use rows carry the tool name used per assistant turn |
| events__message__usage__iterations | 66 | input_tokens, output_tokens, cache_read_input_tokens | per-iteration token usage detail |

Data spans a single ~31-minute window on 2026-07-20 across 3 sessions (2 under `/Users/linjiaxi`, 1 under `/Users/linjiaxi/Learning/intro-to-RAG`).

## Questions
1. [x] How does my Claude Code activity break down over time? → Chart 1
2. [x] What kinds of events make up my usage? → Chart 2
3. [x] What's the split between my messages and the assistant's? → Chart 3
4. [x] Where is my token usage going (input/output/cache)? → Chart 4
5. [x] Which tools does Claude use most on my behalf? → Chart 5
6. [x] How active is each of my sessions? → Chart 6

## Data Gaps
(none)

## Chart 1: Activity Timeline
question: How does my Claude Code activity break down over time?
type: stacked bar
x: timestamp (minute)
y: count(*)
source: events

```sql
SELECT
    DATE_TRUNC('minute', timestamp) AS minute,
    type,
    COUNT(*) AS events
FROM events
WHERE timestamp IS NOT NULL
GROUP BY 1, 2
ORDER BY 1
```

```altair
alt.Chart(df).mark_bar().encode(
    x=alt.X("minute:T", title="Time"),
    y=alt.Y("events:Q", title="Events"),
    color=alt.Color("type:N", title="Event type"),
    tooltip=["minute:T", "type:N", "events:Q"]
).properties(title="Activity Timeline")
```

## Chart 2: Event Type Breakdown
question: What kinds of events make up my usage?
type: bar
x: type
y: count(*)
source: events

```sql
SELECT type, COUNT(*) AS events
FROM events
GROUP BY 1
ORDER BY events DESC
```

```altair
alt.Chart(df).mark_bar().encode(
    x=alt.X("events:Q", title="Events"),
    y=alt.Y("type:N", sort="-x", title="Event type"),
    tooltip=["type:N", "events:Q"]
).properties(title="Event Type Breakdown")
```

## Chart 3: Message Role Distribution
question: What's the split between my messages and the assistant's?
type: bar
x: message__role
y: count(*)
source: events

```sql
SELECT message__role AS role, COUNT(*) AS messages
FROM events
WHERE message__role IS NOT NULL
GROUP BY 1
ORDER BY messages DESC
```

```altair
alt.Chart(df).mark_bar().encode(
    x=alt.X("role:N", title="Role"),
    y=alt.Y("messages:Q", title="Messages"),
    color=alt.Color("role:N", legend=None),
    tooltip=["role:N", "messages:Q"]
).properties(title="Message Role Distribution")
```

## Chart 4: Token Usage Breakdown
question: Where is my token usage going (input/output/cache)?
type: bar
x: token_type
y: sum(tokens)
source: events

```sql
SELECT 'input' AS token_type, SUM(message__usage__input_tokens) AS tokens FROM events
UNION ALL
SELECT 'output', SUM(message__usage__output_tokens) FROM events
UNION ALL
SELECT 'cache_read', SUM(message__usage__cache_read_input_tokens) FROM events
UNION ALL
SELECT 'cache_creation', SUM(message__usage__cache_creation_input_tokens) FROM events
```

```altair
alt.Chart(df).mark_bar().encode(
    x=alt.X("tokens:Q", title="Tokens"),
    y=alt.Y("token_type:N", sort="-x", title="Token type"),
    tooltip=["token_type:N", "tokens:Q"]
).properties(title="Token Usage Breakdown")
```

## Chart 5: Tool Usage Frequency
question: Which tools does Claude use most on my behalf?
type: bar
x: name
y: count(*)
source: events__message__content

```sql
SELECT name AS tool, COUNT(*) AS uses
FROM events__message__content
WHERE type = 'tool_use'
GROUP BY 1
ORDER BY uses DESC
```

```altair
alt.Chart(df).mark_bar().encode(
    x=alt.X("uses:Q", title="Uses"),
    y=alt.Y("tool:N", sort="-x", title="Tool"),
    tooltip=["tool:N", "uses:Q"]
).properties(title="Tool Usage Frequency")
```

## Chart 6: Session Activity
question: How active is each of my sessions?
type: bar
x: session
y: count(*)
source: events

```sql
SELECT
    SUBSTR(session_id, 1, 8) AS session,
    cwd,
    COUNT(*) AS events
FROM events
WHERE session_id IS NOT NULL
GROUP BY 1, 2
ORDER BY events DESC
```

```altair
alt.Chart(df).mark_bar().encode(
    x=alt.X("events:Q", title="Events"),
    y=alt.Y("session:N", sort="-x", title="Session"),
    color=alt.Color("cwd:N", title="Working dir"),
    tooltip=["session:N", "cwd:N", "events:Q"]
).properties(title="Session Activity")
```
