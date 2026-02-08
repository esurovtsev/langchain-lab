# Agent Skills Guide

This project demonstrates the **agent skills pattern** — a mechanism for giving agents on-demand knowledge that shapes how they reason, without permanently bloating their context.

Skills are **not tools**. Tools perform actions (read a file, search, execute shell). Skills contain **guidelines, heuristics, and reasoning strategies** that teach the agent *how to think about a task*. A skill is closer to a runbook or a decision framework — not a function call.

This repo exists to make that pattern obvious and inspectable.

## References

- [Equipping agents for the real world with Agent Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills) — Anthropic blog
- [Prebuilt middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in) — LangChain built-in middleware
- [Custom middleware](https://docs.langchain.com/oss/python/langchain/middleware/custom) — LangChain custom middleware

## Project Structure

```
├── agent_skills_demo.ipynb      # Main notebook — progressive skill pattern guide
├── sample_project/              # A real project for the agent to explore
├── skills/                      # Skill files (Claude Code convention)
│   ├── filesystem_navigation/
│   │   └── SKILL.md
│   └── config_file_recognition/
│       └── SKILL.md
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the Repository

```bash
git clone git@github.com:esurovtsev/langchain-agent-skills.git
cd langchain-agent-skills
```

### 2. Set Up Your Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory with your API keys:

```bash
OPENAI_API_KEY=your_openai_api_key_here

# Optional: LangSmith for tracing and debugging
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=agent-skills-demo
```

**Note**: Never commit `.env` files to version control.

### 5. Open the Notebook

```bash
jupyter notebook agent_skills_demo.ipynb
```

## What the Notebook Covers

The notebook progresses through four stages, each building on the previous:

1. **Basic Agent** — built-in filesystem middleware, no skills. The agent works but reasons naively.
2. **Skills In Memory** — skills as Python dicts, loaded via a `load_skill` tool. The agent reasons with guidance.
3. **Skills on Filesystem** — skills stored as `SKILL.md` files with YAML frontmatter. Portable, progressive disclosure.
4. **SkillMiddleware** — a proper `AgentMiddleware` class that auto-discovers skills and injects them cleanly.

All stages use the same test prompt so you can compare behavior across configurations.

## How Skills Work

Each skill is a directory containing a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: filesystem_navigation
description: Guidelines for systematically exploring directory structures.
---

# Filesystem Navigation
## Strategy
...
```

The agent sees **only the name and description** in its system prompt. When it needs deeper guidance, it calls `load_skill("filesystem_navigation")` to load the full content. Skills can also reference additional files in their directory for even deeper detail (Level 3 progressive disclosure), though this is outside the scope of the guide.

To add a new skill, create a new folder under `skills/` with a `SKILL.md`. No code changes needed.

## License

MIT
