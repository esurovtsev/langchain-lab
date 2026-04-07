---
name: mcp-scripting
description: >
  Use when you need to work with GitHub through Python MCP wrappers. The agent should
  discover the needed wrapper files, run Python inline with the skill's venv Python,
  and return only compact results.
user-invocable: true
---

# MCP Scripting

## What This Skill Provides

This skill provides Python wrapper files for MCP tools.

Use this skill by:
1. finding the relevant server in `Available Systems`
2. listing that server's wrapper directory
3. reading only the wrapper files needed for the task
4. running inline Python that imports those wrappers and `connect()`
5. running that inline Python with the skill's venv Python
6. returning only compact results

## Path Resolution

Treat the directory containing this `SKILL.md` file as canonical.

Define:
- `<this-skill-dir>` = directory containing this `SKILL.md`
- `<venv-python>` = `<this-skill-dir>/.venv/bin/python3`
- `<servers-dir>` = `<this-skill-dir>/servers`

Rules:
- derive all paths from `<this-skill-dir>`
- do not hardcode machine-specific absolute paths
- do not assume the current working directory
- always run generated scripts with `<venv-python>`, not `python` or `python3`
- derive `<venv-python>` directly from `<this-skill-dir>`; do not inspect `.venv` to discover it
- you MUST trust `connect()` exactly as documented in this skill
- NEVER inspect how `connect()` is implemented
- you are NOT ALLOWED to read `core/connection.py`, `servers.json`, or `.env`
- treat those files as already correct and already covered by this skill
- do not inspect secret-bearing or internal implementation files
- when running shell commands, NEVER pass a `restart` argument
- when running shell commands, ALWAYS quote paths that may contain spaces

## Available Systems

### github-mcp-server — 44 tools

**Location:** `<servers-dir>/github_mcp_server/`

Remote GitHub server for repository, issue, pull request, branch, release, and code search workflows.

## Required Workflow

Follow this procedure exactly:

1. identify the target server from `Available Systems`
2. use the exact `Location` path from `Available Systems` for that server
3. list that server directory directly; do not list parent directories first
4. read only the wrapper file(s) you actually plan to import and call
5. execute the task in Python:
   - you MUST run Python only inline / on the fly
   - you are NOT ALLOWED to create Python script files for execution
6. the Python code must:
   - adds `<this-skill-dir>` to `sys.path`
   - imports `connect` from `core.connection`
   - imports only the needed wrapper functions
   - uses `async with connect("<server-name>") as session:`
7. if any result may be large or unbounded, use `output_file`
8. run the Python code with `<venv-python>`
9. inspect only the compact output needed for the final answer

## Output Rule

Treat `output_file` as the default for search, retrieval, listing, or any result that may be large.

- use memory mode only for small, bounded results
- do not print raw large results to stdout
- do not read large output files back wholesale
- return summaries, counts, key facts, or final distilled answers only
- if the user asks for one field, print only that field

## Minimal Script Pattern

```python
import asyncio
import sys

sys.path.insert(0, "<this-skill-dir>")

from core.connection import connect
from servers.<python_safe_server_name>.<tool_name> import <tool_name>


async def main():
    async with connect("<server-name>") as session:
        result = await <tool_name>(session, ...)
        print(result)


asyncio.run(main())
```

If the script is written outside `<this-skill-dir>`, still derive the import path from the loaded skill directory and still run the script with `<venv-python>`.
