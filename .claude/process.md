# General
* No code without a task; no task without a feature; no feature contradicting the spec.
* After creating a feature + task file, stop and present the plan — no code until approved.
* Don't close a feature until its full test suite exists and passes.
* Exception: simple bug fixes/refactors (no spec/behavior change) skip the feature/task pair — log as a chore.
* Any bug fix or regression gets a test.
* Switching between task/feature/chore: stop and ask permission first.

# chores
* One running file, `04-tasks/chores.md`: `- [ ] <what and why>` → `- [x]` when applied.

# features
* `FNN-<slug>.md` in `03-features/{notdone,done,deferred}/`; a mini-spec — scope/intent, not task detail.
* `Tasks File Created: yes` only once a matching `04-tasks/TFNN-*.md` exists. `feature-template.md` shows the format.

# tasks
* Full task list before any design/code. `TFNN-<slug>.md` (`NN` matches the feature) in `04-tasks/{notdone,done,deferred}/`; `task_template.md` shows the format.
* Each step is numbered `TFNN.N`, matching the file's own `TFNN` (e.g. `TF03.0`, `TF03.1`, ...), starting at `.0` — not a bare `T0N`.
* Every step gets a test where feasible (else record why); every feature gets a dedicated test-writing task.
* Task lists must never include a "regenerate literate docs" task — literate docs are refreshed later, at checkpoint, not as part of a feature's task list.
* Last task done → move the task file to `done/`, set the feature's Done/Tests Written/Test Passing to yes, move the feature file to `done/`.

# issues
* `05-issues/{open,closed,deferred}/`, numbered, follow the issue_template.
* New → `open/`; resolved or absorbed into a feature/task → `closed/`; explicitly deferred → `deferred/`.

# writing .md files
* Applies to `03-features/`, `04-tasks/`, `05-issues/`, and any hand-written
  doc — not `01-literate/` (own prompt in `literate.md`). Applies every time
  a file is rewritten, not just on first authoring.
* Default to bullets. Use a prose sentence only when a genuine narrative
  link between clauses can't be expressed as a list.
* One idea per bullet — split a multi-clause bullet into two rather than
  joining with "and"/"which".
* **Bold** for key decisions/terms; *italics* for emphasis or naming a
  pattern. Headed subsections over one long block.
* Be brief — summarize, don't enumerate every file/field/variable.

# agent model selection
* Default subagent dispatch to haiku; upgrade only when the task needs judgment, not just data-gathering.
* **haiku** — file/log discovery, "where is X defined", dependency-closure scans, counting, formatting. Use the `explorer` agent (`.claude/agents/explorer.md`).
* **sonnet** — analysis, code review, writing, moderate reasoning, synthesis across subagent findings. Use the `reviewer` agent (`.claude/agents/reviewer.md`).
* **opus** — architecture decisions, novel debugging, cross-cutting design tradeoffs. Use the `architect` agent (`.claude/agents/architect.md`).

# bootstrap
* `.claude/bootstrap.md` is the scaffold spec. Run `/bootstrap` to bootstrap a new project — don't follow it ad hoc from a mention in conversation.

# github
* Literate docs: apply `.claude/literate.md`'s prompt to each changed Python module, save as `01-literate/<module>.md`.
* Run tests and regenerate literate docs before committing/pushing.
* Commit or push only when asked, with a good message.
