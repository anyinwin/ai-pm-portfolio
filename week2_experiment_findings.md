# Week 2 Experiment Findings
**PatientGuide AI PM Learning Plan**
**Annhien Nguyen | February 2026**

---

## Experiment 1 — Temperature

**What I observed:**
Running the same PatientGuide question 3 times at temperature 0 
produced nearly identical responses each time. Running it 3 times 
at temperature 1 produced more variance — different supporting 
details, inconsistent additional codes, and varying follow-up 
questions across runs.

**What it means for PatientGuide:**
PatientGuide should use a low temperature (close to 0). Users are 
relying on specific CPT codes and exact questions to ask their 
insurance company and provider. Consistency and accuracy matter 
more than creativity. A user who gets a different answer each time 
they ask the same question will lose trust in the product.

**Configuration decision:** Temperature 0 or 0.1

---

## Experiment 2 — Token Counting

**What I observed:**
Three prompts of increasing complexity returned 15, 51, and 112 
tokens respectively. Token counts were higher than word counts in 
all three cases — roughly 1.3-1.5 tokens per word for short 
prompts, dropping toward 1.1-1.2 for longer prompts with more 
common words. Specialized terms like "CPT" tokenize differently 
than everyday words.

**What it means for PatientGuide:**
Token counts directly determine cost and context window usage. 
A full PatientGuide request — system prompt (~500 tokens), RAG 
chunks (~1500 tokens), conversation history (~500 tokens), user 
message (~100 tokens) — totals roughly 2,600-3,000 tokens per 
request. At scale, this is a meaningful cost to manage.

**Cost levers identified (in order of priority):**
1. Model selection — Haiku vs Opus (highest impact)
2. RAG chunk count — retrieve 3 instead of 5
3. System prompt compression — keep instructions tight
4. Max tokens on response — last resort, most user-facing tradeoff

---

## Experiment 3 — Context Window

**What I observed:**
Sending 102,000 tokens (52,000 words of repeated CPT code text) 
did not produce an error. Claude processed it successfully and 
extracted the meaningful signal from the repetition, responding 
to the underlying CPT code content. The response was cut off 
mid-sentence due to max_tokens being set to 100, not due to a 
context window error.

**What it means for PatientGuide:**
Claude Haiku's 200,000 token context window is large enough that 
PatientGuide is unlikely to hit a hard limit. The real risk is 
soft degradation — as conversation history accumulates over many 
exchanges, earlier context (like the user's insurance type) gets 
less attention and Claude's responses become less personalized. 
This is a silent failure, not an obvious error.

**Design implication:**
Implement a sliding window for conversation history — keep only 
the last 5-10 exchanges plus a summary of key facts (insurance 
type, deductible status, location). Never let history grow 
unbounded.

---

## Experiment 4 — Model Comparison

**What I observed:**
Haiku outperformed Opus for PatientGuide's primary use case. 
Haiku returned actionable questions to ask insurance and provider, 
practical next steps, and concise CPT code guidance in 4.63 
seconds using 423 tokens. Opus returned technically comprehensive 
CPT code tables with deep billing nuance in 13.28 seconds using 
557 tokens — impressive depth, but less matched to what an anxious 
patient actually needs before an appointment.

**Key insight:**
Model capability and model fit are different things. Opus is more 
capable. Haiku is more fit for PatientGuide's core user need — 
fast, actionable, human guidance before a medical appointment.

**PatientGuide model recommendation:**

| Feature | Model | Reason |
|---------|-------|--------|
| Main Find + Prepare flow | Haiku | Fast, actionable, cost-effective |
| Complex edge cases | Opus | Billing disputes, chronic conditions, unusual insurance situations |
| Simple FAQ queries | Haiku | No need for Opus depth |

Route to Opus only when query signals complexity — multiple 
conditions, billing disputes, out-of-network situations.

---

## Overall PatientGuide Configuration Recommendation

| Parameter | Setting | Reason |
|-----------|---------|--------|
| Model | claude-haiku-4-5-20251001 (default) | Better fit for core use case, 3x faster, lower cost |
| Temperature | 0.1 | Consistency and accuracy over creativity |
| Max tokens | 800 | Enough for complete actionable response, prevents runaway cost |
| RAG chunks | 3-5 | Enough context without bloating the window |

---

*Experiments run February 2026 as part of PatientGuide AI PM 
Learning Plan. All findings informed by hands-on API experimentation 
rather than documentation alone.*