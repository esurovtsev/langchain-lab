# LangChain Lab

A single repository for a series of LangChain experiments.

The goal is to keep each experiment isolated, reproducible, and easy to extend without creating a new repo every time.

## Repository Layout

```text
.
├── experiments/
│   └── 01-agent-skills/
│       ├── README.md
│       ├── requirements.txt
│       ├── agent_skills_demo.ipynb
│       ├── agent_skills_model_selection.ipynb
│       ├── skills/
│       └── sample_project/
├── LICENSE
└── README.md
```

## Experiment Index

| # | Experiment | Folder | Status |
|---|---|---|---|
| 01 | Agent Skills | `experiments/01-agent-skills` | Active |

## How To Add A New Experiment

1. Create a new folder using a numeric prefix, for example: `experiments/02-tools-routing`.
2. Add an experiment-specific `README.md` inside that folder.
3. Put notebooks, assets, and local dependencies in that same folder.
4. If dependencies differ, create a local `requirements.txt` for that experiment.
5. Add a new row to the table above.

## Convention

- Keep experiment code and data self-contained inside its own folder.
- Do not put experiment-specific instructions in the root README.
- Use the root README only as a navigation/index page for the whole series.

## License

MIT
