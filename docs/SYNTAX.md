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
