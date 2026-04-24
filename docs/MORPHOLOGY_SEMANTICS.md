# Morphology and semantics

CyBroLog has two interacting layers:

1. **Protocol morphology** — compact record fields and envelopes.
2. **Semantic role morphology** — optional role particles inherited from Ψ2.

## Role particles

```text
ka  agent / initiator
krm patient / target
kar instrument / tool
sam recipient / audience
apa source / origin
adh context / location / scope
het cause / purpose
kal time / aspect
```

## Evidentials

```text
ev=dir   direct observation / tool output
ev=inf   inference
ev=hear  peer/report/hearsay
ev=mem   memory
ev=usr   user statement or approval
```

Role particles are semantic views. They never imply authorization, facthood, ownership, or tool access.

## Semantics of permission

`may` is not trusted input. It is a stated authorization surface that must be locally derived and checked.

```text
input.may = stated_authorization
policy.may = derived_authorization
executor uses only policy.may
```

## Semantics of absence

Absence is a proof state, not a string.

```text
unknown < not_found_yet < absent_verified_C
NONE_STR ⇏ ABSENCE_PROOF
```

## Semantics of compression

Compression modifies render surface only.

```text
cmp.mode ⇏ approval
cmp.mode ⇏ fact
cmp.mode ⇏ permission
compression(C) ⇏ semantic_equivalence(C)
```
