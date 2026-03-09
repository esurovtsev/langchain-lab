# Experiment 01: Agent Skills

This experiment demonstrates the **agent skills pattern**: give an agent compact skill metadata first, then load full guidance only when needed.

Skills are different from tools:
- **Tools** execute actions.
- **Skills** shape reasoning and decision strategy.

## References

- [Equipping agents for the real world with Agent Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills)
- [LangChain built-in middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in)
- [LangChain custom middleware](https://docs.langchain.com/oss/python/langchain/middleware/custom)

## Folder Contents

```text
01-agent-skills/
├── README.md
├── requirements.txt
├── agent_skills_demo.ipynb
├── agent_skills_model_selection.ipynb
├── skills/
│   ├── filesystem_navigation/SKILL.md
│   └── config_file_recognition/SKILL.md
└── sample_project/
```

## Setup

Run from this folder (`experiments/01-agent-skills`):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Environment

Create `.env` in this directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here

# Optional: LangSmith tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=agent-skills-demo
```

## Notebooks

- `agent_skills_demo.ipynb`: end-to-end walkthrough of progressive skill loading.
- `agent_skills_model_selection.ipynb`: model selection variation for the same pattern.

Start with:

```bash
jupyter notebook agent_skills_demo.ipynb
```

## What This Experiment Covers

1. Basic agent with filesystem middleware and no skills.
2. Skills stored in memory and loaded on demand.
3. Skills stored as filesystem `SKILL.md` files.
4. Middleware-based skill discovery/injection.

## Notes

`sample_project/` is a realistic target project used by the notebooks for exploration tasks.
