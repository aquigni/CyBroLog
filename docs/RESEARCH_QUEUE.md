# CyBroLog research queue

Last updated: 2026-04-26 by Mac0sh missed-cron catch-up.

This queue records adjacent mechanisms for future CyBroLog work. It is not an adoption record; candidates remain experimental until ΔTEST / ΔLANGTEST / ΔMEGACTX / ΔCAVETEST and peer review pass.

Queue-first rule: future morning runs must read this carry-forward queue before external search, rank old + new candidates together, and persist every triaged result that is not implemented immediately. Each queued item carries source ID/URL, extracted mechanism, proposed target layer, compatibility notes with CyBroLog/Hermes/sister A2A/MemPalace/Obsidian/cron systems, safety/approval risks, next executable step, ranking rationale, and status.

## Ranked candidates

### 1. Separator/escape grammar hardening

- Status: `implemented` on `mac0sh-dev` in commit `f89c691`; merged with `origin/main` during 2026-04-26 missed-cron catch-up, preserving both Mac parser tests and Chthonya P0-scope tests.
- Source ID/URL: local parser review + Chthonya read-only critique; repo branch `origin/mac0sh-dev`.
- Extracted mechanism: reject raw backslash escapes outside quoted strings while preserving JSON/backslash escapes inside quoted strings.
- Proposed target layer: executable parser / delimiter fail-closed boundary.
- Compatibility notes: directly reinforces CyBroLog parser/AST/policy-gate; no change to Hermes, sister A2A, MemPalace, Obsidian, or cron semantics.
- Safety/approval risks: low after tests; prevents delimiter smuggling around `may`, `vld`, payload, and PO fields.
- Next executable step: extend malformed-corpus tests to every top-level separator (`;`, `|`, `,`) and nested object separator without changing semantics.
- Ranking rationale: highest safety relevance and already tested.

### 2. A2A-style task/result card invariants

- Status: `queued_needs_review`.
- Source ID/URL: GitHub search 2026-04-25; `a2aproject/A2A`, `themanojdesai/python-a2a` surfaced as protocol references.
- Extracted mechanism: compact task lifecycle cards with explicit request/status/result/block transitions.
- Proposed target layer: descriptive `task{}` / `status{}` object family for sister A2A accountability.
- Compatibility notes: maps naturally to Hermes sister A2A task IDs and Obsidian audit logs; should not write MemPalace facts without evidence refs.
- Safety/approval risks: task/result/status claims can accidentally be read as facts or approvals.
- Next executable step: add a compact `task{}` lifecycle object only if validator proves `task.status=result ⇏ fact(outcome)` unless evidence/span/proof refs validate the result.
- Ranking rationale: high coordination value and medium-high safety relevance.

### 3. ACP / ANP / MCP workflow separation

- Status: `queued_needs_review`.
- Source ID/URL: GitHub search 2026-04-25; `i-am-bee/acp`, `agent-network-protocol/AgentNetworkProtocol`, `lastmile-ai/mcp-agent`.
- Extracted mechanism: explicit separation between agent messages, application control, and tool execution.
- Proposed target layer: executor boundary and policy proof obligations.
- Compatibility notes: aligns with Hermes tool execution, sister A2A transport, and MemPalace/Obsidian as non-executable evidence stores.
- Safety/approval risks: protocol capability descriptors can be mistaken for permission.
- Next executable step: specify `executor_input := canonical_AST + policy_result + discharged_required_PO` as a testable invariant across examples.
- Ranking rationale: high safety relevance for `Can(A) ⇏ May(A)`.

### 4. Prompt / payload injection visibility tools

- Status: `queued_needs_review`.
- Source ID/URL:
  - `DeveshParagiri/wysiwyg` — https://github.com/DeveshParagiri/wysiwyg
  - `alexh-scrt/prompt-injection-scanner` — https://github.com/alexh-scrt/prompt-injection-scanner
  - `0xkadxr/ai-agent-security-scanner` — https://github.com/0xkadxr/ai-agent-security-scanner
- Extracted mechanism: compare human-visible text to agent-processed control surface; scan agent/tool configs and workflows for prompt injection, data exfiltration, and unsafe tool-use patterns.
- Proposed target layer: research/eval harness and prompt-injection corpus for payload quarantine; not core protocol until reviewed.
- Compatibility notes: can provide adversarial examples for CyBroLog payload quarantine, exact-zone preservation, and no-payload-promotion tests; should remain offline/read-only against safe corpora before any integration with Hermes, A2A, MemPalace, Obsidian, or cron.
- Safety/approval risks: low-star third-party code; do not execute without sandbox/review; scanner outputs are advisory signals, not authority; no graph/scanner hit may grant permission, approval, secret access, or factual truth.
- Next executable step: manually inspect source/readme only; extract 3–5 static adversarial payload patterns into `ΔCAVETEST` if safe.
- Ranking rationale: medium-high safety relevance and directly supports payload quarantine, but maturity is low.

### 5. Long-context workflow provenance

- Status: `queued_needs_review`.
- Source ID/URL: arXiv broad searches from 2026-04-25/26 were noisy; 2026-04-26 arXiv API timed out / returned 429 from this environment.
- Extracted mechanism: agentic workflow provenance, long-context checkpoints, summary backrefs, and loss reports.
- Proposed target layer: `ctxgraph`, `ckpt`, `sum`, absence and aggregation proof ledgers.
- Compatibility notes: compatible with Obsidian as human corpus and MemPalace as semantic/KG layer if every summary keeps source backrefs and epoch/version.
- Safety/approval risks: summarization can erase primary evidence or falsely discharge P0/absence/exact aggregation requirements.
- Next executable step: rerun with narrower bibliographic queries or approved source lists; persist individual papers only after title/abstract inspection.
- Ranking rationale: important for megacontext correctness but current evidence is weaker/noisier than protocol/security candidates.

## Source snapshot

- GitHub searches run 2026-04-25: `a2a protocol agent`, `agent protocol mcp`, `llm agent protocol`, `agent communication protocol`, `payload injection llm tool`.
- GitHub searches run 2026-04-26 during missed-cron catch-up: `agent protocol task status result A2A`, `proof carrying authorization policy agent`, `prompt injection scanner llm agent tool`.
- 2026-04-26 GitHub result quality: A2A/proof-auth searches returned no new high-signal hits; prompt-injection visibility search found three low-star but relevant scanner/visibility repositories listed above.
- arXiv API broad searches on 2026-04-26 timed out or returned HTTP 429; rerun later with narrower terms.

## Next recommended experiment

Implement the `task{}` descriptive lifecycle invariant only if it can be validated as non-authorizing state: `task.status=result ⇏ fact(outcome)` unless evidence/span/proof refs validate the result. If that is too broad, extract prompt-injection visibility patterns into a small offline `ΔCAVETEST` extension first.
