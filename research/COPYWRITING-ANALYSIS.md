# Aplicando a Skill de Copywriting ao README do databricks-repl

## Fase 1: "Before Writing" — Diagnóstico com o Framework da Skill

A skill de copywriting exige que se responda 4 perguntas antes de escrever qualquer linha. Vamos aplicá-las ao README.

### 1. Page Purpose
- **Tipo de página**: Homepage (README = landing page do projeto no GitHub)
- **Ação primária**: Instalar o plugin (`claude plugin add wedneyyuri/databricks-repl`)

### 2. Audience
- **Cliente ideal**: Desenvolvedores e data engineers que usam AI coding agents (Claude Code, Cursor, Copilot) e trabalham com Databricks
- **Problema que tentam resolver**: Não conseguem usar Databricks de forma fluida dentro do fluxo do AI agent — precisam alternar entre terminal, notebooks Databricks, e IDE
- **Objeções/hesitações**: "Já tenho o Genie, pra que preciso disso?" / "Isso é só um wrapper de API?" / "Vai poluir meu contexto?"
- **Linguagem do cliente**: "Análise de dados", "rodar no cluster", "perdi o contexto", "sessão caiu", "pipeline de dados"

### 3. Product/Offer
- **O que vende**: Skill que permite AI agents executar Python em clusters Databricks com gerenciamento limpo de contexto
- **Diferencial vs. alternativas**: Cross-domain orchestration (único que cruza Databricks + local + APIs numa sessão), contexto limpo (metadata-only), session continuity com eviction recovery
- **Transformação/outcome**: "Seu AI agent vira orquestrador de dados: lê local, executa no cluster, compara resultados, commita — tudo numa sessão"
- **Proof points**: Exemplos reais (primes, monte-carlo, iris-classification), padrão RLM publicado, compatibilidade com 35+ agents

### 4. Context
- **De onde vem o tráfego**: GitHub search, links em comunidades de AI coding (Twitter/X, Discord, Reddit), referências de outros repos (superpowers, get-shit-done)
- **O que o visitante já sabe**: Provavelmente já usa Claude Code ou Cursor, pode já conhecer Databricks, mas não necessariamente entende o problema de context management

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

**Opções geradas:**

| Fórmula | Headline | Rationale |
|---|---|---|
| 1 | "Use Databricks from your AI agent — without losing context" | Outcome claro + dor real (perda de contexto) |
| 1 | "Run Spark jobs from Claude Code — without auth boilerplate or context bloat" | Mais específico, dois pain points |
| 2 | "The Databricks skill for AI coding agents" | Simples, categoriza imediatamente |
| 3 | "Never switch between your terminal and Databricks notebooks again" | Emocional, foca na frustração do fluxo quebrado |
| 4 | "Why can't your AI agent use Databricks and local files in the same session?" | Provoca, destaca a limitação do Genie |

**Recomendação**: Opção 1 como headline, Opção 2 como subheadline.

### Above the Fold — Subheadline

A skill diz: "Expands on headline. Adds specificity. 1-2 sentences max."

**Atual**: "Run Python on Databricks clusters from your AI coding agent. Just describe what you want — the skill handles auth, sessions, output capture, and eviction recovery."

**Proposta**: "Describe what you want. The skill creates a session on your cluster, executes the code, and returns clean metadata — no tokens wasted on auth, polling, or raw output."

**Rationale**: Remove "eviction recovery" (jargão sem contexto), mantém a promessa de simplicidade, adiciona especificidade sobre o que é economizado.

### Above the Fold — Primary CTA

A skill diz: Formula = `[Action Verb] + [What They Get] + [Qualifier if needed]`

**Atual**: Nenhum CTA explícito above the fold. A instalação está na seção "Installation" lá embaixo.

**Proposta**: Trazer o CTA para logo após a subheadline:

```
claude plugin add wedneyyuri/databricks-repl
```

Com texto: "Install in one command — works with Claude Code, Cursor, Copilot, and [35+ agents](https://agentskills.io)."

### Core Sections — Aplicando a tabela da skill

| Seção da Skill | Mapeamento no README | Status Atual | Recomendação |
|---|---|---|---|
| **Social Proof** | "Works with 35+ agents" (uma linha) | Fraco — enterrado, sem números de uso | Mover para above the fold, adicionar agent logos se possível |
| **Problem/Pain** | "Why This Approach?" (técnico demais) | Existe mas fala para engenheiros, não para o público | Reescrever como "The Problem" com linguagem do cliente |
| **Solution/Benefits** | "What It Feels Like" + "How It Works" | Bom conteúdo, mas mistura features com benefits | Separar: uma seção de benefícios, outra de "how it works" |
| **How It Works** | "How It Works" (5 steps) | Sólido, claro | Manter, talvez simplificar para 3 steps |
| **Objection Handling** | "How Is This Different from Databricks Genie?" | Bom conteúdo, mas enterrado no final | **Mover para cima** — é a objeção #1 |
| **Final CTA** | Não existe | Ausente | Adicionar seção final com CTA + recap de valor |

---

## Fase 4: Reescrita Concreta do README

Aplicando todos os princípios, aqui está a estrutura proposta:

```markdown
# databricks-repl

Use Databricks from your AI agent — without losing context.

Describe what you want. The skill creates a session on your cluster,
executes your code, and returns clean metadata — no tokens wasted
on auth, polling, or raw output.

Works with Claude Code, Cursor, GitHub Copilot, and
[35+ other agents](https://agentskills.io).

## Install

‎```bash
claude plugin add wedneyyuri/databricks-repl
‎```

## What You Can Do

‎```
You: "Load the customers table and train a classifier"

Claude:
→ creates a REPL session on your cluster
→ executes the code, returns structured metadata
→ reads output selectively (only what matters enters context)
→ iterates until done, then produces a clean .py file
‎```

Read a local CSV, run a Spark job on Databricks, compare results
with a local model, commit the output to git — all in one session.

## Why Not Just Use Genie?

Genie is great inside Databricks notebooks. But it can't cross boundaries.

| Scenario | Genie | This skill |
|----------|-------|------------|
| Analyze a repo and cross-reference with Databricks logs | Can't read local repos | One session: reads repo + queries cluster |
| Train on cluster, compare with local baselines | Workspace only | Local files + cluster compute + local comparison |
| Build a pipeline and commit the code | No git integration | Executes, validates, consolidates, commits |
| Resume after connection loss | Start over | Append-only log with replay |

The key: **your AI agent becomes the orchestrator**. Genie is scoped
to Databricks. This skill lets your agent work across everything.

## How It Works

1. **You describe the task** — your agent decides what code to run
2. **Scripts handle the plumbing** — auth, sessions, polling, output capture
3. **The agent sees only metadata** — file paths and status, never raw output

That's it. Your agent's context stays clean, so sessions stay
productive for 50+ interactions without compaction.

## Examples

| Example | What It Shows |
|---------|---------------|
| [primes](examples/primes/) | Basic Python execution on a Databricks cluster |
| [monte-carlo-pi](examples/monte-carlo-pi/) | Distributed Spark — estimate π with 100M → 10B samples |
| [iris-classification](examples/iris-classification/) | Full ML pipeline — load, train, evaluate, persist to Volumes |

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

## License

[MIT](LICENSE)
```

---

## Fase 5: Anotações — Por Que Cada Mudança Foi Feita

### Headline

**Antes**: "Run Python on Databricks clusters from your AI coding agent"
**Depois**: "Use Databricks from your AI agent — without losing context"

**Princípio aplicado**: Fórmula `{Achieve outcome} without {pain point}`. A headline anterior descreve uma feature (rodar Python). A nova descreve um resultado (usar Databricks) e endereça a dor (perder contexto).

### Subheadline

**Antes**: Lista features (auth, sessions, output capture, eviction recovery)
**Depois**: Descreve o fluxo do ponto de vista do usuário

**Princípio aplicado**: Benefits > Features. "Eviction recovery" é jargão — "no tokens wasted on auth, polling, or raw output" é o que o dev realmente sente.

### CTA movido para cima

**Antes**: Instalação enterrada na seção 5
**Depois**: Segunda seção do README

**Princípio aplicado**: "Primary CTA" deve estar above the fold. Em GitHub READMEs, "above the fold" = primeiras ~30 linhas visíveis sem scroll.

### "Why Not Just Use Genie?" subiu

**Antes**: Penúltima seção, tabela técnica de capabilities
**Depois**: Terceira seção, tabela de cenários reais

**Princípio aplicado**: Objection Handling é parte do core da página (tabela da skill). A objeção #1 do público é "já tenho Genie". Respondê-la cedo previne abandono. A tabela mudou de capabilities (features) para scenarios (benefits) — princípio Benefits > Features.

### "Why This Approach?" removida

**Antes**: Seção inteira explicando MCP vs SDK vs Skills, padrão RLM, Root LM / Sub-LMs
**Depois**: Condensada em uma linha: "Your agent's context stays clean, so sessions stay productive for 50+ interactions without compaction."

**Princípio aplicado**: One Idea Per Section + Specificity > Vagueness. O visitante quer saber o resultado ("50+ interactions sem degradação"), não a arquitetura (RLM, Root LM, Sub-LMs). A explicação técnica pode ir para uma página de docs separada.

### "How It Works" simplificado

**Antes**: 5 passos com termos como "JSON metadata", "stateful REPL session", "bootstrap helpers"
**Depois**: 3 passos em linguagem natural

**Princípio aplicado**: Simple > Complex + Customer Language > Company Language. "Scripts handle the plumbing" é o que o dev entende. "dbx_repl.py manages auth, session creation, polling, and output capture" é detalhe de implementação.

### Seção de Quick Start removida (absorvida pelo CTA)

**Antes**: Seção separada "Quick Start" com exemplo de invocação
**Depois**: O "What You Can Do" já mostra o fluxo completo

**Princípio aplicado**: One Idea Per Section. A seção "Quick Start" e "What It Feels Like" eram redundantes — ambas mostravam o fluxo de uso. Consolidei em uma.

### "Final CTA" implícito

A skill recomenda uma seção final com recap de valor e CTA. No README, a seção "Using with Other Agents" funciona como CTA secundário — "já instalou no Claude Code? Agora leve para Cursor e Copilot."

---

## Fase 6: Alternativas para Headline e CTA

A skill pede 2-3 opções com rationale:

### Headlines

| Opção | Copy | Rationale |
|-------|------|-----------|
| A | "Use Databricks from your AI agent — without losing context" | Fórmula outcome/pain. Direto, universal. |
| B | "Your AI agent + Databricks. One session, any data source." | Mais curto, enfatiza cross-domain. Menos claro sobre o "pain". |
| C | "Never switch between terminal and Databricks notebooks again" | Fórmula "Never X again". Emocional, foca na frustração do workflow quebrado. |

**Recomendação**: A (mais claro, endereça a dor principal)

### CTAs

| Opção | Copy | Rationale |
|-------|------|-----------|
| A | "Install in one command" (acima do code block) | Action + qualifier. Simples. |
| B | "Add Databricks to your agent" (acima do code block) | Foca no outcome, não no mecanismo. |
| C | "Get started — one command" | Mais direto, mas genérico. |

**Recomendação**: B (customer language — "add Databricks to your agent" é o que o dev quer fazer)

---

*Análise aplicada usando: [marketingskills/copywriting](https://github.com/coreyhaines31/marketingskills) SKILL.md v1.0.0*
*Princípios referenciados: Before Writing framework, Clarity > Cleverness, Benefits > Features, Specificity > Vagueness, Customer Language > Company Language, One Idea Per Section, Page Structure Framework (headline formulas, core sections table, CTA formula), Output Format (annotations + alternatives)*
