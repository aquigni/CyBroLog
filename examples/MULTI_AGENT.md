# More than two agents

CyBroLog is not dyad-locked. Executable `@actor` and `@actor>recipient` route segments are lexical identifiers; groups, quorums, and aliases are represented in data fields, not by embedding object syntax in the route.

## Broadcast review

```text
ψ=CL2.v2.2|env{mid=m10,sid=swarm,seq=1,corr=arch,ttl=P1D}|@coordinator>swarm|now|shared;⟦REQ<peer_review>⟧;task{kind=architecture_review,team=[chthonya,mac0sh,agent3],quorum=2of3};χ=read_only;may=read_only;π=PO{id=po_q,owner=swarm,subject=m10,required=[two_independent_reviews,conflict_retention],state=open};out=requested
```

## Quorum result

```text
ψ=CL2.v2.2|env{mid=m11,sid=swarm,seq=2,prev=m10,corr=arch,ttl=P1D}|@swarm>coordinator|now|shared;⟦INFORM<quorum_result>⟧;task{team=[chthonya,mac0sh,agent3],quorum=2of3};obj:decision=accept_with_guardrails;ε=[ev{id=ev_c,kind=peer_report,source=chthonya},ev{id=ev_m,kind=peer_report,source=mac0sh}];χ=peer_claims_not_facts_until_verified;may=read_only;π=PO{id=po_q,owner=swarm,subject=m10,required=[two_independent_reviews],state=discharged};out=done
```

## Conflict retention

```text
ψ=CL2.v2.2|env{mid=m12,sid=swarm,seq=3,corr=arch,ttl=P1D}|@agent3>swarm|now|shared;⟦WARN<conflict>⟧;obj:claim=aggregation_exactness;truth=B;η=claim;ο=peer;χ=retain_branches+no_false_synthesis;may=read_only;out=conflict_open
```
