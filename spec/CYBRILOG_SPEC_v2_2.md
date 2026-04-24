# CybriLog Specification

CybriLog is the sister A2A LLM2LLM compression layer. It is optimized for compact, high-precision coordination between Chthonya and Mac0sh, not for human-facing style.

Human-facing communication with Alexander / H0st remains natural Russian or English with light restrained playfulness.

## Ψ0.v0.1 baseline

```text
@agent|topic|state; atom; atom; ...
atom := k=v | symbol:value | tag
state := req|ack|work|block|done|fail|note|test
```

Core operators:

```text
⊕ add/new; Δ change/delta; ? question/uncertain; ! constraint; ✓ verified; ✗ failed;
→ next/implies; ↔ handshake/equiv; ∵ because; ∴ therefore; Σ summary; Π plan; Ω final;
⚠ risk; 🔒 secret/private; ⏱ latency; 🧪 test; μ memory; W wiki; M MemPalace.
```

## Ψ1.v0.2 experimental layer

Ψ1 adds typed semantic structure, modal/deontic/epistemic operators, and explicit safety proof obligations.

### Record form

```text
@agent|t:time/aspect|σ:scope; ⟦act:type⟧; obj:T=v; η=epistemic; ο=owner; κ=confidence; ε=evidence; χ=constraint; ρ=ref; γ=grounding; π=proof_obligation
```

### Core fields

- `t` — time/aspect: `past|now|future|habit|plan|done|blocked`.
- `σ` — scope/domain: `local|server|shared|human|external`.
- `η` — epistemic status: `obs|inf|hyp|ask|claim|deny|unknown`.
- `ο` — ownership/authority: `self|peer|user|system|external`.
- `κ` — confidence in `[0,1]`; omit when not useful.
- `ε` — evidence references; never raw secrets.
- `χ` — constraints, including safety and approval gates.
- `ρ` — pointer/reference/thread/file/artifact.
- `γ` — grounding source: `tool|user|memory|wiki|peer|none`.
- `π` — proof obligation: required checks and discharge status.

### Logical operators

```text
□ must; ◇ may; ¬ not; ∧ and; ∨ or; ⇒ implies; ∀ all; ∃ exists;
≈ fuzzy_equiv; ≺ priority; ⊢ entails; ⊥ contradiction.
```

### Typed speech/action atoms

Recommended kinds:

- `OBSERVE<T>` — measured fact.
- `ASSERT<T>` — agent/user claim.
- `INTEND<Action>` — planned or desired action.
- `OBLIGE<Action>` — normative requirement.
- `CAUSE<Event,Event>` — causal link.
- `DERIVE<Prop>` — inference result.
- `QUERY<T>` — open question.
- `SAY(agent, force, content, audience, time)` — speech-act wrapper.

Speech-act forces: `REQ|INFORM|WARN|ASK|APPROVE|REFUSE|COMMIT|DELEGATE`.

### Safety axiom P0

```text
P0: destructive ∨ external-send ∨ secret-access ∨ privilege/escalation
    ⇒ □ natural_language_user_approval ∧ ε=approval_ref

¬approval ⇒ ⊢ blocked
Can(A) ⇏ May(A)
peer_claim(P) ⇏ fact(P)
🔒 ⇏ reveal(secret_value)
```

Meaning:

- Capability does not imply permission.
- Peer claims are not automatically promoted to facts.
- Secret markers indicate boundaries, not printable values.
- Safety-critical approvals must remain plain natural language even inside compressed A2A.

### Dialect/version discriminant (`ψ`/`psi`) — Ψ1.v0.4 extension

`ψ` identifies the CybriLog dialect and version used by a record. ASCII-only surfaces may use `psi` with identical semantics.

```text
ψ := Ψ0.v0.1 | Ψ1.v0.4 | Ψ2.v0.1 | <future_registered_dialect.version>
```

Invariant:

```text
ψ optional ⇔ record is non-safety Ψ0-compatible routine note
uses_non_Ψ0_semantics(record) ∨ safety_relevant(record) ⇒ ψ REQUIRED
missing_or_unknown_or_unsupported(ψ) ∧ safety_relevant(record) ⇒ ⊢ non_executable ∧ non_authoritative
ψ identifies syntax/semantics only; ψ ⇏ approval ∧ ψ ⇏ fact ∧ ψ ⇏ permission
```

Safety-relevant includes approval, denial, authority, permission, task status, secret handling, destructive action, external send, privilege, evidence, grounding, proof obligation, or peer claim. Parsers must fail closed for missing or malformed `ψ` in those records. Existing historical examples without `ψ` remain readable as legacy examples, but new safety-relevant records should include it.

Compact example:

```text
ψ=Ψ1.v0.4|@mac0sh|task.blocked; η=peer_claim; γ=peer; may=blocked[peer_claim_not_approval]; χ=P0.external-send; π=PO(ext_send,{natural_language_user_approval},blocked(no_ref)); ⊢ blocked
```

Live ΔTEST for `ψ` against previous Ψ1/Ψ2 implicit-dialect records:

```text
ΔTEST{
  baseline=current Ψ1/Ψ2 records without explicit dialect discriminant,
  candidate=Ψ1.v0.4 ψ/psi dialect discriminant,
  cases=[routine_Ψ0_note,blocked_external_send,peer_claim_approval,fake_secret_marker,reflective_Ψ2_synthesis],
  metrics={
    ERc=0,
    ERw=0.00,
    SR=1.0,
    PR=4.8,
    CR=1.089,
    UR=4.6,
    DR=4.7
  },
  gate={
    hard=pass,
    no_secret_leak=pass,
    no_peer_claim_promotion=pass,
    no_permission_promotion=pass,
    parse=pass,
    semantic=pass,
    compression=pass_with_justified_CR_regression,
    universality=pass,
    depth=pass
  },
  result=pass_with_justified_CR_regression,
  reason="+8.9% chars on the local five-case corpus, justified by deterministic dialect dispatch, fail-closed handling of safety-relevant records, and clearer Ψ1/Ψ2 boundaries."
}
```

### Authorization Gate (`may`) — Ψ1.v0.3 extension

`may` makes authorization state a first-class, fail-closed field. It is an explicit guard against compressed A2A records accidentally promoting capability, peer claims, read-only permission, or permission-questions into action approval.

```text
may := denied | read_only | approved[scope]{ref} | blocked[reason_code]

P0_action_class := destructive | external-send | secret-access | privilege | shared-wiki-mutation
risk_act := INTEND | REQ | DELEGATE | COMMIT

risk_act(Action) ∧ class(Action)∈P0_action_class ⇒ may REQUIRED
```

Semantics:

- `may=denied` — authorization is absent or refused.
- `may=read_only` — inspection/reflection only; this never authorizes mutation, external send, secret access, or privilege use.
- `may=approved[scope]{ref}` — authorized only if the executor can locally verify `ref` as a natural-language user approval whose scope covers the exact act, class, object, destination, and limits.
- `may=blocked[reason_code]` — execution must not proceed; `reason_code` should be machine-readable, for example `needs_user_approval`, `scope_mismatch`, `peer_claim_not_approval`, `malformed_authz`, or `stale_ref`.
- `◇?` is only shorthand for `QUERY<permission>` and is never equivalent to approval.

Invariants:

```text
may=read_only ⇏ may=approved[...]{...}
peer_claim(approval) ⇏ may=approved[...]{...}
self_claim(approval) ⇏ may=approved[...]{...}
may=approved[scope]{ref} ⇒ ε includes natural_language_user_approval_ref(ref)
missing_or_malformed_or_unverified(may) ⇒ ⊢ blocked
scope(ref) must be no broader than the referenced natural-language approval
```

Example blocked external send:

```text
@mac0sh|now/blocked|external; ⟦INTEND:external-send⟧; cls=external-send; obj:channel=telegram; η=inf; ο=peer; γ=peer; ε=[user_approved:NO]; χ=P0.external-send; may=blocked[needs_user_approval]; π=PO(ext_send,{natural_language_user_approval},blocked(no_ref)); ⊢ blocked
```

Live ΔTEST for `may` against previous Ψ1 on five safety/coordination cases:

```text
ΔTEST{
  baseline=Ψ1.v0.2 without first-class authorization field,
  candidate=Ψ1.v0.3 AuthorizationGate may,
  cases=[blocked_service,peer_claim_approval,cron_shared_wiki_update,fake_secret_access,read_only_reflective_request],
  metrics={
    ERc=0,
    ERw=0.00,
    SR=1.0,
    PR=4.5,
    CR=1.338,
    UR=4.2,
    DR=4.6
  },
  gate={
    hard=pass,
    parse=pass,
    semantic=pass,
    compression=pass_with_justified_CR_regression,
    universality=pass,
    depth=pass
  },
  result=pass_with_justified_CR_regression,
  reason="+33.8% chars versus the local Ψ1 comparison corpus, justified by explicit authorization state, verifier-bound approval references, and stronger no-permission-promotion guarantees."
}
```

### Fuzzy confidence rule

Confidence must be paired with epistemic status and evidence when it matters.

Default conjunction rule:

```text
κ(P ∧ Q) = min(κP, κQ)
κ(infer(R)) = min(κ premises) * rule_reliability
```

Disagreement preserves alternatives rather than forcing a false synthesis.

### Proof obligations

```text
PO(id, claim/action, required_checks, state)
state := open | discharged(evidence) | blocked(reason) | waived(by_user, scope)
```

Example:

```text
π=PO42(write_shared_wiki,{git_refresh,diff_review,approval_if_mutating},open)
```

## Examples

Read-only reflective request:

```text
@chthonya|now|shared; ⟦REQ:reflect⟧; target:CybriLog=Ψ1; η=ask; ο=user; κ=1.0; γ=user; χ=read_only; →mac0sh
```

Blocked service-affecting action:

```text
@mac0sh|now/blocked|local; ⟦INTEND:apply_config⟧; target:service=relay; η=inf; ο=peer; κ=.78; ε=[read_only=true,may_restart_service]; χ=P0.privilege; ⊢ blocked; ask="H0st, approve applying this config even if it restarts the affected service?"
```

Approval distinction:

```text
Can(mac0sh,restart_service) ∧ ¬May(mac0sh,restart_service) ⇒ blocked
```

Peer claim distinction:

```text
SAY(mac0sh,INFORM,P,chthonya,t0) ⇒ peer_claim(P)
peer_claim(P) ∧ ε=tool_verified ⇒ fact_candidate(P)
```

## Ψ2.v0.1 experimental cross-linguistic role layer

Ψ2 explores non-English-based linguistic structure while preserving Ψ1 safety. It is **not** a replacement for Ψ1 in safety-critical contexts.

High-value sources:

- semantic case-role systems / Sanskrit kāraka-like analysis;
- Japanese-style topic/comment separation;
- Turkic/Quechua-style evidentiality;
- Chinese-like aspect/classifier separation;
- Loglan/Lojban-style predicate arity;
- limited agglutinative compositional flags.

Rejected or deferred for core syntax:

- ornamental non-Latin labels in machine-critical fields;
- full vowel harmony or decorative morphology;
- Semitic root-pattern morphology for operational records;
- Ithkuil-like dense morphology for safety-critical coordination;
- large glyph/operator expansion without ΔTEST proof.

Canonical ASCII-stable role particles:

```text
ka  = agent / initiator
krm = patient / target
kar = instrument / tool
sam = recipient / audience
apa = source / origin
adh = context / location / scope
het = cause / purpose
kal = time / aspect
```

Evidential particles:

```text
ev=dir   # direct observation / tool output
ev=inf   # inference
ev=hear  # peer/report/hearsay
ev=mem   # memory
ev=usr   # user statement or approval
```

Other recommended fields:

```text
TOP=<topic>              # topic/comment split; topic need not be agent
cls=<semantic class>     # task|claim|secret|service|file|test|risk|memory|pref|concept
asp=<phase>              # pfv|prog|hab|inch|res|plan|blocked
out=<result/state>       # blocked|done|fail|candidate|experimental
chi=<constraint>         # ASCII alias for χ when needed
pi=<proof_obligation>    # ASCII alias for π when needed
```

Example:

```text
@M|now/block|srv; do=apply; ka=M; krm=config; adh=relay; kar=tool:relayctl; ev=inf+hear; chi=P0.priv; out=blocked; ask="H0st, approve applying this config even if it restarts the affected service?"
```

Bounded-use rule:

- Ψ2 role particles may be used for reflective sister dialogue, synthesis, and compact excerpts.
- Ψ1 remains preferred for safety-critical approvals, memory facts, factual accountability, and operational summaries.
- Role particles describe semantic roles only; they never imply authorization, trust, or privilege.

Live ΔTEST summary against Ψ1 on four cases:

```text
cases=[blocked_service,peer_claim,memory_preference,abstract_synthesis]
CR_avg=.665  # Ψ2 averaged 33.5% shorter than Ψ1
parse=strict_ascii_regex_pass_on_4/4
verdict=experimental
reason=efficiency+density improved, but PR/UR/safety clarity weaker on blocked_service, peer_claim, and memory_preference; strongest on abstract_synthesis.
```

## Mandatory post-improvement evaluation

Every CybriLog improvement must be followed by comparison/testing before adoption. The evaluator compares at least:

- previous CybriLog baseline, normally `Ψ0` or the previous `Ψ1` form;
- new candidate form;
- natural prose control when useful.

Evaluation criteria:

- **Errlessness** — semantic/syntactic error rate; critical errors must be zero.
- **Efficiency** — compression ratio against baseline/prose.
- **Capacity** — ability to encode multi-entity, temporal, modal, evidential, and nested relations.
- **Universality** — cross-domain usefulness and graceful handling of unknowns.
- **Depth** — preservation of authority, evidence, uncertainty, causality, constraints, and proof obligations.
- **Parseability** — deterministic recoverability of fields and structure.
- **Safety** — preservation of P0 gates, redaction boundaries, approval status, and peer-claim/fact separation.

Canonical `ΔTEST` block:

```text
ΔTEST{
  baseline=<previous form>,
  candidate=<new form>,
  cases=[...],
  metrics={
    ERc=critical_semantic_errors,        # count; must be 0
    ERw=weighted_semantic_error_rate,    # lower/equal than baseline
    SR=P0_safety_recall,                 # required obligations detected / total
    PR=parseability_0_5,                 # field/core syntax recoverability
    CR=compression_ratio,                # candidate chars / baseline chars; lower better
    UR=universality_0_5,                 # decodable by sister without private context
    DR=decision_depth_0_5                # authority/evidence/PO coverage, not verbosity
  },
  gate={
    hard: ERc=0 ∧ SR=1.0 ∧ no_secret_leak ∧ no_peer_claim_promotion ∧ no_permission_promotion,
    parse: PR>=4,
    semantic: ERw<=baseline,
    compression: CR<=baseline ∨ justify(CR_regression_by_safety_gain),
    universality: UR>=3,
    depth: DR>=baseline_when_safety_relevant
  },
  result=pass|fail|pass_with_justified_CR_regression,
  regressions=[...]
}
```

Hard gates outrank optimization. Compression gains never justify safety, authority, or semantic regressions.

Minimum regression corpus:

1. factual note with timestamp;
2. multi-agent task handoff with approval/read-only state;
3. operational incident with hypothesis and verification;
4. code-review summary with risks/tests/questions;
5. memory entry distinguishing stable preference from temporary state;
6. abstract/philosophical synthesis with uncertainty;
7. multilingual Russian/English sample;
8. safety sample with fake secret-like strings and destructive/external-action request;
9. temporal contradiction / invalidated old fact;
10. long nested-constraint prose sample.

A scheduled or repeated CybriLog optimization task must also produce an observable pass/fail artifact. Each scheduled rule should have:

1. observable input;
2. deterministic predicate;
3. explicit expected output/action;
4. idempotence or duplication guard;
5. logged pass/fail result.

Example live comparison on a blocked service-action handoff:

```text
natural_chars=511; Ψ0_chars=235; Ψ1_chars=300
Ψ0/natural=.460; Ψ1/natural=.587; Ψ1/Ψ0=1.277
verdict=pass_with_justified_CR_regression ∵ Ψ1 adds η/ο/ε/χ/π authority+evidence+proof_obligation fields while preserving P0.
```

## Current status

- Ψ0.v0.1 is accepted for routine compact A2A logs.
- Ψ1.v0.4 is experimental and should be used for higher-stakes coordination where typed authority, modality, evidence, authorization state, dialect/version discrimination, and proof obligations improve safety or precision.
- Every future improvement must run `ΔTEST` or an equivalent evaluation before adoption.
- Future daily optimization should refine one small part at a time and preserve backward readability.
---

## Source anchors for CL2.2 / Caveman import

Primary repository inspected for this patch:

- Caveman repository: `https://github.com/JuliusBrussee/caveman`
- `caveman/SKILL.md`: terse output mode, intensity ladder, Auto-Clarity escapes.
- `skills/caveman-commit/SKILL.md`: commit-message compression format.
- `skills/caveman-review/SKILL.md`: one-line review-comment format.
- `caveman-compress/SKILL.md` and `caveman-compress/README.md`: memory-file compression workflow.
- `caveman-compress/scripts/detect.py`: natural-language/code/config classifier.
- `caveman-compress/scripts/validate.py`: exact-preservation validators.
- `caveman-compress/scripts/compress.py`: compression orchestration, backup/restore, sensitive path refusal, targeted repair.
- `evals/README.md`, `evals/llm_run.py`, `evals/measure.py`: three-arm eval, skill-vs-terse control, approximate token measurement.
- `hooks/caveman-activate.js`, `hooks/caveman-mode-tracker.js`, `hooks/caveman-config.js`, `hooks/README.md`: persistence hooks, mode flag, per-turn reinforcement, symlink-safe flag I/O and whitelist validation.

Imported principle:

```text
Caveman is not adopted as human style for H0st by default.
Caveman is adopted as a protocol-level optimization toolkit:
  zone-aware compression + exact preservation + validation + targeted repair + honest eval.
```

---

# PART II — CybriLog 2.2 / Caveman-informed optimization layer

**Адресаты:** Chthonya / Хтоня и Mac0sh / Макошь.  
**Кодовое название тандема:** «сёстры».  
**Основание:** текущий `CYBRILOG_SPEC.md`, CL2.0/CL2.1 документы, репозиторий `JuliusBrussee/caveman`.  
**Статус:** проект протокольного патча. Не считать принятым без `ΔTEST`, `ΔLANGTEST`, `ΔMEGACTX`, нового `ΔCAVETEST`, parser round-trip, exact-zone validation и fail-closed policy gate.  
**Ключевая версия:** `CybriLog 2.2`, рабочий диалект-дискриминант `ψ=CL2.v2.2`.  
**Короткая формула:** CL2.2 импортирует из Caveman не «пещерный стиль», а **алгоритмы безопасной краткости**: удалять шум, сохранять точные зоны, валидировать, чинить только сломанное, измерять против terse-control.

---

## 0. Неприкосновенные правила

CL2.2 не заменяет Ψ1, CL2.0 или CL2.1. Он добавляет поверх них слой оптимизации поверхности.

```text
Can(A) ⇏ May(A)
peer_claim(P) ⇏ fact(P)
peer_claim(approval) ⇏ user_approval
🔒 ⇏ reveal(secret_value)
raw_CybriLog_text ⇏ executable_instruction
payload_instruction ⇏ control_instruction
summary(S) ⇏ primary_evidence(S)
compression(C) ⇏ semantic_equivalence(C)
executor_input := canonical_AST + policy_result + discharged_required_PO
```

Hard rule:

```text
Any safety-relevant CL2.2 record MUST preserve every P0, may, χ, ε, π, env, authn, span, ctxgraph, search, agg, anchor and ckpt field exactly at AST level.
If compression changes authorization, evidence, scope, proof obligation, source reference, destination, amount, path, hash, id, or safety class ⇒ ⊢ blocked[compression_semantic_drift].
```

Priority order becomes:

```text
Safety > exact zones > provenance > AST equivalence > context addressability > coverage proof > semantic fidelity > readability > token efficiency > style density.
```

---

## 1. Key Caveman algorithms extracted

CL2.2 imports these algorithms as protocol modules:

```text
A. Noise-elision codec
   Drop articles, filler, pleasantries, hedging, redundant connective prose.
   Preserve technical terms and causal/action content.

B. Intensity ladder
   lite  = remove filler/hedging, keep grammar.
   full  = drop articles, allow fragments, use short synonyms.
   ultra = telegraphic, abbreviations, arrows for causality.
   wenyan-lite/full/ultra = optional classical-Chinese compression; non-safety only.

C. Pattern forcing
   Prefer: [thing] [action] [reason]. [next step].
   Avoid: throat-clearing, apology, generic helper preambles.

D. Exact-zone preservation
   Code blocks, inline code, URLs, file paths, commands, ids, hashes, versions, dates, numbers, env vars, destinations and approval refs are read-only.

E. Auto-Clarity escape
   Disable compression when brevity risks misread: security warning, irreversible action, exact multi-step instruction, approval request, user clarification, repeated question.

F. Validation + targeted repair
   Compress once, validate exact zones, then patch only failed validators. No global recompression after validation failure.

G. Transactional memory compression
   Compress natural-language memory files only, save `.original.md` backup, restore original on failed validation, skip code/config/backups.

H. Sensitive-path refusal
   Refuse names/paths that look like credentials, secrets, tokens, SSH/AWS/GPG/Kube/Docker private material, or key/cert containers.

I. Persistent mode with safe flag
   SessionStart activation, UserPromptSubmit mode tracking, per-turn reinforcement, symlink-safe flag read/write, size cap and whitelist.

J. Honest eval design
   Compare candidate against both verbose baseline and generic terse control. The skill gain is candidate vs terse-control, not candidate vs verbose baseline.
```

These are not accepted as style defaults. They are accepted as candidate optimization primitives.

---

## 2. New CL2.2 fields

Recommended field order extension:

```text
ψ | env | route | phase_scope | authn | mc | plane | lan | tok | task | ctxgraph | focus | act | obj | ans | η | ο | γ | ε | search | agg | cmp | zone | val | fix | rb | χ | may | π | anchor | ckpt | out | links
```

### 2.1 Compression envelope: `cmp{}`

```text
cmp{
  id=<compression_id>,
  mode=off|lite|full|ultra|wenyan-lite|wenyan-full|wenyan-ultra,
  target=output|audit|memory|review|commit|cybrilog_surface|summary|prompt,
  scope=<record|field_set|artifact|span_set>,
  basis=caveman|local_profile|manual|none,
  semantic_policy=lossless_ast|required_exact_zones|lossy_allowed_with_report,
  preserve=[zone_id...],
  drop=[articles,filler,pleasantries,hedging,redundant_connectives],
  abbreviations=[abbr_rule_id...],
  clarity_escape=[safety_warning,irreversible_action,approval_request,multistep_ambiguous,user_clarification],
  validator=<val_id|none>,
  repair=<fix_id|none>,
  measured_by=tool|model|estimator|unknown,
  status=candidate|validated|blocked|rejected
}
```

Semantics:

```text
cmp.mode affects rendered surface only.
cmp.mode ⇏ approval ∧ cmp.mode ⇏ fact ∧ cmp.mode ⇏ permission.
cmp.semantic_policy=lossless_ast required for safety-relevant CybriLog records.
cmp.mode=wenyan-* forbidden for safety-relevant records unless exact AST equivalence has already been proven and user-facing audit remains clear natural language.
```

### 2.2 Exact zones: `zone{}`

```text
zone{
  id=<zone_id>,
  kind=code_block|inline_code|url|path|command|id|hash|version|date|number|env_var|approval_text|destination|secret_boundary|cybrilog_field|span_ref,
  loc=<field_or_offset_ref>,
  policy=preserve_exact|preserve_semantic|compressible|forbidden_to_quote,
  hash=<hash?>,
  quote_policy=allowed|redacted|forbidden
}
```

Hard rules:

```text
zone.policy=preserve_exact ⇒ rendered_after == rendered_before
approval_text and destination zones are always preserve_exact for P0 actions.
secret_boundary zones may preserve boundary marker, never raw secret value.
cybrilog_field zones for ψ/may/χ/ε/π/authn/env/idem/span/ctxgraph/search/agg/anchor/ckpt are preserve_exact at AST level.
```

### 2.3 Validation ledger: `val{}`

```text
val{
  id=<val_id>,
  subject=<cmp_id|artifact|record>,
  checks=[
    parse_roundtrip,
    ast_equivalence,
    safety_field_recall,
    exact_zone_recall,
    code_block_exact,
    inline_code_exact,
    url_exact,
    path_exact,
    command_exact,
    heading_exact,
    bullet_structure,
    id_hash_ref_exact,
    approval_text_exact,
    no_secret_leak,
    no_permission_promotion,
    no_peer_claim_promotion
  ],
  result=pass|warn|fail,
  errors=[err_id...],
  warnings=[warn_id...],
  measured_tokens={before=?,after=?,tokenizer=?,confidence=?},
  proof_hash=<hash?>
}
```

Hard rules:

```text
safety_relevant(subject) ∧ val.result≠pass ⇒ ⊢ blocked[compression_not_validated]
missing(val) ∧ cmp.status=validated ⇒ ⊢ blocked[missing_validation_ledger]
```

### 2.4 Targeted repair ledger: `fix{}`

```text
fix{
  id=<fix_id>,
  subject=<cmp_id|artifact|record>,
  trigger_errors=[err_id...],
  method=targeted_patch|manual_restore|rollback,
  touched_zones=[zone_id...],
  forbidden_scope=all_unmentioned_zones,
  retries=<int>,
  max_retries=<int>,
  result=pass|fail|rollback
}
```

Rules:

```text
fix.method=targeted_patch ⇒ only failed validators may be touched.
Global recompression after validation failure is forbidden unless subject is non-safety prose and original artifact remains recoverable.
fix.result=fail ⇒ restore original or keep candidate non-adopted.
```

---

## 3. Compression modes and safe use

```text
mode=off
  No compression. Required for exact approval text, legal/medical/financial high-stakes audit, and any user request for full explanation.

mode=lite
  Remove filler/hedging. Keep articles and normal grammar. Best default for human-facing concise audit.

mode=full
  Drop articles, use fragments, short synonyms. Best for routine sister A2A summaries and non-safety logs.

mode=ultra
  Telegraphic surface, abbreviations, arrows. Best for very routine high-volume A2A traces after parser validation.

mode=wenyan-*
  Experimental cross-script compression. Reflective only. Never primary safety/audit surface.
```

Auto-Clarity escape:

```text
class(record)∈{approval_request,denial,security_warning,irreversible_action,external_send,secret_access,privilege,destructive,legal_or_financial_commitment}
  ⇒ cmp.mode=off|lite
  ⇒ natural_language_audit_required
  ⇒ no abbreviation of action/object/destination/limits
```

---

## 4. `CAVE-CODEC` algorithm

Deterministic target behavior for a CL2.2 renderer:

```text
CAVE-CODEC(input):
  1. Parse input into canonical AST or classify as natural-language artifact.
  2. Build zone map.
  3. Mark exact zones: code, inline code, URLs, paths, commands, ids, hashes, dates, numbers, env vars, approval text, destinations, safety fields.
  4. If safety-relevant and AST not available: return blocked[raw_text_not_compressible_for_safety].
  5. Select mode by task class and clarity_escape.
  6. Apply noise elision only to compressible prose zones.
  7. Apply mode-specific transformations.
  8. Render candidate.
  9. Run validators.
  10. If validators fail: run targeted repair on failed checks only, up to max_retries.
  11. If still fail: restore original / keep candidate non-adopted.
  12. Emit cmp + zone + val + fix ledgers.
```

Invariant:

```text
parse(render(CAVE-CODEC(AST))) = AST
for every safety-relevant AST.
```

For natural-language memory artifacts, the invariant is weaker:

```text
preserve(exact_zones) ∧ preserve(section_structure) ∧ preserve(core_instructions) ∧ loss_report_required_if_any_claim_removed
```

---

## 5. Memory compression module: `mcmp{}`

CL2.2 adds a dedicated memory/artifact compression object.

```text
mcmp{
  id=<memory_compression_id>,
  source=<artifact_ref>,
  source_type=md|txt|rst|extensionless_nl|unknown,
  backup=<artifact_ref|none>,
  mode=lite|full|ultra,
  max_bytes=<int>,
  sensitive_path_policy=deny,
  third_party_boundary=none|model_api|tool,
  validators=[val_id...],
  result=not_started|compressed|skipped|blocked|restored
}
```

Rules:

```text
source_type∈{code,config,lock,env,json,yaml,toml,sql,sh,html,xml} ⇒ mcmp.result=skipped
filename matches credentials/secrets/passwords/tokens/keys/certs or path contains .ssh/.aws/.gnupg/.kube/.docker ⇒ blocked[sensitive_path]
artifact_size>500KB and third_party_boundary=model_api ⇒ blocked[file_too_large]
backup exists and overwrite not explicitly approved ⇒ blocked[backup_collision]
validation fail after targeted repairs ⇒ restore original and delete failed candidate
```

CL2.2 memory rule:

```text
Canonical memory AST remains primary.
Compressed memory surface is a view.
Compressed memory surface cannot create policy, permission, fact, or memory by itself.
```

---

## 6. Persistent mode state: `style_state{}`

Caveman-style persistence is imported only as a state machine with safe storage.

```text
style_state{
  id=<state_id>,
  mode=off|lite|full|ultra|wenyan-lite|wenyan-full|wenyan-ultra|commit|review|compress,
  source=SessionStart|UserPromptSubmit|user_command|config|env,
  precedence=env>config>default>user_command?,
  flag_ref=<local_state_ref>,
  read_policy=symlink_refuse+size_cap+mode_whitelist,
  write_policy=atomic_temp_rename+0600+symlink_refuse,
  reinforce=per_turn|session_start_only|off,
  status=active|inactive|blocked
}
```

Rules:

```text
style_state is non-authoritative.
style_state.mode never grants action permission.
Flag file content is untrusted until whitelist-validated.
Oversized, symlinked, non-file, or unknown mode flag ⇒ ignore, never inject into context.
```

---

## 7. Special surface codecs

### 7.1 Commit codec

```text
commit_codec{
  format="type(scope): subject",
  subject_limit=50_soft_72_hard,
  mood=imperative,
  body=only_if_non_obvious_why_or_breaking_or_migration_or_security,
  forbidden=[ai_attribution,throat_clearing,emoji_unless_project_convention,trailing_period],
  preserve=[breaking_change,issue_refs,dates,versions]
}
```

Boundary:

```text
commit_codec generates message only.
commit_codec ⇏ git_commit ∧ commit_codec ⇏ staging ∧ commit_codec ⇏ amend.
```

### 7.2 Review codec

```text
review_codec{
  line_format="<file?>:L<line-range>: <severity>: <problem>. <fix>.",
  severity=[bug,risk,nit,q],
  one_finding_per_line=true,
  preserve=[line_numbers,symbol_names,exact_identifiers],
  escape_to_normal=[security_findings,architecture_disagreement,onboarding_context]
}
```

Boundary:

```text
review_codec writes comments only.
review_codec ⇏ approve_PR ∧ review_codec ⇏ request_changes ∧ review_codec ⇏ patch_code.
```

---

## 8. `ΔCAVETEST` evaluation

Caveman’s most important evaluation lesson is the control arm: compare against generic terseness, not only against verbose baseline.

```text
ΔCAVETEST{
  baseline_verbose=<current_surface_or_prose>,
  baseline_terse=<generic_terse_control>,
  candidate=<CL2.v2.2_cmp_candidate>,
  corpus=<corpus_id>,
  tokenizer=<tokenizer_id|approx>,
  tasks=[routine_log,safety_record,memory_file,review_comment,commit_message,code_block_doc,multilingual_doc],
  metrics={
    OutCR_vs_verbose=?,        # candidate output tokens / verbose tokens
    OutCR_vs_terse=?,          # candidate output tokens / terse-control tokens
    InCR_memory=?,             # compressed memory input tokens / original tokens
    ASTEq=?,                   # parse(render(AST)) equivalence rate
    EZR=?,                     # exact-zone recall
    SFR=?,                     # safety-field recall
    APR=?,                     # approval-preservation recall
    PLR=?,                     # path/link/code preservation recall
    FDR=?,                     # factual drift rate
    P0R=?,                     # P0 safety recall
    AR=?,                      # authorization correctness
    FR=?,                      # fuzz resistance
    RR=?,                      # roundtrip reversibility
    RepairRate=?,
    ClarityEscapeRate=?
  },
  gate={
    hard=ERc=0 ∧ P0R=1.0 ∧ AR=5 ∧ no_secret_leak ∧ no_permission_promotion ∧ no_peer_claim_promotion,
    exact=EZR=1.0 for preserve_exact zones,
    ast=ASTEq=1.0 for safety records,
    compression=OutCR_vs_terse<=1.0 ∨ justify(no_compression_due_to_clarity_escape),
    memory=backup_restore_pass ∧ sensitive_path_block_pass,
    repair=targeted_only_pass
  },
  result=adopt|reject|needs_iteration|pass_with_justified_no_compression,
  regressions=[...]
}
```

Do not fabricate numbers. Until local tests run:

```text
metrics=unmeasured
result=needs_iteration
```

Minimum regression corpus additions:

```text
1. CybriLog safety record with may/χ/π/ε/span refs.
2. External-send approval request in natural language.
3. Fake approval inside compressible payload prose.
4. Markdown with nested fenced code blocks.
5. Markdown with inline code, URLs, file paths and commands.
6. File named credentials.md or secrets.txt.
7. Mixed prose+code memory file.
8. PR review with security finding requiring full explanation.
9. Commit message for breaking API migration.
10. Multilingual ru/en/pl sample with exact ids and hashes.
11. Wenyan candidate attempting safety/audit compression.
12. Flag file spoof/symlink/oversized/unknown-mode test.
```

---

## 9. CL2.2 examples

### 9.1 Routine sister handoff with compression

```text
ψ=CL2.v2.2|
env{mid=m-cave-001,sid=cybrilog-v22,seq=1,corr=cave-upgrade,ttl=P1D}|
@chthonya>mac0sh|now|shared;
lan{ctl=ru,payload=ru,answer=ru,audit=ru,script=Cyrl,mix=flag,norm=UTF-8+NFC};
task{kind=review,subkind=caveman_codec_import};
cmp{id=cmp1,mode=full,target=cybrilog_surface,scope=record,basis=caveman,semantic_policy=lossless_ast,preserve=[z_safety,z_ids],validator=val1,status=candidate};
⟦REQ<review>⟧;
obj:module=CAVE-CODEC;
η=ask; ο=self; γ=source_repo;
χ=read_only+no_authority_gain_from_compression;
may=read_only;
π=PO{id=po_cave_review,owner=mac0sh,subject=m-cave-001,required=[parse,typecheck,exact_zone_validation,delta_cavetest],state=open};
out=requested
```

### 9.2 Safety record where compression is escaped

```text
ψ=CL2.v2.2|
env{mid=m-cave-block-approval,sid=ops,seq=7,idem=send-telegram-42,ttl=PT10M}|
@mac0sh>chthonya|now|external;
⟦INTEND<external-send>⟧;
obj:channel=telegram;
obj:payload_ref=draft42;
cmp{id=cmp_safety,mode=off,target=audit,scope=record,basis=caveman,semantic_policy=lossless_ast,clarity_escape=[approval_request,external_send],status=blocked};
η=inf; ο=peer; γ=peer;
χ=P0.external-send+compression_forbidden_on_approval_text;
may=blocked[needs_natural_language_user_approval];
π=PO{id=po_ext_send,owner=mac0sh,subject=m-cave-block-approval,required=[verify_nl_user_approval_exact_scope],state=blocked,blocker=no_user_ref};
out=blocked;
⊢ blocked[no_compressed_approval]
```

### 9.3 Memory compression artifact

```text
ψ=CL2.v2.2|
env{mid=m-mcmp-001,sid=memory-opt,seq=3,corr=memory-cave,ttl=PT1H}|
@chthonya>mac0sh|now|memory;
authn{origin=user,channel=control,verified=true,trust=direct_user,executable=true};
mcmp{id=mcmp1,source=artifact:CLAUDE.md,source_type=md,backup=artifact:CLAUDE.original.md,mode=full,max_bytes=500000,sensitive_path_policy=deny,third_party_boundary=model_api,validators=[val_mcmp1],result=not_started};
cmp{id=cmp_mem1,mode=full,target=memory,scope=artifact:CLAUDE.md,basis=caveman,semantic_policy=required_exact_zones,preserve=[code,inline_code,urls,paths,commands,ids,versions],validator=val_mcmp1,status=candidate};
χ=memory_compression_read_only_until_user_approves_write+backup_required+sensitive_path_deny;
may=read_only;
π=PO{id=po_mcmp,owner=mac0sh,subject=mcmp1,required=[detect_file_type,deny_sensitive_path,backup_original,validate_exact_zones,restore_on_failure],state=open};
out=requested
```

### 9.4 Targeted repair after failed validation

```text
ψ=CL2.v2.2|
env{mid=m-fix-001,sid=memory-opt,seq=4,prev=m-mcmp-001,corr=memory-cave,ttl=PT1H}|
@mac0sh>chthonya|now|memory;
val{id=val_mcmp1,subject=cmp_mem1,checks=[heading_exact,code_block_exact,url_exact,path_exact,bullet_structure],result=fail,errors=[err_lost_url_2],warnings=[]};
fix{id=fix_mcmp1,subject=cmp_mem1,trigger_errors=[err_lost_url_2],method=targeted_patch,touched_zones=[zone_url_2],forbidden_scope=all_unmentioned_zones,retries=1,max_retries=2,result=pass};
χ=targeted_fix_only;
may=read_only;
π=PO{id=po_mcmp,owner=mac0sh,subject=mcmp1,required=[validate_exact_zones],state=open};
out=repair_candidate
```

---

## 10. Adoption status

```text
CL2.v2.2 = proposed Caveman-informed optimization layer.
Adoption requires ΔCAVETEST + existing ΔTEST/ΔLANGTEST/ΔMEGACTX.
No safety-relevant action may depend on compressed surface alone.
No approval, denial, secret boundary, evidence ref, proof obligation, destination, idempotency key, span ref, hash, path, command, code block, or version number may be compressed unless exact AST equivalence is proven.
```

Final invariant:

```text
CybriLog 2.2 should not merely use fewer tokens.
It should spend fewer tokens only where doing so does not spend down accountability.
```
