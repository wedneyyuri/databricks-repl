# Aplicando a Skill de Copywriting ao README do databricks-repl

## Fase 1: "Before Writing" — Diagnóstico com o Framework da Skill

A skill de copywriting exige que se responda 4 perguntas antes de escrever qualquer linha. Vamos aplicá-las ao README.

### 1. Page Purpose
- **Tipo de página**: Homepage (README = landing page do projeto no GitHub)
- **Ação primária**: Instalar o plugin (`claude plugin add wedneyyuri/databricks-repl`)

### 2. Audience
- **Cliente ideal**: Desenvolvedores e data engineers que já usam Databricks e AI coding agents (Claude Code, Cursor, Copilot)
- **O que já sabem**: Conhecem Genie, usam Databricks diariamente, entendem o ecossistema. Não precisam ser convencidos sobre Databricks — precisam ser convencidos de que existe algo melhor que Genie para o workflow deles com AI agents.
- **Problema que tentam resolver**: Genie funciona num contexto simples (notebook, workspace). Mas quando o trabalho real exige cruzar fontes de dados, validar hipóteses em paralelo, interagir com APIs externas, ou compor múltiplas ferramentas — Genie não chega lá.
- **Objeções/hesitações**: "Genie já faz isso" (resposta: não faz — Genie é single-context), "Isso é só um wrapper?" (resposta: não — é uma porta de entrada para o poder de orquestração completo do AI agent)
- **Linguagem do cliente**: "Rodar no cluster", "pipeline de dados", "validar hipótese", "paralelizar análises", "workflow end-to-end"

### 3. Product/Offer
- **O que vende**: Databricks como mais uma capacidade dentro do poder de orquestração completo do AI agent
- **Diferencial vs. Genie**: Genie = assistente single-context dentro do workspace Databricks. databricks-repl = Databricks como um dos muitos recursos que o agente orquestra. O agente pode usar GSD, superpowers, outras skills, criar subagents, explorar código em várias linguagens, interagir com MCPs, validar múltiplas hipóteses em paralelo — e Databricks é só uma das peças.
- **Transformação/outcome**: "Genie te dá um assistente dentro do Databricks. Isso te dá Databricks dentro de um orquestrador que faz tudo."
- **Proof points**: Exemplos reais (primes, monte-carlo, iris-classification), composição com skills (GSD, superpowers), padrão RLM, compatibilidade com 35+ agents

### 4. Context
- **De onde vem o tráfego**: GitHub search, links em comunidades de AI coding (Twitter/X, Discord, Reddit), referências de outros repos (superpowers, get-shit-done)
- **O que o visitante já sabe**: Já usa Databricks. Já conhece Genie. Provavelmente já usa Claude Code ou Cursor. O README não precisa explicar o que é Databricks ou o que Genie faz — precisa mostrar o que Genie **não** faz e o que se ganha com a abordagem de orquestração.

---

## Fase 2: Diagnóstico do README Atual vs. Princípios da Skill

### Princípio: "Clarity Over Cleverness"

| Trecho Atual | Problema | Princípio Violado |
|---|---|---|
| "Recursive Language Model (RLM) pattern" | Jargão acadêmico — o visitante não conhece RLM | Customer Language > Company Language |
| "JSON metadata + file paths" | Detalhe de implementação, não benefício | Benefits > Features |
| "Append-only execution" | Termo técnico sem contexto | Specificity > Vagueness |
| "eviction recovery" | O visitante não sabe o que é eviction sem contexto | Customer Language |
| "Root LM / Sub-LMs" | Conceito de paper acadêmico | Clarity > Cleverness |

### Princípio: "Benefits Over Features"

| Feature Atual (o que faz) | Benefício que falta (o que significa) |
|---|---|
| "Scripts return JSON metadata + file paths" | "Sessões 3x mais longas sem degradação — seu agente não fica 'burro' no meio da análise" |
| "Append-only session log" | "Retome de onde parou, mesmo se o cluster cair" |
| "sub_llm() / sub_llm_batch()" | "Processe 10.000 registros com LLM sem consumir o contexto do agente principal" |
| "Session consolidation" | "Quando terminar, ganhe um .py limpo pronto pra commit — sem copiar/colar de notebooks" |

### Princípio: "Specificity Over Vagueness"

| Vago | Específico |
|---|---|
| "keeping your agent's context window clean" | "Sessions stay productive for 50+ interactions — no compaction needed" |
| "Cross-project context" | "Read a CSV from your desktop, run a Spark job, compare with a local model, commit to git — one session" |
| "Full ecosystem" | "Combine with other skills, MCP servers, and shell tools in the same conversation" |

### Princípio: "One Idea Per Section"

O README atual viola isso em "Why This Approach?" — essa seção tenta explicar context management, comparar com MCP/SDK, E introduzir o padrão RLM, tudo de uma vez.

---

## Fase 3: Aplicando o "Page Structure Framework"

### Above the Fold — Headline

**Fórmulas da skill:**

1. `{Achieve outcome} without {pain point}`
2. `The {category} for {audience}`
3. `Never {unpleasant event} again`
4. `{Question highlighting main pain point}`

**Opções geradas (revisadas para público que já conhece Genie):**

| Fórmula | Headline | Rationale |
|---|---|---|
| 1 | "Databricks inside your AI agent's full orchestration power" | Posiciona Databricks como peça de algo maior. O "algo maior" é o gancho. |
| 1 | "Genie gives you AI inside Databricks. This gives you Databricks inside AI." | Inversão direta. Memorável. Posiciona sem atacar. |
| 3 | "Everything Genie does — plus everything outside Databricks" | Reconhece Genie, expande o escopo. |
| 4 | "What if your AI agent could use Databricks, local files, APIs, and other tools — all at once?" | Pergunta retórica que pinta o cenário completo de orquestração. |

**Recomendação**: Opção 2 como headline (inversão direta, posiciona imediatamente), Opção 1 como subheadline (expande sobre o poder de orquestração).

### Above the Fold — Subheadline

A skill diz: "Expands on headline. Adds specificity. 1-2 sentences max."

**Proposta**: "Run code on Databricks clusters while your agent orchestrates everything else — other skills, subagents, MCPs, local files, and parallel hypothesis validation. One session, no boundaries."

**Rationale**: Para quem já conhece Genie, "handles auth, sessions, output capture" é feature de infraestrutura (boring). O que excita é o que eles **não podem fazer hoje**: orquestração completa com paralelização, subagents, composição de skills.

### Above the Fold — Primary CTA

A skill diz: Formula = `[Action Verb] + [What They Get] + [Qualifier if needed]`

**Proposta**: "Add Databricks to your agent" (acima do code block).

```
claude plugin add wedneyyuri/databricks-repl
```

"Works with Claude Code, Cursor, GitHub Copilot, and [35+ other agents](https://agentskills.io)."

**Rationale**: "Add Databricks to your agent" é customer language. Não é "install a plugin" (mecanismo). É o que o dev quer fazer (outcome).

### Core Sections — Revisado para Público que Conhece Genie

| Seção da Skill | Recomendação Revisada |
|---|---|
| **Problem/Pain** | **"Genie is single-context"** — Genie trabalha num notebook, num workspace. Quando o trabalho real exige cruzar fontes, paralelizar análises, compor ferramentas — ele não chega lá. Essa é a dor. Não precisa ser sutil. |
| **Solution/Benefits** | **"Full orchestration"** — Paralelizar hipóteses, criar subagents, explorar código em várias linguagens, interagir com MCPs, compor com GSD/superpowers/outras skills. Databricks é uma peça, não o todo. |
| **How It Works** | Manter simples (3 steps). O público técnico entende rápido. |
| **Social Proof** | Composição com ecossistema: "Works with GSD, superpowers, and any skill that follows the Agent Skills Spec" |
| **Objection Handling** | Agora é **a seção principal**, não objeção. A comparação com Genie é o gancho de posicionamento. Deve ser a 2ª ou 3ª seção. |
| **Final CTA** | "Start orchestrating" — recap do poder de orquestração |

---

## Fase 4: Reescrita Concreta do README

Aplicando todos os princípios, aqui está a estrutura proposta:

```markdown
# databricks-repl

Genie gives you AI inside Databricks. This gives you Databricks inside AI.

Run code on Databricks clusters while your agent orchestrates
everything else — other skills, subagents, MCPs, local files, and
parallel hypothesis validation. One session, no boundaries.

Works with Claude Code, Cursor, GitHub Copilot, and
[35+ other agents](https://agentskills.io).

## Add Databricks to Your Agent

‎```bash
claude plugin add wedneyyuri/databricks-repl
‎```

## Genie vs. Full Orchestration

Genie works inside one notebook, one workspace. When the real work
crosses boundaries, it stops. Your AI agent doesn't.

| What you need | Genie | Your agent + this skill |
|---------------|-------|------------------------|
| Analyze a repo and cross-reference with Databricks logs | Workspace only | Reads repo + queries cluster in one session |
| Validate 3 hypotheses in parallel on different datasets | One notebook at a time | Spawns subagents, each running its own cluster query |
| Train on cluster, compare with local baselines, commit results | Can't access local files or git | Cluster compute + local files + git — same session |
| Use an MCP to enrich data before running Spark | No MCP support | Calls MCPs, APIs, other skills, then sends to cluster |
| Explore Python + Scala + SQL across multiple repos | Single-language notebooks | Subagents explore each language, agent synthesizes |
| Resume after cluster eviction | Start over | Append-only session log with replay |

The difference isn't features. It's architecture. Genie is an
assistant scoped to Databricks. This makes Databricks one resource
inside an orchestrator that can do **anything** — use
[GSD](https://github.com/coreyhaines31/get-shit-done),
[superpowers](https://github.com/coreyhaines31/superpowers),
compose skills, spawn subagents, interact with MCPs, and
parallelize work across tools.

## What It Looks Like

‎```
You: "Load the customers table, train a classifier,
      compare with last quarter's local baseline,
      and open a PR with the results"

Claude:
→ creates a REPL session on your Databricks cluster
→ runs the training code, captures outputs as files
→ reads your local baseline for comparison
→ consolidates everything into a clean .py file
→ commits and opens the PR
‎```

Five tools, one session. No switching between terminal,
notebooks, and browser.

## How It Works

1. **You describe the task** — your agent decides what to run
2. **Scripts handle the plumbing** — auth, sessions, polling, output capture
3. **Agent sees only metadata** — file paths and status, never raw output

Context stays clean. Sessions stay productive for 50+ interactions.

## Examples

| Example | What It Shows |
|---------|---------------|
| [primes](examples/primes/) | Basic Python execution on a Databricks cluster |
| [monte-carlo-pi](examples/monte-carlo-pi/) | Distributed Spark — estimate π scaling from 100M to 10B samples |
| [iris-classification](examples/iris-classification/) | Full ML pipeline — load, train, evaluate, persist model to Volumes |

## Skills

| Skill | What It Does |
|-------|--------------|
| [databricks-repl](skills/databricks-repl/) | Execute Python on Databricks via a stateful REPL session |
| [databricks-repl-consolidate](skills/databricks-repl-consolidate/) | Turn a REPL session into a single committable .py file |

## Prerequisites

- [Databricks CLI](https://docs.databricks.com/dev-tools/cli/install.html)
  with a profile in `~/.databrickscfg`
- [Databricks SDK for Python](https://docs.databricks.com/dev-tools/sdk-python.html)
  (`pip install databricks-sdk`)
- A running classic all-purpose cluster

## Using with Other Agents

These skills follow the
[Agent Skills Specification](https://agentskills.io/specification).
Copy `skills/` to wherever your agent reads SKILL.md files.

### Cursor

‎```bash
cp -r skills/databricks-repl .cursor/skills/
cp -r skills/databricks-repl-consolidate .cursor/skills/
‎```

### GitHub Copilot

‎```bash
mkdir -p .github/skills
cp -r skills/databricks-repl .github/skills/
cp -r skills/databricks-repl-consolidate .github/skills/
‎```

## Start Orchestrating

Databricks is powerful. But Databricks inside an AI agent that
can parallelize work, compose tools, and cross every boundary?
That's something else.

‎```bash
claude plugin add wedneyyuri/databricks-repl
‎```

## License

[MIT](LICENSE)
```

---

## Fase 5: Anotações — Por Que Cada Mudança Foi Feita

### Headline: Inversão como posicionamento

**Antes**: "Run Python on Databricks clusters from your AI coding agent"
**Depois**: "Genie gives you AI inside Databricks. This gives you Databricks inside AI."

**Princípio aplicado**: Analogia (Best Practices da skill: "Use Analogies When Helpful") + Be Direct. A inversão comunica o posicionamento inteiro em uma frase. Para quem já conhece Genie (o público-alvo), isso clica imediatamente — não precisa de explicação.

### Subheadline: Orquestração como promessa

**Antes**: Lista features (auth, sessions, output capture, eviction recovery)
**Depois**: "Run code on Databricks clusters while your agent orchestrates everything else — other skills, subagents, MCPs, local files, and parallel hypothesis validation."

**Princípio aplicado**: Benefits > Features. O público já sabe que precisa de auth e sessions. O que não sabe (e é o gancho) é que o agente pode **orquestrar tudo junto** — skills, subagents, MCPs, paralelização. Isso é o "uau" que faz o cientista de dados ficar doido.

### CTA: "Add Databricks to Your Agent"

**Antes**: "Installation" (seção 5, linguagem de mecanismo)
**Depois**: "Add Databricks to Your Agent" (seção 2, linguagem de outcome)

**Princípio aplicado**: CTA Formula `[Action Verb] + [What They Get]`. "Add Databricks" é o que o dev quer fazer. "Install a plugin" é como ele faz. A skill diz: foque no que eles ganham.

### "Genie vs. Full Orchestration" como seção central

**Antes**: "How Is This Different from Databricks Genie?" — enterrada no final, tabela de capabilities
**Depois**: "Genie vs. Full Orchestration" — 3ª seção, tabela de cenários reais de orquestração

**Princípio aplicado**: Para público que já conhece Genie, isso não é Objection Handling — é **Problem/Pain** (a seção mais importante do core). A dor é: "Genie não faz X, Y, Z que eu preciso". Os cenários novos mostram paralelização de hipóteses, subagents explorando múltiplas linguagens, composição com MCPs — coisas que Genie não consegue por design. A tabela mudou de capabilities (features) para scenarios que pintam o uso real (benefits).

### Parágrafo de orquestração após a tabela

**Texto**: "The difference isn't features. It's architecture. Genie is an assistant scoped to Databricks. This makes Databricks one resource inside an orchestrator that can do anything — use GSD, superpowers, compose skills, spawn subagents, interact with MCPs, and parallelize work across tools."

**Princípio aplicado**: One Idea Per Section — essa seção tem uma ideia: a diferença é arquitetural, não funcional. + Specificity > Vagueness — nomeia as ferramentas concretas (GSD, superpowers, MCPs) em vez de dizer "extensível".

### "What It Looks Like" em vez de "What It Feels Like"

**Antes**: Exemplo simples (load customers + train classifier)
**Depois**: Exemplo cross-domain (train on cluster + compare with local baseline + open PR)

**Princípio aplicado**: Specificity > Vagueness + Show Over Tell. O exemplo anterior poderia ser feito no Genie. O novo mostra algo que **só** a abordagem de orquestração permite: cluster + local + git + PR em uma sessão.

### Seção "Start Orchestrating" no final

**Antes**: Não existia CTA final
**Depois**: Recap de valor + CTA repetido

**Princípio aplicado**: A skill exige Final CTA com "recap value, repeat CTA, risk reversal". O texto "Databricks is powerful. But Databricks inside an AI agent that can parallelize work, compose tools, and cross every boundary? That's something else." recapitula a promessa central e repete o comando de instalação.

---

## Fase 6: Alternativas para Headline e CTA

A skill pede 2-3 opções com rationale:

### Headlines

| Opção | Copy | Rationale |
|-------|------|-----------|
| A (recomendada) | "Genie gives you AI inside Databricks. This gives you Databricks inside AI." | Inversão direta. Memorável. Posiciona sem atacar. Para público que já conhece Genie, clica imediatamente. |
| B | "Databricks inside your AI agent's full orchestration power" | Mais descritivo, menos memorável. Bom se "inversão" parecer agressivo. |
| C | "Everything Genie does — plus everything outside Databricks" | Reconhece Genie, expande escopo. Tom mais conciliador. |

**Recomendação**: A — a inversão é a forma mais compacta de comunicar o posicionamento. Se parecer agressivo demais para a relação com Databricks, usar C.

### CTAs

| Opção | Copy | Rationale |
|-------|------|-----------|
| A (recomendada) | "Add Databricks to Your Agent" | Customer language. O outcome que o dev quer. |
| B | "Start Orchestrating" (CTA final) | Foca no poder de orquestração. Bom como CTA de fechamento. |
| C | "Install in One Command" | Funcional, remove friction. Bom como texto secundário junto ao code block. |

**Recomendação**: A para CTA principal, B para CTA final (a skill recomenda repetir o CTA no final com variação).

---

*Análise aplicada usando: [marketingskills/copywriting](https://github.com/coreyhaines31/marketingskills) SKILL.md v1.0.0*
*Princípios referenciados: Before Writing framework, Clarity > Cleverness, Benefits > Features, Specificity > Vagueness, Customer Language > Company Language, One Idea Per Section, Page Structure Framework (headline formulas, core sections table, CTA formula), Analogies, Be Direct, Rhetorical Questions, Output Format (annotations + alternatives)*
