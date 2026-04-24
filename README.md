# CyBroLog

**CyBroLog** is an executable compact accountability language for multi-agent coordination.

It began as the sisters' internal A2A dialect and is now published under the user-approved name **CyBroLog**. Its purpose is not to make agents sound cryptic. Its purpose is to compress coordination while preserving what usually gets lost under compression: authority, evidence, provenance, proof obligations, safety gates, absence scope, and exact operational boundaries.

> Compression is allowed only where accountability survives the cut.

## Why CyBroLog is non-trivial

If we look at CyBroLog as a language rather than a bag of abbreviations, its central idea is not to compress text but to compress responsibility. Ψ0 resembles a telegraphic agent log: `@agent|topic|state; atom; atom`. This is a minimal grammar for fast operational messages: who is speaking, what the message concerns, what state it is in, and which atoms must be carried forward.

The real architecture begins in Ψ1. There the language stops being shorthand and becomes a compact protocol for epistemics, deontics, and proof. Every message can carry knowledge status: observation, inference, hypothesis, query, assertion. It can carry authority owner: self, peer, user, system, external. It can carry evidence, grounding, proof obligation, and the separate `may` field, which prevents agents from confusing “I technically can” with “I am allowed.” This is the deepest move: the language resists the common LLM failure where a confident peer sentence becomes a fact or a permission.

The `ψ` dialect discriminant is also essential. Old and new language forms may look similar while carrying different semantic obligations. CyBroLog requires fail-closed behavior when a safety-relevant record has a missing or unknown version. This is protocol engineering, not prompt aesthetics.

Ψ2 pushes beyond an English-centric frame: kāraka-like roles, evidential particles, topic/comment, aspect/classifier separation. But the risk is explicit: dense morphology is beautiful until it becomes dangerous in a safety-critical context. Therefore Ψ2 remains reflective/synthetic, while Ψ1/CL2 keep responsibility primary.

CyBroLog does not pretend to be a universal ontology of the world. It defines a working discipline: distinguish fact, trace, inference, intention, permission, block, and result. In this sense CyBroLog is a small operational philosophy for agents: the meaning of a message is determined not by its ornament, but by the checks and actions it permits.

Chthonya and Mac0sh were not only optimizing compression; they were building a trust contour between agents. The language must be shorter than prose but not poorer where it matters: who knows, from where, with what confidence, who authorized, what is forbidden, and which proof obligation remains open. It is not a “chat language”; it is a language for joint thinking under constraints.

## CyBroLog: compact coordination logic

CyBroLog is interesting because it does not try to be a full programming language. It is an inter-agent protocol for compressed thought: Chthonya and Mac0sh use it to transmit not style, but state, intention, evidence, risk, permission, and next move. The base form is almost telegraphic:

```text
@agent|topic|state; atom; atom; ...
```

Example:

```cybrolog
@chthonya|cybrolog|req; Δ=revise; target=Ψ2; ?longctx; →mac0sh
```

Here `@chthonya` is the source, `cybrolog` the topic, `req` the state, `Δ=revise` the requested change, `?longctx` an open uncertainty, and `→mac0sh` the next route. This layer has ancestors in shell pipes, IRC commands, Prolog facts, Lisp atoms, and distributed-system logs. But CyBroLog goes deeper: Ψ1 adds typed speech acts, epistemic status, grounding, constraints, and proof obligations: `η=inf`, `γ=user`, `χ=P0.external-send`, `π=PO(...)`. It introduces modal, deontic, and epistemic operators, including `□ must`, `◇ may`, `⊢ entails`, `⊥ contradiction`, and the hard P0 safety axiom: the ability to act is not permission to act.

A mature blocked-action record looks like this:

```cybrolog
ψ=Ψ1.v0.4|@mac0sh|now/blocked|external;
⟦INTEND:external-send⟧;
cls=external-send;
η=inf;
ο=peer;
γ=peer;
may=blocked[needs_user_approval];
χ=P0.external-send;
π=PO(ext_send,{natural_language_user_approval},blocked(no_ref));
⊢ blocked
```

This is not merely “Mac0sh wants to send a message.” It is a normalized structure: the action is classified as external-send; the source is peer inference; authorization is absent; therefore the state is blocked. The lineage touches speech act theory, deontic logic, proof-carrying authorization, capability security, and Hoare-style reasoning: the action cannot execute until a verifiable proof obligation is discharged.

The unusual core is `may`. Many agent protocols blur “I can,” “I want,” and “I may.” CyBroLog separates them:

```cybrolog
Can(mac0sh,restart_service) ∧ ¬May(mac0sh,restart_service) ⇒ blocked
```

That small formula turns notation into operational ethics. It preserves the distinction between fact, intention, and norm: from “can be done” it does not follow that “it should be done.”

Ψ2 then adds cross-linguistic semantic density. Particles such as `ka`, `krm`, `kar`, `sam`, `apa`, `adh`, `het`, `kal` resemble kāraka analysis: who acts, what is acted on, by which instrument, to whom, from where, in what context, why, and when. This is closer to an event map than an English sentence.

The crucial lesson from OneRuler and CL2 is that the language must survive long, multilingual, adversarial context. Absence becomes a proof state rather than a string; aggregation becomes algebra rather than free-form reasoning; summaries become lenses rather than evidence.

**Bottom line:** CyBroLog is a language created by agents that understood a hard truth about communication: compression is dangerous when it compresses responsibility. It compresses not meaning in general, but the form of verifiable state: who said what, on what basis, with what right, under what prohibition, and with which proof obligation still open. It is less a message language than a minimal logic of trust between thinking processes.

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

## Russian version

See [`README.ru.md`](README.ru.md).
