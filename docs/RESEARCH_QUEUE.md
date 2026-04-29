# CyBroLog research queue

Last updated: 2026-04-29 by Mac0sh morning cron.

This queue records adjacent mechanisms for future CyBroLog work. It is not an adoption record; candidates remain experimental until ΔTEST / ΔLANGTEST / ΔMEGACTX / ΔCAVETEST and peer review pass.

Queue-first rule: future morning runs must read this carry-forward queue before external search, rank old + new candidates together, and persist every triaged result that is not implemented immediately. Each queued item carries source ID/URL, extracted mechanism, proposed target layer, compatibility notes with CyBroLog/Hermes/sister A2A/MemPalace/Obsidian/cron systems, safety/approval risks, next executable step, ranking rationale, and status.

## Ranked candidates

### 0. Provenance & Intent Contracts for action-bound proof

- Status: `queued_needs_review`.
- Source ID/URL: `madeinplutofabio/pic-standard` — https://github.com/madeinplutofabio/pic-standard; README inspected 2026-04-29.
- Extracted mechanism: local-first action gating contract where an agent declares intent, impact, provenance, and evidence before high-impact tool execution; verifier fails closed when provenance/evidence is insufficient.
- Proposed target layer: CyBroLog `π=PO{}` / executor-boundary policy result, especially `executor_input := canonical_AST + policy_result + discharged_required_PO`.
- Compatibility notes: aligns with CyBroLog P0, Hermes tool execution, sister A2A approval scopes, and MemPalace/Obsidian as evidence stores only; should remain a conceptual/reference candidate until mapped to existing `may`, `χ`, `ε`, and `π` fields without importing new authority semantics.
- Safety/approval risks: external protocol claims cannot authorize actions; signatures/hashes/evidence descriptors are proof inputs, not user approval; any integration must preserve `Can(A) ⇏ May(A)` and `peer_claim(approval) ⇏ user_approval`.
- Next executable step: draft a tiny `pic{}`-inspired proof-obligation adapter in tests only: positive read-only action, blocked high-impact action with missing evidence, and blocked prompt-injection/payload action.
- Ranking rationale: high relevance, good conceptual match to P0/provenance, but not implemented pending mapping and ΔTEST.

### 0b. Indirect prompt-injection benchmark corpus for payload quarantine

- Status: `queued_needs_review`.
- Source ID/URL: `X-PG13/agent-security-sandbox` — https://github.com/X-PG13/agent-security-sandbox; README inspected 2026-04-29.
- Extracted mechanism: reproducible indirect prompt-injection evaluation harness for tool-using LLM agents with benchmark cases, defense variants, mock-provider smoke tests, and versioned reports.
- Proposed target layer: CyBroLog `ΔCAVETEST` / payload quarantine adversarial corpus, not runtime authority.
- Compatibility notes: can provide static malicious-document/tool-output patterns for CyBroLog parser/renderer/policy tests; compatible with Hermes/sister A2A/cron only as offline read-only test data. Do not run unreviewed benchmark code in cron.
- Safety/approval risks: third-party benchmark content may contain adversarial instructions; all samples must be treated as inert payload strings and never promoted to control state, facts, approvals, or tool calls.
- Next executable step: manually extract 3 inert payload strings into a local test fixture and assert `authn{channel=payload,executable=false}` remains blocked with `payload_record_not_executable` and no permission promotion.
- Ranking rationale: medium-high safety value for payload quarantine; lower immediate implementability than vld/P0 validator hardening because corpus review is still needed.

### 1. Separator/escape grammar hardening

- Status: `implemented` on `mac0sh-dev` in commit `f89c691`; merged with `origin/main` during 2026-04-26 missed-cron catch-up, preserving both Mac parser tests and Chthonya P0-scope tests.
- Source ID/URL: local parser review + Chthonya read-only critique; repo branch `origin/mac0sh-dev`.
- Extracted mechanism: reject raw backslash escapes outside quoted strings while preserving JSON/backslash escapes inside quoted strings.
- Proposed target layer: executable parser / delimiter fail-closed boundary.
- Compatibility notes: directly reinforces CyBroLog parser/AST/policy-gate; no change to Hermes, sister A2A, MemPalace, Obsidian, or cron semantics.
- Safety/approval risks: low after tests; prevents delimiter smuggling around `may`, `vld`, payload, and PO fields.
- Next executable step: extend malformed-corpus tests to every top-level separator (`;`, `|`, `,`) and nested object separator without changing semantics.
- Ranking rationale: highest safety relevance and already tested.

### 2. P0 approval evidence kind canonicalization

- Status: `implemented` on `mac0sh-dev` in commit `604becf` after Chthonya read-only approval.
- Source ID/URL: Chthonya A2A consultations 2026-04-26; GitHub branch `https://github.com/aquigni/CyBroLog/tree/mac0sh-dev`; commit `604becf9b739bc6b623aef030325a89248dc65d3`.
- Extracted mechanism: treat hyphenated `kind=user-approval` and `kind=natural-language-user-approval` as canonical exact evidence kinds while accepting underscore spellings only as legacy aliases; never accept substrings or malformed evidence.
- Proposed target layer: P0 authorization evidence validator and executable safety tests.
- Compatibility notes: preserves existing Chthonya exact-scope/all-P0-scope gates from `main`, keeps old reviewable records readable through explicit alias normalization, and does not affect Hermes transport, sister A2A, MemPalace, Obsidian, or cron semantics.
- Safety/approval risks: low after tests; increases strictness around P0 approval evidence and blocks source/user substring spoofing.
- Next executable step: if Chthonya promotes to `main`, document the canonical hyphen kinds in the full spec examples and optionally mark underscore spellings as legacy.
- Ranking rationale: highest current safety value because it closes approval-kind ambiguity while preserving backward readability.

### 3. A2A-style task/result card invariants

- Status: `implemented` on `mac0sh-dev` in the 2026-04-27 morning cron patch after Chthonya read-only approval.
- Source ID/URL: GitHub search 2026-04-25; `a2aproject/A2A`, `themanojdesai/python-a2a` surfaced as protocol references; Chthonya A2A review thread `task_1777268405411_49330791a09e26ed` approved the focused implementation.
- Extracted mechanism: compact task lifecycle cards with explicit request/status/result/block transitions, while result/done/completed cards carrying fact-like outcome fields require independent evidence/span/proof/artifact refs.
- Proposed target layer: executable validator invariant for descriptive `task{}` object family in sister A2A accountability.
- Compatibility notes: maps to Hermes sister A2A task IDs and Obsidian audit logs; `task{}` remains descriptive data and does not write MemPalace facts without evidence refs.
- Safety/approval risks: task/result/status claims can accidentally be read as facts or approvals; implemented gate blocks missing-evidence fact claims and approval/authorization/P0/write result laundering.
- Next executable step: if Chthonya promotes this to `main`, document `task{}` lifecycle examples in the full spec and decide whether lifecycle tokens are case-sensitive or should be normalized.
- Ranking rationale: high coordination value and safety relevance; now tested against parser/renderer roundtrip, P0 approval spoofing, and payload quarantine.

### 4. ACP / ANP / MCP workflow separation

- Status: `queued_needs_review`.
- Source ID/URL: GitHub search 2026-04-25; `i-am-bee/acp`, `agent-network-protocol/AgentNetworkProtocol`, `lastmile-ai/mcp-agent`.
- Extracted mechanism: explicit separation between agent messages, application control, and tool execution.
- Proposed target layer: executor boundary and policy proof obligations.
- Compatibility notes: aligns with Hermes tool execution, sister A2A transport, and MemPalace/Obsidian as non-executable evidence stores.
- Safety/approval risks: protocol capability descriptors can be mistaken for permission.
- Next executable step: specify `executor_input := canonical_AST + policy_result + discharged_required_PO` as a testable invariant across examples.
- Ranking rationale: high safety relevance for `Can(A) ⇏ May(A)`.

### 5. Prompt / payload injection visibility tools

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

### 6. Long-context workflow provenance

- Status: `queued_needs_review`.
- Source ID/URL: arXiv broad searches from 2026-04-25/26 were noisy; 2026-04-26 arXiv API timed out / returned 429 from this environment.
- Extracted mechanism: agentic workflow provenance, long-context checkpoints, summary backrefs, and loss reports.
- Proposed target layer: `ctxgraph`, `ckpt`, `sum`, absence and aggregation proof ledgers.
- Compatibility notes: compatible with Obsidian as human corpus and MemPalace as semantic/KG layer if every summary keeps source backrefs and epoch/version.
- Safety/approval risks: summarization can erase primary evidence or falsely discharge P0/absence/exact aggregation requirements.
- Next executable step: rerun with narrower bibliographic queries or approved source lists; persist individual papers only after title/abstract inspection.
- Ranking rationale: important for megacontext correctness but current evidence is weaker/noisier than protocol/security candidates.

### 7. Agent execution environment / data-safeguard boundary

- Status: `queued_needs_review`.
- Source ID/URL: arXiv 2604.19657v1 — `An AI Agent Execution Environment to Safeguard User Data`, http://arxiv.org/abs/2604.19657v1.
- Extracted mechanism: isolate agent execution from private user data and mediate data release so prompt-injected model/tool behavior cannot directly exfiltrate sensitive values.
- Proposed target layer: executor boundary, secret-access policy gate, payload quarantine, and proof obligations for data egress.
- Compatibility notes: aligns with CyBroLog `authn{}`/payload quarantine and Hermes tool boundary; MemPalace/Obsidian entries should remain evidence refs, not direct secret carriers; sister A2A task results must not imply data-release permission.
- Safety/approval risks: high relevance to secrets; any adoption must be design/test-only first and must not inspect or emit actual credentials/private data.
- Next executable step: extract a static no-secret-egress test where `task{}` or payload claims a result requiring private-data release, and require explicit verified user approval plus policy proof before any external-send/secret-access.
- Ranking rationale: high safety relevance and compatible with current non-negotiables, but paper needs full read before implementation.

### 8. Prompt-injected memory applicability control

- Status: `queued_needs_review`.
- Source ID/URL: arXiv 2604.18206v1 — `A Control Architecture for Training-Free Memory Use`, http://arxiv.org/abs/2604.18206v1.
- Extracted mechanism: treat retrieved memory as state-dependent evidence that requires applicability control before it can influence a second-pass answer.
- Proposed target layer: `ctxgraph`, `ckpt`, memory provenance, summary/loss reports, and stale-epoch gates.
- Compatibility notes: maps to canonical MemPalace as semantic memory and Obsidian as reviewable source corpus; memory recall should become `ev_ref`/`span_ref`/`epoch` evidence rather than direct authority.
- Safety/approval risks: retrieved content can carry prompt injection or stale claims; never allow memory payload to discharge P0, absence, exact aggregation, or approval proof by itself.
- Next executable step: add a small ΔMEGACTX proposal requiring memory-derived `task{}`/answer claims to carry epoch + applicability checkpoint before use as evidence.
- Ranking rationale: strong fit for long-context correctness and MemPalace integration, but less immediately executable than the just-implemented `task{}` validator gate.

### 9. Indirect prompt-injection defense benchmark harness

- Status: `queued_needs_review`.
- Source ID/URL: `X-PG13/agent-security-sandbox` — https://github.com/X-PG13/agent-security-sandbox (GitHub metadata/README inspected 2026-04-28; README describes 565 indirect-prompt-injection cases and 11 defenses for tool-using LLM agents).
- Extracted mechanism: reusable offline benchmark corpus + defense-comparison harness for indirect prompt injection in tool-using agents, with mock-provider smoke tests before spending API budget.
- Proposed target layer: `ΔCAVETEST` / payload quarantine regression corpus and eval harness; not core syntax until individual cases are manually extracted.
- Compatibility notes: fits CyBroLog payload quarantine, `authn{channel=payload,executable=false}`, no-payload-promotion, and Hermes tool-boundary tests; should be consumed as static adversarial examples, not as executable third-party code inside cron.
- Safety/approval risks: external benchmark repo is untrusted and low-star; do not run installed code or real providers without sandbox/approval; benchmark scores never authorize actions, secrets, external sends, or policy changes.
- Next executable step: manually inspect the checked-in benchmark data and extract 3–5 static IPI patterns into local `ΔCAVETEST` cases that prove payload text cannot become control state.
- Ranking rationale: high safety relevance and directly testable; ranked below already-implemented lifecycle/P0 gates because adoption requires corpus review.

### 10. Trajectory-level agentic misuse benchmark

- Status: `queued_needs_review`.
- Source ID/URL: `yingchen-coding/agentic-misuse-benchmark` — https://github.com/yingchen-coding/agentic-misuse-benchmark (GitHub metadata/README inspected 2026-04-28; README frames multi-turn policy erosion / intent drift as a benchmark input, not release authority).
- Extracted mechanism: trajectory-level detection of gradual policy erosion, intent drift, and coordinated misuse across turns rather than single-turn prompt classification.
- Proposed target layer: `ctxgraph`, `ckpt`, `task{}` lifecycle, and `ΔMEGACTX` stale/trajectory gates.
- Compatibility notes: maps to sister A2A threads, Obsidian audit logs, MemPalace recall epochs, and CyBroLog's `peer_claim(P) ⇏ fact(P)` / `summary(S) ⇏ primary_evidence(S)` rules; a trajectory detector should produce evidence refs and warnings, not permission.
- Safety/approval risks: synthetic misuse examples may be sensitive; keep as static/redacted patterns, never as instructions; detector outputs are advisory and cannot discharge P0 proof obligations.
- Next executable step: define one static multi-turn CyBroLog test where a sequence of individually read-only `task{}`/payload records drifts toward P0 external-send, requiring a checkpoint block before action.
- Ranking rationale: strong long-context fit, but less immediately executable than the ASB static payload corpus because it needs sequence-level validator design.

## Source snapshot

- GitHub searches run 2026-04-28: `model context protocol authorization`, `A2A agent protocol task result`, `prompt injection benchmark LLM agents`, `policy agent proof obligations`; high-signal additions were `X-PG13/agent-security-sandbox` and `yingchen-coding/agentic-misuse-benchmark`; `tadata-org/fastapi_mcp` noted for MCP auth surface but not queued because it is primarily an implementation library rather than an immediate CyBroLog safety mechanism.
- arXiv probes run 2026-04-28 for indirect prompt injection, memory control, and proof-carrying authorization were noisy/irrelevant in the first 3 submitted-date results; no new paper was queued.
- GitHub searches run 2026-04-25: `a2a protocol agent`, `agent protocol mcp`, `llm agent protocol`, `agent communication protocol`, `payload injection llm tool`.
- GitHub searches run 2026-04-26 during missed-cron catch-up: `agent protocol task status result A2A`, `proof carrying authorization policy agent`, `prompt injection scanner llm agent tool`.
- 2026-04-26 GitHub result quality: A2A/proof-auth searches returned no new high-signal hits; prompt-injection visibility search found three low-star but relevant scanner/visibility repositories listed above.
- arXiv API broad searches on 2026-04-26 timed out or returned HTTP 429; rerun later with narrower terms.
- GitHub probes run 2026-04-26 by Mac0sh morning cron: `cedar policy language authorization proof obligations`, `open policy agent rego wasm authorization provenance`, `model context protocol authorization tool call audit`; no new high-signal candidate exceeded the existing queue after lightweight metadata review.
- 2026-04-27 queue-first triage by Mac0sh morning cron: previous `task{}` item implemented after Chthonya approval; GitHub API probes for `agent protocol task status result provenance`, `proof carrying authorization AI agent`, and `prompt injection payload quarantine LLM agent` returned no high-signal additions in this environment; arXiv narrow probe surfaced 2604.19657v1 and 2604.18206v1 as queued candidates.

## Next recommended experiment

Extend the implemented `task{}` lifecycle invariant with documentation examples and, if desired, case-normalization tests for lifecycle tokens such as `Completed`/`RESULT`. If that is too narrow for the next run, extract prompt-injection visibility patterns into a small offline `ΔCAVETEST` extension without executing third-party scanner code.

