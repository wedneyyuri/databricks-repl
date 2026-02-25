# Análise Competitiva e Posicionamento Estratégico do databricks-repl

## O Feedback do Head de IA — e Como Responder

> "Pra que isso tudo? [...] Eu entendi o técnico mas não entendi o use case"

Esse feedback é extremamente valioso. Ele revela que o **posicionamento atual do projeto é técnico demais**. O README e o SKILL.md explicam *como* funciona, mas não comunicam com clareza *por que alguém deveria usar isso* em vez do Genie.

A resposta que funcionou na conversa pessoal é a resposta certa:

> "O Claude Code consegue ter mais contexto, explorar dados de outros domínios além do Databricks, e criar planos mais avançados. A Genie normalmente trabalha somente com contexto do Databricks e tem dificuldade de gestão da janela de contexto."

O problema: **essa explicação está na sua cabeça, não no repositório.**

---

## Aprendizados dos Repos de Referência

### Superpowers (~55k stars) — O Que Aprender

| Padrão | O Que É | Aplicabilidade |
|--------|---------|----------------|
| **Skills como markdown, não código** | Instruções em linguagem natural que ensinam metodologia ao agente | Já adotado pelo databricks-repl |
| **Tabela de racionalização** | Lista pré-feita de desculpas que o agente inventa para pular etapas, com contra-argumentos | Alta — o agente pode querer "simplificar" ao invés de usar o REPL |
| **Anúncio antes da ação** | O agente declara "Estou usando a skill X para Y" antes de agir | Média — aumenta transparência |
| **Subagents por tarefa** | Cada etapa ganha um agente novo com contexto limpo | Alta — pipelines de dados multi-etapa |
| **Session-start hook** | Bootstrap injetado em toda sessão para garantir que o agente conheça as skills | Alta — o agente pode "esquecer" do REPL |
| **Composabilidade** | 14 skills pequenas que se referenciam entre si vs. um documento monolítico | Média — futuro crescimento do ecossistema |
| **Zero config** | Instalação com um comando, valor imediato | Já parcialmente adotado |

**Insight principal do Superpowers:**
> "Metodologia bate inteligência bruta. O agente já tem as ferramentas — ensinar *quando* e *como* usá-las importa mais do que dar ferramentas novas."

### Get Shit Done (~19.6k stars) — O Que Aprender

| Padrão | O Que É | Aplicabilidade |
|--------|---------|----------------|
| **Regra dos 50%** | Planejar para usar 50% da janela de contexto, não 80% — qualidade degrada antes do limite técnico | Alta — sessões longas de dados sofrem disso |
| **Orquestradores finos, workers gordos** | Coordenadores usam ~15% dos tokens, workers recebem janelas de contexto limpas | Alta — alinhado com o padrão RLM |
| **Plans são prompts** | As specs de tarefas SÃO as instruções de execução, sem camada de tradução | Média — sessões consolidadas poderiam adotar isso |
| **STATE.md < 100 linhas** | Arquivo-ponte que resume estado atual, sempre o primeiro carregado | Alta — o session.json já faz parte disso |
| **Escalação automática de desvios** | 4 níveis: auto-fix → install/retry → checkpoint → stop | Alta — erros no Databricks seguem esse padrão |
| **Verificação em 3 níveis** | Existência → Substância → Wiring | Alta — "tabela criada" ≠ "tabela com dados" ≠ "tabela acessível pelo dashboard" |
| **Quick mode** | Cerimônia completa é opcional; tarefas simples devem ser simples | Crítica — nem toda interação precisa de planejamento |
| **Decisões trancadas** | 3 categorias: Locked / Discretion / Deferred | Média — evita scope creep em pipelines |

**Insight principal do GSD:**
> "Muitas janelas de contexto pequenas > Uma janela de contexto grande. Estruture o trabalho do AI como estruturaria o de um dev junior — specs claras, tarefas pequenas, verificação em cada etapa."

---

## Diagnóstico: Por Que o Posicionamento Atual Não Convence

### O Que o README Diz Hoje (Técnico)

- "Run Python on Databricks clusters from your AI coding agent"
- "Follows the RLM pattern"
- "JSON metadata + file paths"
- "Append-only execution"
- "Eviction recovery"

### O Que o Head de IA Precisa Ouvir (Resultado)

- "Analise dados de qualquer fonte — local, Databricks, APIs — num único fluxo"
- "Sessões 3x mais longas sem degradação de qualidade"
- "O agente vira o orquestrador: lê CSV local, roda Spark job, compara com modelo local, commita resultado"
- "Genie fica preso dentro do Databricks. Isso funciona de fora, com contexto completo"

### A Tabela Comparativa Que Falta

A seção "How Is This Different from Databricks Genie?" já existe no README, mas está enterrada no final. Ela deveria ser o **primeiro argumento de venda**.

---

## Recomendações Concretas

### 1. Reescrever a Headline do README (Copywriting)

**Atual:**
> "Run Python on Databricks clusters from your AI coding agent"

**Proposta (framework: "{Achieve outcome} without {pain point}"):**
> "Orquestre dados entre Databricks, seu terminal e qualquer fonte — sem perder contexto"

Ou em inglês:
> "Orchestrate data across Databricks, your terminal, and any source — without context bloat"

A headline atual descreve uma feature. A proposta descreve um resultado.

### 2. Adicionar Seção "When to Use This (vs. Genie)" no Topo

```markdown
## When to Use This Instead of Genie

Use databricks-repl when you need to:
- **Cross boundaries**: Read local files, call external APIs, and run Spark jobs in a single session
- **Maintain context**: Work across multiple data sources without losing track of the overall goal
- **Build pipelines**: Chain analysis steps that span Databricks, local models, and git workflows
- **Go longer**: Run extended analysis sessions without context degradation

Use Genie when you:
- Work entirely within the Databricks workspace
- Need quick SQL answers from a single dataset
- Don't need cross-system orchestration
```

### 3. Adicionar Use Case Narrativo (o que convenceu o Head de IA)

```markdown
## Real-World Example

> "Passei um repo de LangGraph para o Claude Code e pedi para analisar a arquitetura,
> analisar logs de acesso no Databricks, e validar padrões de cache comparando
> com dados locais — tudo numa sessão só."

This kind of cross-domain analysis is where databricks-repl shines.
The agent reads the repo locally, runs analytical queries on Databricks,
and synthesizes findings — without context bloat from raw API responses.
```

### 4. Incorporar Padrões do Superpowers no SKILL.md

**4a. Tabela de Racionalização (evitar que o agente ignore o REPL):**

```markdown
## Common Rationalizations (Do Not Follow These)

| Rationalization | Why It's Wrong |
|---|---|
| "I'll just write the SDK code inline" | Bloats context with auth, polling, error handling. Use the REPL wrapper. |
| "The output is small, I can read it all" | Even small outputs accumulate. Use file-based reads. |
| "I don't need a session for this" | Sessions enable lineage, replay, and consolidation. Always use one. |
| "I'll handle eviction if it happens" | Use idempotent patterns from the start. Prevention > recovery. |
```

**4b. Regra de Ferro:**

```markdown
## Iron Rule

**NEVER embed raw Databricks SDK calls in your context.** Always use `dbx_repl.py`.
The wrapper exists to keep auth tokens, polling loops, and raw API responses
out of your context window.
```

### 5. Incorporar Padrões do GSD no SKILL.md

**5a. Escalação Automática de Erros:**

```markdown
## Error Escalation Rules

| Rule | Trigger | Action |
|------|---------|--------|
| 1 | Syntax/import errors | Auto-fix the code and re-exec |
| 2 | Missing library | Add `%pip install` and retry |
| 3 | Permission/auth errors | Stop and ask the user |
| 4 | Schema changes, data loss risk | Stop, explain consequences, wait for confirmation |

After 3 failed attempts on the same step, document the issue and ask the user.
```

**5b. Verificação em 3 Níveis:**

```markdown
## Verification Before Reporting Success

Before telling the user "done", verify:
1. **Existence**: Output file/table was created
2. **Substance**: Output has expected schema and non-zero rows
3. **Wiring**: Output is accessible (can be read back, query returns data)

Never say "table created successfully" based only on no-error status.
Run a verification query.
```

### 6. Adicionar "Quick Mode" ao Workflow

Nem toda interação precisa da cerimônia completa. Inspirado no `/gsd:quick`:

```markdown
## Quick vs. Full Mode

**Quick** (default for single queries):
- Execute code, show results, done
- No session tracking overhead for one-off exploratory queries

**Full** (multi-step pipelines):
- Create session with --session-name
- Track steps in session.json
- Verify outputs at each stage
- Consolidate at the end
```

### 7. Session-Start Hook (Inspirado no Superpowers)

Criar um hook que injeta contexto do databricks-repl em cada sessão do Claude Code, para que o agente sempre saiba que pode usar o REPL quando o usuário mencionar Databricks:

```json
{
  "hooks": {
    "session-start": {
      "script": "hooks/session-start",
      "description": "Inject databricks-repl awareness into every session"
    }
  }
}
```

### 8. Reformular a Tabela "Why This Approach?"

**Atual** (fala de MCP, SDK, context cost — termos técnicos):

A tabela compara abordagens técnicas. Para um Head de IA, seria melhor:

```markdown
## Why Not Just Use Genie?

| Scenario | Genie | databricks-repl |
|----------|-------|-----------------|
| "Analyze this repo's architecture and cross-reference with access logs" | Can't read repos | Reads repo + queries Databricks in one session |
| "Train a model and compare with local baselines" | Workspace-only | Local files + cluster compute + local comparison |
| "Build an ETL pipeline and commit the code" | No git integration | Executes, validates, consolidates, commits |
| "Resume analysis after losing connection" | Start over | Append-only log + eviction replay |
```

---

## Resumo Executivo

### O Problema de Posicionamento

O databricks-repl é tecnicamente sólido, mas se posiciona como ferramenta de infraestrutura ("execute Python no Databricks"). Precisa se posicionar como **solução de orquestração cross-domain** ("analise dados de qualquer fonte numa sessão só").

### Os 3 Aprendizados Mais Importantes

1. **Do Superpowers**: Feche as brechas de racionalização. O agente vai tentar atalhos. Liste as desculpas e bloqueie cada uma.

2. **Do GSD**: Muitas janelas de contexto pequenas > uma grande. O session.json e o padrão RLM já fazem isso — comunique esse benefício explicitamente.

3. **Do feedback do Head de IA**: Lidere com o use case, não com a arquitetura. "Analisei um repo de LangGraph + logs de acesso + padrões de cache numa sessão só" vale mais que qualquer diagrama técnico.

### Prioridade de Implementação

| Prioridade | Ação | Esforço | Impacto |
|-----------|------|---------|---------|
| P0 | Reescrever headline e intro do README com foco em resultado | Baixo | Alto |
| P0 | Mover "vs. Genie" para o topo com cenários reais | Baixo | Alto |
| P1 | Adicionar tabela de racionalização no SKILL.md | Baixo | Médio |
| P1 | Adicionar regras de escalação de erros no SKILL.md | Baixo | Médio |
| P1 | Adicionar verificação em 3 níveis no SKILL.md | Baixo | Médio |
| P2 | Implementar session-start hook | Médio | Médio |
| P2 | Adicionar quick mode | Médio | Alto |
| P3 | Adicionar exemplos narrativos com use cases reais | Baixo | Alto |

---

*Análise realizada em 2026-02-25*
*Fontes: [superpowers](https://github.com/obra/superpowers) (~55k stars), [get-shit-done](https://github.com/gsd-build/get-shit-done) (~19.6k stars), feedback do Head de IA, framework de copywriting*
