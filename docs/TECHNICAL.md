# Technical architecture

## Pipeline

```text
surface → parser → canonical AST → renderer → round-trip check → policy gate → proof-obligation gate → executor decision
```

Raw text never executes. Only canonical AST plus policy result plus discharged proof obligations can reach an executor.

## Implemented components

- `CyBroLogParser`: conservative CL2.v2.2 subset parser.
- `render_record`: canonical renderer.
- `validate_record`: policy/safety/absence/aggregation/compression gate.
- `cave_codec`: exact-zone preserving compression seed.
- `run_benchmark_suite`: deterministic local activation suite for ΔTEST / ΔLANGTEST / ΔMEGACTX / ΔCAVETEST.

## Safety gates

- P0 actions require locally verifiable natural-language user approval: each required risky scope must have an explicit evidence item with `source=user`, canonical `kind=user-approval` or `kind=natural-language-user-approval` (legacy underscore aliases are accepted only for backward readability), `verified=true`, and matching `scope`.
- Peer approval claims never become user approval.
- Payload records are quarantined by default.
- `absent_verified_C` requires scoped full coverage and checkpoint pass.
- `agg.exact=true` requires partition/partial + deterministic merge proof and verifier.
- Safety-relevant compression requires AST equivalence and validation ledger.

## CL2.v2.2 field families

```text
cmp{}   compression envelope
zone{}  exact-zone preservation ledger
val{}   validation ledger
fix{}   targeted repair ledger
mcmp{}  memory/artifact compression object
style_state{} safe persistent mode state
```

## Benchmarks

Local activation runs synthetic deterministic gates:

- parser round-trip;
- delimiter fuzz inside quoted strings;
- fake approval rejection;
- payload instruction quarantine;
- partial-search absence rejection;
- exact aggregation proof rejection;
- exact-zone preservation;
- sensitive-path refusal.

These tests activate the implementation as an executable local dialect. They do not claim universal LLM benchmark performance.
