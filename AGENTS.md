# AGENTS.md

Project-level operating instructions for coding agents working in this repository.

## Purpose

`langchain-lab` is a single-repo series of LangChain experiments.
Each experiment must be self-contained so new episodes can be added without breaking previous ones.

## Source Of Truth

- Treat the root `README.md` as the series index only.
- Treat each experiment README as the source of truth for that experiment.
- Do not put experiment-specific setup/run details in the root README.

## Repository Structure Rules

- Keep all experiment work under `experiments/`.
- Use numeric prefix + slug for experiment folders:
  - `experiments/01-agent-skills`
  - `experiments/02-<topic-slug>`
- Keep each experiment isolated:
  - notebooks
  - local `requirements.txt` (if needed)
  - assets/data
  - support code
  - experiment README
- Do not add new top-level project folders unless explicitly requested.

## Experiment Creation Workflow

When asked to add a new experiment:

1. Copy structure from `experiments/EXPERIMENT_TEMPLATE.md`.
2. Create `experiments/NN-<slug>/README.md`.
3. Place notebook(s) and assets inside that folder only.
4. Add/update `requirements.txt` only for that experiment.
5. Update the experiment index table in root `README.md`.

## Editing Policy

- Make the smallest safe change that solves the request.
- Preserve behavior of existing experiments unless user asks for cross-experiment refactors.
- Avoid silent breaking changes across folders.
- Prefer clear file moves over duplicating content.

## Notebook Hygiene

- Keep notebook filenames descriptive and stable once published.
- Avoid unnecessary output bloat in notebooks (large cell outputs, huge embedded data).
- If a notebook is published in a video, avoid disruptive renames unless requested.
- If code is substantial, prefer extracting reusable helpers into `.py` files inside the same experiment folder.

## Dependency Policy

- Prefer per-experiment dependencies over global root dependencies.
- If two experiments require different versions, keep them separated.
- Do not introduce monorepo-wide tooling unless explicitly requested.

## README Conventions

Root README should contain:

- short repo purpose
- high-level folder layout
- experiment index table
- “how to add experiment” guidance

Experiment README should contain:

- objective/scope
- setup instructions
- environment variables (if needed)
- run instructions
- references
- notes/caveats

## Naming Conventions

- Experiment folder: `NN-kebab-case-topic`
- Notebook files: concise, topic-specific names
- Avoid spaces in file or folder names inside `experiments/`

## Git And Commit Guidance

- Keep commits scoped to one logical change when practical.
- For restructures, use clear commit messages with `refactor:` prefix.
- Do not rewrite history unless explicitly asked.

## Safety Checks Before Finishing

Before finalizing substantial changes:

1. Verify moved paths exist and old paths are removed.
2. Verify root README links/index entries match actual folders.
3. Verify experiment README commands are runnable from that experiment directory.
4. Run a quick `git status -sb` and report key file changes.

## Collaboration Defaults

- Be concise and practical.
- If a request is ambiguous, choose the path that preserves current structure and minimizes future migration work.
- Suggest next steps only when they naturally follow the completed task.
