# LangChain Lab

A single repository for a series of focused LangChain experiments on agent behavior, tooling, and workflow design.

This repo is organized as a lab notebook for videos and hands-on explorations.  
Each experiment lives in its own folder so it can evolve independently without forcing a new GitHub repository.

## What This Repo Is For

- Keep all experiment work in one place.
- Preserve reproducibility for older episodes while adding new ones.
- Make it easy to browse by topic and run only what you need.
- Explore how different agent interfaces, guidance patterns, and tool setups affect behavior in practice, including when existing CLIs may be more practical than dedicated agent protocols.

## Shared Prerequisites

These are common expectations across experiments:

- Python 3.11+ available locally.
- Jupyter installed and runnable.
- `OPENAI_API_KEY` available in your environment.
- Optional LangSmith env vars if tracing is needed (`LANGCHAIN_TRACING_V2`, `LANGCHAIN_API_KEY`, `LANGCHAIN_PROJECT`).

## First-Time Setup

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Shared Environment Configuration

Set environment variables once for all experiments.

Option A: export in your shell session

```bash
export OPENAI_API_KEY="your_openai_api_key_here"
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY="your_langsmith_api_key_here"
export LANGCHAIN_PROJECT="langchain-lab"
```

Option B: create a root `.env` file

```bash
OPENAI_API_KEY=your_openai_api_key_here

# Optional: LangSmith tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=langchain-lab
```

Use experiment-specific `LANGCHAIN_PROJECT` values only when you want separate traces by experiment.

## How To Use The Lab

1. Pick an experiment from the index below.
2. Open that experiment's `README.md`.
3. Install shared dependencies once from root (`pip install -r requirements.txt`).
4. Run the notebook(s) from that experiment directory.

## Repository Layout

```text
.
├── experiments/
│   ├── mcp_helpers.py
│   ├── notebook_helpers.py
│   ├── 01-agent-skills/
│   ├── 02-cli-vs-mcp/
│   ├── 03-mcp-as-code/
│   └── EXPERIMENT_TEMPLATE.md
├── LICENSE
└── README.md
```

## Experiment Index

| # | Experiment | Folder |
|---|---|---|
| 01 | Agent Skills | `experiments/01-agent-skills` |
| 02 | CLI vs MCP (CLI-First Agents) | `experiments/02-cli-vs-mcp` |
| 03 | MCP as Code | `experiments/03-mcp-as-code` |

## How To Add A New Experiment

1. Create a new folder using a numeric prefix, for example: `experiments/04-tools-routing`.
2. Add an experiment-specific `README.md` inside that folder.
3. Put notebooks and assets in that same folder.
4. Update root `requirements.txt` only if the new experiment needs extra packages.
5. Add a new row to the table above.

## Convention

- Keep experiment code and data self-contained inside its own folder.
- Do not put experiment-specific instructions in the root README.
- Use the root README as the series guide and index.

## License

MIT
