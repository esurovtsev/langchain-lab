# Experiment 01: Agent Skills

This experiment demonstrates the **agent skills pattern**: give an agent compact skill metadata first, then load full guidance only when needed.

Skills are different from tools:
- **Tools** execute actions.
- **Skills** shape reasoning and decision strategy.

## Goal

- Compare how agent behavior changes when skills are absent vs progressively introduced.
- Show a practical pattern for filesystem-based skills (`SKILL.md`) and middleware-driven loading.

## Folder Contents

```text
01-agent-skills/
├── README.md
├── agent_skills_demo.ipynb
├── agent_skills_model_selection.ipynb
├── skills/
│   ├── filesystem_navigation/SKILL.md
│   └── config_file_recognition/SKILL.md
└── sample_project/
```

## Experiment-Specific Notes

- Uses `sample_project/` as the target codebase for agent exploration.
- Recommended trace project name: `LANGCHAIN_PROJECT=agent-skills-demo`.

## Notebooks

- `agent_skills_demo.ipynb`: end-to-end walkthrough of progressive skill loading.
- `agent_skills_model_selection.ipynb`: model selection comparison for the same pattern.

## What This Experiment Covers

1. Basic agent with filesystem middleware and no skills.
2. Skills stored in memory and loaded on demand.
3. Skills stored as filesystem `SKILL.md` files.
4. Middleware-based skill discovery/injection.

## References

- [Equipping agents for the real world with Agent Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills)
- [LangChain built-in middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in)
- [LangChain custom middleware](https://docs.langchain.com/oss/python/langchain/middleware/custom)

## Notes

`sample_project/` is a realistic target project used by the notebooks for exploration tasks.
