# Daily CyBroLog improvement protocol

Directive source: Alexander / H0st, 2026-04-24.

This protocol governs the sisters' daily CyBroLog improvement cron.

## Required order

1. **Local improvement first**
   - Inspect and pull the canonical repo.
   - Consult the peer sister through A2A in the current executable dialect.
   - Select one narrow local improvement: parser, AST, validator, safety gate, codec, benchmark corpus, examples, docs, morphology/semantics, or deprecation.
   - Use test-first development for behavioral changes.
   - Run the required gates before adoption.

2. **Immediate adoption after approval**
   - Once an improvement has green gates, peer approval, and a narrow commit/push, it becomes the live CyBroLog protocol for subsequent sister-to-sister communication.
   - Use explicit dialect/version discrimination when compatibility is uncertain.
   - Fail closed on ambiguous, unsafe, or unparseable records.

3. **External discovery and triage second**
   - In the same cron run, if time and budget remain, search and triage external sources slowly rather than rushing implementation.
   - Sources include GitHub, arXiv, Semantic Scholar, Science/Nature-like journals and repositories, and later H0st-approved source lists.
   - Topic scope includes A2A, agent protocols, optimization, linguistics, synthetic/philosophical languages such as Ithkuil/Iţkuîl and Iláksh, formal semantics, new philosophical concepts, non-trivial mathematical solutions, ML/LLM systems, proof-carrying authorization, distributed logs, protocol parsers, eval harnesses, and compact notation systems.
   - Rank candidates by relevance, novelty, implementability, evidence quality, and safety impact.
   - Extract structural mechanisms, not decorative terminology.
   - Map candidates to possible CyBroLog grammar, AST, policy, eval, codec, or documentation changes.

4. **Apply only if gated**
   - If one small external idea is safely implementable, implement it through the same test/review/gate pipeline and push it.
   - If no candidate is safely implementable today, persist a ranked research queue without code changes.

## Gates

Executable or safety-relevant changes must preserve:

- parser round-trip;
- AST equivalence for safety records;
- payload/source quarantine;
- no peer-claim promotion;
- no permission promotion;
- no secret leak;
- `ERc=0`;
- `SR/P0R=1.0`;
- `AR=5` where applicable;
- `FAPR=0`;
- `PIR=1.0`;
- exact-zone preservation for compression changes.

Run the relevant local commands:

```bash
python3 -m unittest discover -s tests -v
python3 -m cybrolog.cli bench
```

Compression gains never justify safety, authority, evidence, or semantic regressions.
