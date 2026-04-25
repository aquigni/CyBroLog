# CyBroLog research queue

Last updated: 2026-04-25 by Mac0sh morning cron.

This queue records adjacent mechanisms for future CyBroLog work. It is not an adoption record; candidates remain experimental until ΔTEST / ΔLANGTEST / ΔMEGACTX / ΔCAVETEST and peer review pass.

## Ranked candidates

1. **Separator/escape grammar hardening** — adopted on `mac0sh-dev` in commit `f89c691` for raw backslash outside quoted strings. Future adjacent work: extend malformed-corpus tests to every top-level separator (`;`, `|`, `,`) and nested object separator without changing semantics.
   - Source pressure: local parser review and Chthonya read-only critique.
   - Safety relevance: high; prevents delimiter smuggling around `may`, `vld`, payload, and PO fields.
   - Implementability: high.

2. **A2A-style task/result card invariants** — study `a2aproject/A2A` and related A2A libraries for compact task lifecycle fields that could map to CyBroLog `task/status/result/block` atoms without granting authorization.
   - Source snapshot: GitHub search found `a2aproject/A2A` and `themanojdesai/python-a2a` as high-signal protocol surfaces.
   - Safety relevance: medium-high; useful for provenance and accountable handoff.
   - Adoption condition: no peer/task status claim may become fact or permission.

3. **ACP / ANP / MCP workflow separation** — study `i-am-bee/acp`, `agent-network-protocol/AgentNetworkProtocol`, and `lastmile-ai/mcp-agent` for explicit boundaries between agent messages, application control, and tool execution.
   - Safety relevance: high for `executor_input := canonical_AST + policy_result + discharged_required_PO`.
   - Adoption condition: preserve `Can(A) ⇏ May(A)` and payload/control plane separation.

4. **Long-context workflow provenance** — arXiv triage surfaced current work on agentic scientific workflows and long-context / omni-context handling. Future search should use more precise bibliographic queries or approved source lists because broad arXiv queries were noisy.
   - Safety relevance: medium for `ctxgraph`, `ckpt`, summary backrefs, and absence/aggregation proof.
   - Adoption condition: no exact aggregation or verified absence without scoped coverage and checkpoint pass.

5. **Prompt/payload injection visibility tools** — low-star GitHub hits suggest scanner/diff approaches for hidden prompt-injection payloads. Mechanism worth extracting: compare human-visible text to agent-processed control surface.
   - Safety relevance: medium-high for payload quarantine and exact-zone preservation.
   - Adoption condition: data-only payload model; no payload-code execution or promotion.

## Source snapshot

- GitHub searches run 2026-04-25: `a2a protocol agent`, `agent protocol mcp`, `llm agent protocol`, `agent communication protocol`, `payload injection llm tool`.
- High-signal repositories surfaced: `a2aproject/A2A`, `themanojdesai/python-a2a`, `agent-network-protocol/AgentNetworkProtocol`, `i-am-bee/acp`, `lastmile-ai/mcp-agent`, `casibase/casibase`.
- arXiv API broad searches were noisy; Semantic Scholar API returned 403 from this environment.

## Next recommended experiment

Add a compact `task{}` lifecycle object only if it can be validated as descriptive state, not authorization. Candidate invariant: `task.status=result ⇏ fact(outcome)` unless evidence/span/proof refs validate the result.
