# Experiment 03: MCP as Code

This experiment explores a context-efficiency pattern for agent tooling: instead of exposing a full MCP server directly to the model, generate Python wrappers for its tools and let the agent write and run small Python programs that use those wrappers. The goal is to keep large tool catalogs and large tool results out of the model context whenever possible.

## Goal

- Show how MCP server discovery can move out of the prompt/context window and into the filesystem.
- Test a "script-first" workflow where the agent discovers wrapper files, writes Python inline, and runs it with a dedicated skill venv.
- Compare this against the direct MCP path where the agent receives the full MCP tool surface up front.
- Establish a reusable pattern for daily work, not just a one-off demo.

## Folder Contents

```text
03-mcp-as-code/
├── README.md
├── notes.md
├── mcp_as_code.ipynb
├── mcp_config.json
├── skills/
│   └── mcp-scripting/
│       ├── SKILL.md
│       ├── .venv/              # gitignored local venv
│       ├── core/
│       ├── servers/
│       └── servers.json
└── tmp/
```

## Experiment Scope

This experiment focuses on the first major problem with direct MCP usage:

- the full MCP server tool catalog is injected into context up front

That is the main thing demonstrated here. A second related problem also exists:

- large MCP results can still pollute context if the agent carelessly prints or reloads them

We explored that direction during development, but it is not the primary demo for this experiment.

## Experiment-Specific Requirements

This experiment assumes:

- the root Python environment is set up (`pip install -r requirements.txt`)
- `OPENAI_API_KEY` is available
- optional LangSmith tracing env vars are available if you want traces
- `GITHUB_PERSONAL_ACCESS_TOKEN` is available for the GitHub MCP server used in the notebook demo

Recommended trace project name:

- `LANGCHAIN_PROJECT=mcp-as-code`

## Notebook

- `mcp_as_code.ipynb`: notebook for the experiment and demo trace
- `notes.md`: implementation notes, design decisions, and article material collected during development

## Skills

The notebook uses a local skill under `skills/mcp-scripting/`.

That skill provides:

- a strict operational workflow for using MCP wrappers
- a dedicated Python venv for running inline Python
- generated wrapper files under `servers/github_mcp_server/`
- a `connect()` helper used by those wrappers

The usage pattern is:

1. load the skill dynamically
2. list the relevant wrapper directory
3. read only the wrapper file(s) needed
4. run inline Python with the skill venv
5. return only compact output

## What We Are Testing

- Whether wrapper-file discovery can replace injecting a full MCP tool catalog into the model context.
- Whether a small, strict skill can make the script-first MCP workflow reliable enough for normal use.
- Whether stronger discipline around path resolution, inline execution, and compact outputs improves repeatability.
- Whether the pattern still feels practical enough to reuse in day-to-day work with stronger models.

## Current Demo Story

The cleanest demo in this experiment is:

- direct MCP path: the model receives the GitHub MCP tool surface directly
- MCP-as-code path: the model discovers only the needed GitHub wrapper file from the filesystem and runs inline Python against it

In LangSmith, the main thing to look for is that the MCP-as-code version no longer needs the full MCP tool catalog in context.

## Notes

- This experiment keeps the usage skill intentionally strict and operational.
- The skill is not the place for maintenance or admin instructions; it only tells the agent how to use the wrappers.
- The catalog of available servers is expected to be updated separately as more MCP servers are added.
- The current local demo skill is scoped to GitHub, but the workflow pattern itself is generic.

## References

- [Anthropic: Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
