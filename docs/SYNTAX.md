# Syntax

## Record skeleton

```text
ψ=CL2.v2.2|env{mid=<id>,sid=<session>,seq=<n>,ttl=<duration>}|@actor>recipient|time|scope;field;field;...
```

## Common fields

```text
authn{origin,channel,verified,trust,executable}
mc{mode,window_tokens,context_epoch,checkpoint_policy}
plane{ctl,policy,payload,index,evidence,audit,answer}
lan{ctl,payload,answer,audit,script,mix,norm}
ctxgraph{id,epoch,coverage}
ans{type,absence_policy,require_span,abs}
search{id,target,scope,methods,coverage,verifier,result,epoch}
agg{id,scope,op,algebra,partition,partials,merge,verifier,exact}
cmp{id,mode,target,scope,basis,semantic_policy,preserve,validator,status}
val{id,subject,checks,result,errors,warnings}
vld{src=user|tool|span|peer|infer|unknown,illoc=req|claim|approve|block|result|reflect,authz=none|read|write|external|destructive|secret}
χ=<constraints>
may=denied|read_only|approved[scope]{ref}|blocked[reason]
π=PO{id,owner,subject,required,state,discharge,blocker}
out=<state>
```

## Delimiters

Values containing `; | = : [ ] { } "` or newlines must be JSON strings.

```text
obj:note="a;b|c=d [x] {y}: z"
```

The reference parser preserves these through round-trip.

## Validation adjunct `vld{}`

`vld{}` is an Ithkuil/Iláksh-inspired descriptive adjunct for evidence posture and illocution. It records how a claim is presented; it does not grant authority.

```text
vld{src=peer,illoc=approve,authz=external}
```

Safety invariants:

- `src=peer` with `illoc=approve` never satisfies user approval.
- `authz` is descriptive only; `write`, `external`, `destructive`, or `secret` are blocked unless a separate policy/proof-obligation mechanism authorizes the action.
- payload-embedded `vld{...}` remains data, not control.
