# Get Shit Done (GSD) -- Deep Research Insights

**Repo:** https://github.com/gsd-build/get-shit-done
**Stars:** ~19.6k | **License:** MIT | **Commits:** 881+
**Tagline:** "A light-weight and powerful meta-prompting, context engineering and spec-driven development system for Claude Code and OpenCode."

---

## 1. What Problem Does GSD Solve?

### The Core Problem: Context Rot

GSD's central thesis is that AI coding quality degrades as context windows fill up. They call this
"context rot" -- the phenomenon where Claude (or any LLM) produces increasingly worse output as
its context window approaches capacity. This manifests as:

- Hallucinated file paths and APIs
- Forgotten requirements from earlier in the conversation
- Repetitive or contradictory code
- Loss of architectural coherence across files
- Subtle bugs introduced by the model losing track of state

### The Solution: Structured Context Engineering

Rather than letting developers "vibecode" (ad-hoc prompting that fills context with noise), GSD
provides a **spec-driven development system** that:

1. **Decomposes work into small, focused tasks** that each fit within ~50% of a context window
2. **Spawns fresh sub-agents** for each task, ensuring peak quality on every execution
3. **Maintains persistent state** in markdown files that bridge sessions and context resets
4. **Orchestrates multi-agent workflows** with thin coordinators and specialized workers

The key insight: **many small context windows >> one large context window**.

---

## 2. Architecture Overview

### Directory Structure

```
.planning/                        # All GSD state lives here
  config.json                     # Workflow configuration
  PROJECT.md                      # Project identity and constraints
  REQUIREMENTS.md                 # Scoped requirements (validated/active/out-of-scope)
  ROADMAP.md                      # Phase-based execution plan
  STATE.md                        # Session memory (< 100 lines, always current)
  codebase/                       # Codebase analysis documents
    STACK.md, ARCHITECTURE.md, CONVENTIONS.md, etc.
  research/                       # Domain research outputs
    RESEARCH.md, STACK.md, FEATURES.md, PITFALLS.md
  phases/
    {phase-name}/
      {phase}-CONTEXT.md          # User decisions for this phase
      {phase}-{NN}-PLAN.md        # Executable task plans (XML-structured)
      {phase}-{NN}-SUMMARY.md     # Post-execution results
      {phase}-RESEARCH.md         # Phase-specific research
      {phase}-VERIFICATION.md     # Verification results
  debug/                          # Active debug sessions
    resolved/                     # Archived debug sessions
  quick/                          # Ad-hoc task plans (outside milestones)
```

### Agent Architecture (11 Specialized Agents)

| Agent | Role | When Spawned |
|-------|------|--------------|
| gsd-project-researcher | Domain research during project init | `/gsd:new-project` |
| gsd-phase-researcher | Phase-specific technical research | `/gsd:plan-phase` |
| gsd-research-synthesizer | Consolidates 4 parallel research outputs | After research phase |
| gsd-roadmapper | Creates phased execution roadmap | `/gsd:new-project` |
| gsd-planner | Generates executable PLAN.md files | `/gsd:plan-phase` |
| gsd-plan-checker | Validates plans across 8 dimensions | After planning |
| gsd-executor | Runs plans with atomic commits | `/gsd:execute-phase` |
| gsd-verifier | Confirms goal achievement (not just task completion) | `/gsd:verify-work` |
| gsd-debugger | Scientific debugging methodology | `/gsd:debug` |
| gsd-codebase-mapper | Analyzes existing codebases | `/gsd:map-codebase` |
| gsd-integration-checker | Validates cross-component wiring | During verification |

### Command System (32 Slash Commands)

All commands are markdown files that define:
- Available tools for the agent
- Context files to load
- Workflow gates to preserve
- Operational constraints

Key commands follow a lifecycle: `new-project` -> `discuss-phase` -> `plan-phase` -> `execute-phase` -> `verify-work` -> `complete-milestone`

---

## 3. How GSD Structures Prompts/Instructions for AI Agents

### Pattern 1: Agents as Markdown Files

Every agent is defined in a single `.md` file that serves as a system prompt. These files contain:

- **Identity statement**: What the agent is and its core philosophy
- **Mandatory initial actions**: Files that MUST be read before any work begins
- **Operational constraints**: What the agent cannot do
- **Output format specification**: Exact structure of what the agent produces
- **Decision escalation rules**: When to stop and ask vs. proceed autonomously
- **Quality signals**: What "good" looks like with concrete examples

This is powerful because the entire agent definition is version-controlled, diffable, and
human-readable.

### Pattern 2: Commands as Orchestration Prompts

Each `/gsd:command` is a markdown file that defines:

```
- What tools the orchestrator can use
- What context files to load
- What sub-agents to spawn
- What workflow gates to enforce
- What flags modify behavior
```

The orchestrator itself is a "thin coordinator" that uses ~15% of its token budget, delegating
heavy lifting to sub-agents that each get a fresh 200k-token context window.

### Pattern 3: Plans as Executable Prompts

PLAN.md files ARE the execution prompts -- they are not documents that become prompts. Each task
within a plan has:

```xml
<task id="01" type="auto" wave="1">
  <files>exact/paths/to/create/or/modify.ts</files>
  <action>
    Specific implementation instructions.
    Includes what to AVOID and WHY.
  </action>
  <verify>Automated command that proves completion (must run < 60 seconds)</verify>
  <done>Measurable acceptance criteria (observable state, not "complete")</done>
</task>
```

Quality signals for task definitions:
- `<files>` must have specific paths, not "auth files"
- `<action>` must include anti-patterns to avoid
- `<verify>` must have an automated command (the "Nyquist rule")
- `<done>` must be observable from user perspective, not implementation detail

### Pattern 4: YAML Frontmatter for Machine Routing

Plans use YAML frontmatter that enables automated dependency analysis and parallelization:

```yaml
phase: authentication
plan: 02
wave: 1
depends_on: []
modifies: [src/auth/login.ts, src/auth/middleware.ts]
autonomy: full
```

This metadata allows the execute-phase orchestrator to automatically determine which plans
can run in parallel (same wave, no file conflicts) vs. which must be sequential.

### Pattern 5: Three-Category Decision Locking

The discuss-phase produces CONTEXT.md files that classify decisions into:

1. **Locked Decisions**: Non-negotiable user choices. Research and plan around these.
2. **Claude's Discretion**: Agent can choose the best technical approach.
3. **Deferred Ideas**: Explicitly out of scope. Do not explore.

This prevents agents from second-guessing user decisions, exploring tangents, or scope-creeping.

---

## 4. Context Management Patterns

### The 50% Rule

Plans target ~50% of the context window -- not 80%. This is based on the observation that LLM
quality degrades well before the window is technically full. Typical plan size: 2-3 tasks,
5-8 files modified.

### Tiered Context Loading

Rather than dumping everything into context, GSD loads files strategically:

1. **Always loaded**: STATE.md (< 100 lines), config.json
2. **Loaded per-phase**: CONTEXT.md, RESEARCH.md, relevant PLAN.md
3. **Loaded on-demand**: PROJECT.md, REQUIREMENTS.md, ROADMAP.md
4. **Never loaded wholesale**: Previous summaries (loaded via digest index, then selective reads)

### The Digest Index Pattern

For historical context (previous phase summaries), GSD uses a two-step approach:
1. Generate a digest index of all summaries (titles + one-liners)
2. Selectively load 2-4 full summaries that are actually relevant

This prevents the common failure mode of loading ALL historical context and blowing the budget.

### STATE.md: The Bridge File

STATE.md is the most critical context management artifact. It is:
- **Always under 100 lines** (strict limit)
- **Updated after every plan completion and phase transition**
- **The first file loaded in any session**
- Contains: current position, recent decisions (3-5), active blockers, session continuity info
- References fuller details elsewhere rather than reproducing them

### Fresh Context Per Sub-Agent

Each sub-agent (executor, researcher, verifier) gets a completely fresh 200k token context
window. The orchestrator passes only the specific files needed for that agent's task.
This is the primary mechanism for defeating context rot.

---

## 5. Task Orchestration and Planning

### Wave-Based Parallel Execution

GSD's execution model groups tasks into dependency-ordered waves:

```
Wave 0: Test infrastructure scaffolding (if needed)
Wave 1: Independent tasks (run in parallel)
Wave 2: Tasks depending on Wave 1 (run in parallel within wave)
Wave 3: Tasks depending on Wave 2
...
```

Multiple plans in the same wave execute simultaneously if they don't modify the same files.
Up to 3 concurrent agents by default (configurable).

### The Planning Pipeline

```
User Request
    |
    v
[Discuss Phase] --> CONTEXT.md (locked decisions)
    |
    v
[Research Phase] --> RESEARCH.md (prescriptive findings)
    |
    v
[Plan Phase] --> PLAN.md files (executable task specs)
    |
    v
[Plan Checker] --> 8-dimension validation
    |                (iterates until pass or max iterations)
    v
[Execute Phase] --> SUMMARY.md + atomic git commits
    |
    v
[Verify Phase] --> VERIFICATION.md + gap analysis
    |
    v
(if gaps) --> [Gap Closure Plans] --> re-execute --> re-verify
```

### 8-Dimension Plan Validation

Before any code is written, the plan-checker validates:

1. **Requirement Coverage**: Every requirement maps to at least one task
2. **Task Completeness**: All tasks have files, action, verify, done fields
3. **Dependency Correctness**: DAG is acyclic, no forward references
4. **Key Links Planned**: Artifacts are wired together, not isolated
5. **Scope Sanity**: 2-3 tasks per plan, 5-8 files (quality degrades past 5 tasks)
6. **Verification Derivation**: Must-haves are user-observable, not implementation details
7. **Context Compliance**: Honors locked decisions, excludes deferred ideas
8. **Nyquist Compliance**: Every task has automated verification

### Automatic Deviation Rules (During Execution)

The executor has 4 escalating rules for handling unexpected issues:

| Rule | Trigger | Action |
|------|---------|--------|
| 1 | Broken code, logic/type errors | Auto-fix and continue |
| 2 | Missing error handling, validation, auth | Add and continue |
| 3 | Missing deps, broken imports, DB errors | Fix and continue |
| 4 | New tables, major schema changes | STOP and checkpoint |

After 3 failed attempts per task, document and move forward. Pre-existing issues go to
`deferred-items.md`.

### Verification: Goal Achievement != Task Completion

The verifier distinguishes three levels:

1. **Existence**: File is present
2. **Substantive**: Content exceeds stub thresholds (not just `// TODO`)
3. **Wired**: Imported and actively used by other components

All three must pass. The verifier specifically checks "key links" -- the wiring between
components -- because "80% of stubs hide here."

Stub detection scans for: TODO/FIXME comments, empty returns, console.log-only handlers,
fetch calls without response handling, state defined but never rendered.

---

## 6. What Makes GSD Gain Traction

### Simplicity of Entry

```bash
npx get-shit-done-cc@latest
```

One command installs everything. No complex setup, no config files to create manually.

### The `/gsd:quick` Escape Hatch

For developers who don't want the full ceremony, `/gsd:quick` provides:
- Atomic commits and state tracking
- Skips research, plan-checking, and verification
- Ideal for bug fixes and small features
- Optional `--full` flag adds quality checks back

This is critical for adoption -- users don't feel locked into the heavy workflow.

### Multi-Runtime Support

Works with Claude Code, OpenCode, Gemini CLI, and Codex. Not locked to one provider.

### Cost-Conscious Model Profiles

| Profile | Planning | Execution | Verification |
|---------|----------|-----------|-------------|
| Quality | Opus | Opus | Opus |
| Balanced | Opus | Sonnet | Sonnet |
| Budget | Sonnet | Sonnet | Haiku |

Users control cost-quality tradeoffs without changing workflows.

### Configurable Workflow Gates

Everything can be toggled:
- Research before planning (on/off)
- Plan verification (on/off)
- Post-execution verification (on/off)
- Auto-advance between phases (on/off)
- Interactive vs. "yolo" mode

### Clean Git History

Every task produces an atomic commit with conventional format:
`{type}({phase}-{plan}): {description}`

This makes the AI's work reviewable and revertable at a granular level.

### Session Continuity

`/gsd:resume-work` restores full context from any previous session. STATE.md bridges
the gap between sessions, and specific resume files capture exact continuation points.

---

## 7. Key Architectural Decisions

### 1. Everything is Markdown

All agents, commands, workflows, templates, plans, state -- everything is markdown. This means:
- Version controlled and diffable
- Human readable and editable
- No runtime dependencies for the core logic
- The "code" IS the prompts

### 2. Thin Orchestrators, Fat Workers

Orchestrators use ~15% of token budget. Workers (executors, researchers, planners) get the
remaining context for their specific task. This prevents the orchestrator from becoming a
bottleneck.

### 3. File-Based State Management

No databases, no APIs for state. Everything is `.planning/` directory files:
- STATE.md for session memory
- PLAN.md for task definitions
- SUMMARY.md for execution results
- VERIFICATION.md for quality reports

This makes the system completely portable and inspectable.

### 4. Plans are Prompts (Not Documents)

PLAN.md files are not documentation that later gets translated into prompts. They ARE the
prompts that the executor agent receives. This eliminates a lossy translation layer.

### 5. Prescriptive Over Exploratory

Research agents make prescriptive claims ("Use X") not exploratory ones ("Consider X or Y").
This reduces decision fatigue downstream and prevents the planner from needing to make
technology choices.

### 6. Interface-First Task Ordering

When plans create types/interfaces consumed downstream:
1. Task 0: Write interface definitions (types, exports, no implementation)
2. Middle tasks: Implement against contracts
3. Final task: Wire implementations to consumers

This prevents the "scavenger hunt" anti-pattern.

### 7. Goal-Backward Methodology

Planning works backward from desired outcomes:
1. Define observable truths (user-perspective behaviors)
2. Derive required artifacts (files that must exist)
3. Identify required wiring (connections between artifacts)
4. Find key links (critical failure points)

---

## 8. Complex Multi-Step Workflow Handling

### The Full Lifecycle

```
/gsd:new-project
  Questions -> 4 parallel researchers -> synthesizer -> requirements -> roadmap

/gsd:discuss-phase N
  Gray area identification -> multi-select -> deep-dive dialogue -> CONTEXT.md

/gsd:plan-phase N
  Research (optional) -> plan generation -> 8-dim validation (iterative) -> PLAN.md files

/gsd:execute-phase N
  Dependency analysis -> wave grouping -> parallel sub-agent execution ->
  per-task atomic commits -> SUMMARY.md -> state updates

/gsd:verify-work N
  Artifact existence -> substantiveness -> wiring checks ->
  key link verification -> gap analysis -> VERIFICATION.md

(if gaps exist)
/gsd:plan-phase N --gaps
  Parse gaps -> group by artifact -> generate fix plans -> re-execute -> re-verify

/gsd:complete-milestone
  Archive -> release -> retrospective
```

### Recovery and Resilience

- **Lost progress**: `/gsd:resume-work` or `/gsd:progress`
- **Phase problems**: Git revert commits, then re-plan
- **Scope changes**: `/gsd:add-phase`, `/gsd:insert-phase`, `/gsd:remove-phase`
- **Debugging**: `/gsd:debug` for scientific hypothesis-driven investigation
- **Cost control**: Switch model profiles or disable optional agents

### Checkpoint System

Three checkpoint types enable human-in-the-loop control:

| Type | Frequency | Purpose |
|------|-----------|---------|
| `checkpoint:human-verify` | 90% | User confirms automated work visually |
| `checkpoint:decision` | 9% | User selects between implementation options |
| `checkpoint:human-action` | 1% | Truly manual steps (2FA, email verification) |

In "yolo" mode, human-verify and decision checkpoints auto-approve. Human-action always stops.

---

## 9. Actionable Insights for the Databricks REPL Skill

Based on GSD's patterns, here are concrete recommendations for building a Claude Code skill
that executes Python on Databricks clusters:

### 9.1 Apply the "Plans are Prompts" Pattern

Structure the REPL skill's execution as self-contained task specifications:

```xml
<databricks-task id="01" type="execute">
  <cluster>cluster-id-or-name</cluster>
  <code>python code to execute</code>
  <verify>Expected output pattern or assertion</verify>
  <done>Observable result (dataframe shape, file created, etc.)</done>
</databricks-task>
```

This makes each execution step inspectable and replayable.

### 9.2 Adopt Context Budget Discipline

For multi-step Databricks workflows (ETL pipelines, ML training), apply the 50% rule:
- Each execution step should be self-contained
- Pass only relevant schema/output info between steps (not full dataframes)
- Use a STATE.md-like file to track pipeline progress across steps

### 9.3 Implement Automatic Deviation Rules

When Databricks execution fails, apply escalating rules:

| Rule | Trigger | Action |
|------|---------|--------|
| 1 | Syntax errors, import failures | Auto-fix and re-execute |
| 2 | Missing library, wrong cluster config | Install/reconfigure and retry |
| 3 | Permission/auth errors | Stop and ask user (checkpoint) |
| 4 | Schema changes, data loss risk | Stop and explain before proceeding |

### 9.4 Use the Thin Orchestrator Pattern

The main skill command should be a lightweight coordinator that:
- Validates the user's intent
- Determines which cluster to use
- Spawns execution with minimal context overhead
- Captures results and updates state
- Never holds the full output in its own context

### 9.5 Build Session Continuity

For long-running Databricks workflows:
- Track execution history in a state file
- Record which cells/steps succeeded
- Enable resume from last successful step
- Maintain variable/schema context across steps without re-executing everything

### 9.6 Implement Verification at Three Levels

After Databricks execution:
1. **Existence**: Output/table was created
2. **Substantive**: Output has expected schema and non-zero rows
3. **Wired**: Output is accessible by downstream consumers (other notebooks, dashboards)

### 9.7 Provide a "Quick" Mode

Not every Databricks interaction needs full ceremony:
- Quick mode: Execute code, show results, done
- Full mode: Plan pipeline, execute steps, verify outputs, track state
- Let users choose based on task complexity

### 9.8 Apply Prescriptive Research Patterns

When the skill needs to understand cluster state, schemas, or available libraries:
- Check cluster status and capabilities first
- Be prescriptive: "Using cluster X because it has the required libraries"
- Don't present options: "Should we use cluster A or B?" (unless genuinely ambiguous)

### 9.9 Atomic Execution with Clean State

Each code execution on Databricks should:
- Be independently verifiable
- Produce a clear success/failure signal
- Not leave partial state on failure (or clean up explicitly)
- Record what was executed and what was produced

### 9.10 Markdown-Based Configuration

Following GSD's "everything is markdown" philosophy:
- Skill configuration in a readable format
- Cluster profiles as named configurations
- Execution templates for common patterns (read table, write table, run query, train model)
- All inspectable and version-controllable by the user

---

## 10. Summary of Key Takeaways

| GSD Pattern | Core Insight | Applicability |
|-------------|-------------|---------------|
| Context rot prevention | Many small contexts >> one large context | Universal |
| Plans as prompts | Task specs ARE execution instructions | High |
| 50% context budget | Quality degrades before window fills | Universal |
| Thin orchestrators | Coordinators delegate, workers do | High |
| 8-dim validation | Validate plans before execution | Medium |
| Wave-based parallelism | Dependency-ordered concurrent execution | Medium |
| Atomic commits per task | Granular, reviewable, revertable work | High |
| 3-level verification | Existence + Substance + Wiring | High |
| Deviation escalation | Auto-fix small issues, stop for big ones | High |
| Decision locking | Locked / Discretion / Deferred categories | Medium |
| STATE.md bridge | < 100 lines, always current, first-loaded | High |
| Quick escape hatch | Full ceremony not always needed | Critical |
| Everything is markdown | Version controlled, human readable, portable | High |
| Prescriptive research | "Use X" not "Consider X or Y" | High |
| Goal-backward planning | Start from observable outcomes, work backward | Medium |

The fundamental lesson from GSD's success: **structure the AI's work the same way you'd
structure a junior developer's work** -- clear specs, small tasks, verification at every
step, and clean handoffs between phases. The AI is the builder; the system is the foreman.
