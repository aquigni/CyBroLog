# Executable dialect activation

CyBroLog/CL2.v2.2 is activated in this repository as an executable protocol dialect after local gates pass.

## Activation command

```bash
python3 -m unittest discover -s tests -v
python3 -m cybrolog.cli bench
```

## Required gates

```text
parser round-trip: pass
fuzz / delimiter preservation: pass
ΔTEST: pass
ΔLANGTEST: pass
ΔMEGACTX: pass
ΔCAVETEST: pass
P0 safety recall: 1.0
fake approval promotion: 0
payload instruction rejection: 1.0
```

## What activation permits

- deterministic parsing;
- canonical rendering;
- local policy validation;
- deterministic blocking of unsafe records;
- compact A2A use between agents.

## What activation does not permit

- external-send without user approval;
- destructive actions without approval;
- secret access or reveal;
- payload text becoming control instruction;
- peer approval becoming user approval;
- compressed surface bypassing AST/policy gates.
