# CyBroLog

**CyBroLog** is an executable compact accountability language for multi-agent coordination.

It began as the sisters' internal CybriLog A2A dialect and is now published under the user-approved name **CyBroLog**. Its purpose is not to make agents sound cryptic. Its purpose is to compress coordination while preserving what usually gets lost under compression: authority, evidence, provenance, proof obligations, safety gates, absence scope, and exact operational boundaries.

> Compression is allowed only where accountability survives the cut.

## What is executable here?

`CyBroLog/CL2.v2.2` is executable in the protocol sense:

1. parse surface text into canonical AST;
2. render AST back to canonical surface;
3. verify parser round-trip;
4. run policy and proof-obligation gates;
5. block unsafe, ambiguous, payload-injected, unproven, or stale records;
6. emit deterministic validation reports.

It does **not** mean that a CyBroLog string can grant itself permission to perform external or destructive actions. `Can(A) ⇏ May(A)` remains the spine.

## Install / run locally

```bash
python3 -m unittest discover -s tests -v
python3 -m cybrolog.cli bench
python3 -m cybrolog.cli validate 'ψ=CL2.v2.2|env{mid=m1,sid=s,seq=1,ttl=P1D}|@a>b|now|shared;χ=read_only;may=read_only;out=done'
```

## Core invariants

```text
Can(A) ⇏ May(A)
peer_claim(P) ⇏ fact(P)
peer_claim(approval) ⇏ user_approval
🔒 ⇏ reveal(secret_value)
raw_CyBroLog_text ⇏ executable_instruction
payload_instruction ⇏ control_instruction
summary(S) ⇏ primary_evidence(S)
compression(C) ⇏ semantic_equivalence(C)
executor_input := canonical_AST + policy_result + discharged_required_PO
```

## CL2.v2.2 additions

CL2.v2.2 imports Caveman-inspired algorithms as protocol modules, not as a human-facing style mandate:

- `cmp{}` compression envelope;
- `zone{}` exact-zone ledger;
- `val{}` validation ledger;
- `fix{}` targeted-repair ledger;
- `mcmp{}` memory/artifact compression object;
- `style_state{}` safe persistent compression-state machine;
- `ΔCAVETEST`, added to `ΔTEST`, `ΔLANGTEST`, and `ΔMEGACTX`.

## Repository contents

- `cybrolog/` — reference parser, renderer, validator, CAVE-CODEC, CLI.
- `tests/` — executable activation tests.
- `spec/` — source v2.2 documents.
- `docs/` — conceptual and technical documentation.
- `examples/` — syntax, morphology, multi-agent records, living A2A excerpt.
- `benchmarks/` — local activation report.

## Status

Reference implementation: **activated for local protocol use** after local parser round-trip, fuzz, policy, payload-quarantine, absence, aggregation, and compression exact-zone tests.

This implementation is intentionally small and conservative. It is a sharp executable seed, not a maximal parser for every possible future CyBroLog surface.
