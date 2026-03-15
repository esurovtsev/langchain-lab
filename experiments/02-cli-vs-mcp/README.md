# Experiment 02: CLI vs MCP (GitHub)

This experiment studies a broader shift in agent tooling: moving from MCP-first integrations toward CLI-first integrations. The goal is not to evaluate GitHub CLI specifically, but to use GitHub as a practical, safe case study for testing a newer idea in the ecosystem: that many workflows people modeled through MCP may have already had a viable interface in the form of an existing CLI.

## Goal

- Compare the same task across MCP and CLI execution paths.
- Test the broader migration question: when can an existing CLI replace an MCP integration that teams previously treated as the default agent interface?
- Observe the tradeoff between protocol-level structure and reuse of an interface that already exists for humans.
- Test whether prompt hints and reusable skills can make a CLI-based agent reliable enough to support that migration.
- Identify which failures come from model behavior, which come from CLI ambiguity, which come from capability wiring, and which come from the skill instructions themselves.

## Folder Contents

```text
02-cli-vs-mcp/
├── skills/
│   └── github-cli/
│       └── SKILL.md
├── README.md
├── mcp_helpers.py
├── mcp_config.json
└── cli_vs_mcp_experiment.ipynb
```

## Experiment-Specific Requirements

You will also need GitHub authentication for the specific path being tested:

- MCP path: GitHub MCP server credentials/config.
- CLI path: local `gh auth login` (or equivalent).
- Recommended trace project name: `LANGCHAIN_PROJECT=cli-vs-mcp`.

This experiment also assumes:

- `gh` is installed locally and available on `PATH`.
- The GitHub account used by `gh` has access to the repositories being inspected.
- `GITHUB_PERSONAL_ACCESS_TOKEN` is available for the MCP configuration if you want to run the MCP path.

## Notebook

- `cli_vs_mcp_experiment.ipynb`: runs the GitHub task through several stages so behavior can be compared rather than guessed:
  - MCP path with GitHub MCP tools
  - shell path with no special CLI guidance
  - shell path with `SkillsMiddleware`
  - shell path with both skills and filesystem access so the agent can discover and read `SKILL.md`
- `mcp_helpers.py`: helper utilities for loading MCP server config, resolving env placeholders, redacting sensitive values, and printing discovered MCP tools.
- `skills/github-cli/SKILL.md`: reusable deterministic workflow for authenticated GitHub analysis via `gh`.

## What We Are Testing

- Whether a structured MCP tool surface actually produces better behavior than a mature CLI that already existed as an alternative interface.
- Whether existing CLI affordances such as auth, inspectability, and composability reduce integration work compared with MCP.
- Whether a skill can act as the missing operational documentation layer for CLI use, instead of building a dedicated MCP server.
- Whether the debugging story is better when both the human and the agent can run the same commands.
- Where CLI-first workflows break down and should still be promoted to dedicated tools.
- GitHub is only the case study here; the larger question is about interface strategy for agent integrations in general.

## Notes

- Keep the user task identical across MCP and CLI runs for fair comparison.
- The CLI path is intentionally tested under multiple setup levels because the experiment is not about GitHub alone; it is about what has to be added when teams migrate a workflow away from MCP and onto an existing CLI.
- Skills are part of the experiment design: they let us test whether reusable operational instructions can substitute for protocol-level structure in common workflows.
- A key part of the notebook is separating three kinds of failure:
  - missing capability wiring
  - model reasoning/tool-choice mistakes
  - incorrect or incomplete skill instructions
- This experiment is useful when deciding whether a workflow should stay as CLI automation, be wrapped in a skill, or be promoted to a dedicated MCP tool interface.

## Why This Experiment Matters

- MCP gives the model a constrained action space with named tools and structured arguments, but it also introduces extra integration surface area.
- CLI reuses interfaces that already exist for humans: commands, auth flows, debugging habits, and composable pipelines.
- In real systems, teams often already had a stable CLI while still treating MCP as the agent-facing answer. This experiment tests that assumption directly.
- The practical question is not whether CLI exists, but whether CLI + guidance is strong enough to justify migrating work away from MCP.

## References

- [GitHub CLI](https://cli.github.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
