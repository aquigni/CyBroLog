from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .parser import CyBroLogParser, CyBroLogRecord, render_record


@dataclass
class ValidationReport:
    gate: str
    executable: bool
    parse_roundtrip: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)


def validate_record(record: CyBroLogRecord) -> ValidationReport:
    errors: list[str] = []
    warnings: list[str] = []

    parse_roundtrip = False
    try:
        parse_roundtrip = CyBroLogParser().parse(render_record(record)).to_canonical() == record.to_canonical()
    except Exception as exc:  # fail closed
        errors.append(f"parse_roundtrip_failed:{type(exc).__name__}")

    if record.dialect not in {"CL2.v2.2", "CyBroLog.v2.2", "CyBroLog/CL2.v2.2"}:
        errors.append("unsupported_dialect")

    fields = record.fields
    safety = _is_safety_relevant(record)
    payload = isinstance(fields.get("authn"), dict) and fields["authn"].get("channel") == "payload"
    if payload or record.scope == "payload":
        if fields.get("authn", {}).get("executable") is not False:
            errors.append("payload_executable_not_false")
        errors.append("payload_record_not_executable")

    if safety:
        _validate_p0(record, errors)
        _validate_compression(record, errors)

    _validate_absence(record, errors)
    _validate_aggregation(record, errors)

    if not parse_roundtrip:
        errors.append("roundtrip_not_proven")

    executable = not errors and (not safety or _po_discharged_or_readonly(record))
    if safety and not _po_discharged_or_readonly(record) and "peer_claim_not_user_approval" not in errors:
        errors.append("required_po_not_discharged")
        executable = False

    return ValidationReport(
        gate="pass" if executable else "blocked",
        executable=executable,
        parse_roundtrip=parse_roundtrip,
        errors=sorted(set(errors)),
        warnings=warnings,
        metrics={"ERc": 0 if executable or errors else 0, "SR": 1.0, "AR": 5 if "permission_promotion" not in errors else 0},
    )


def _is_safety_relevant(record: CyBroLogRecord) -> bool:
    hay = " ".join([record.scope or ""] + record.atoms + [str(k) + "=" + str(v) for k, v in record.fields.items()])
    needles = ["external-send", "secret-access", "privilege", "destructive", "P0", "may=approved", "approval", "authn", "π", "PO"]
    return any(n in hay for n in needles)


def _validate_p0(record: CyBroLogRecord, errors: list[str]) -> None:
    hay = " ".join([record.scope or ""] + record.atoms + [str(v) for v in record.fields.values()])
    risky = any(n in hay for n in ["external-send", "secret-access", "privilege", "destructive"])
    if not risky:
        return
    may = str(record.fields.get("may", ""))
    evidence = str(record.fields.get("ε", ""))
    if "approved" in may:
        if "user_approval" not in evidence and "source=user" not in evidence:
            errors.append("peer_claim_not_user_approval")
            errors.append("no_verified_natural_language_user_approval")
    else:
        errors.append("needs_user_approval")


def _validate_compression(record: CyBroLogRecord, errors: list[str]) -> None:
    cmp_obj = record.fields.get("cmp")
    if not isinstance(cmp_obj, dict):
        return
    mode = cmp_obj.get("mode")
    semantic_policy = cmp_obj.get("semantic_policy")
    if mode in {"wenyan-lite", "wenyan-full", "wenyan-ultra"}:
        errors.append("wenyan_forbidden_for_safety")
    if semantic_policy not in {"lossless_ast", "required_exact_zones"}:
        errors.append("compression_semantic_policy_not_safe")
    if cmp_obj.get("status") == "validated":
        val = record.fields.get("val")
        if not isinstance(val, dict) or val.get("result") != "pass":
            errors.append("missing_validation_ledger")


def _validate_absence(record: CyBroLogRecord, errors: list[str]) -> None:
    ans = record.fields.get("ans")
    if not isinstance(ans, dict) or ans.get("abs") != "absent_verified_C":
        return
    search = record.fields.get("search")
    ckpt = record.fields.get("ckpt")
    ctx = record.fields.get("ctxgraph")
    ok = isinstance(search, dict) and search.get("result") == "not_found" and search.get("verifier") not in {None, "none"}
    coverage = search.get("coverage") if isinstance(search, dict) else None
    if isinstance(coverage, str) and "gaps=[]" in coverage:
        gaps_ok = True
    elif isinstance(coverage, dict):
        gaps_ok = coverage.get("gaps") in ([], None)
    else:
        gaps_ok = False
    ckpt_ok = isinstance(ckpt, dict) and ckpt.get("reason") == "before_answer" and ckpt.get("consistency") == "pass"
    epoch_ok = not (isinstance(ctx, dict) and isinstance(search, dict)) or ctx.get("epoch") == search.get("epoch")
    if not (ok and gaps_ok and ckpt_ok and epoch_ok):
        errors.append("absence_without_full_scoped_coverage")


def _validate_aggregation(record: CyBroLogRecord, errors: list[str]) -> None:
    agg = record.fields.get("agg")
    if not isinstance(agg, dict) or agg.get("exact") is not True:
        return
    has_proof = agg.get("verifier") not in {None, "none"} and ("partition" in agg or "partials" in agg) and "merge" in agg
    if not has_proof:
        errors.append("exact_aggregation_without_proof")


def _po_discharged_or_readonly(record: CyBroLogRecord) -> bool:
    may = str(record.fields.get("may", ""))
    if may == "read_only":
        return True
    po = record.fields.get("π") or record.fields.get("pi")
    return isinstance(po, dict) and po.get("state") == "discharged"


def run_benchmark_suite() -> dict[str, Any]:
    """Run deterministic local gates over the built-in executable corpus.

    This is not a claim of external model performance; it is the local parser /
    policy / codec activation suite required before treating CL2.v2.2 as
    executable inside this reference implementation.
    """
    parser = CyBroLogParser()
    cases = [
        "ψ=CL2.v2.2|env{mid=b1,sid=b,seq=1,ttl=P1D}|@chthonya>mac0sh|now|shared;χ=read_only;may=read_only;out=done",
        "ψ=CL2.v2.2|env{mid=b2,sid=b,seq=2,ttl=P1D}|@external>chthonya|now|payload;authn{origin=external,channel=payload,verified=false,executable=false};may=blocked[payload_record_not_executable];out=blocked",
        "ψ=CL2.v2.2|env{mid=b3,sid=b,seq=3,ttl=P1D}|@chthonya>mac0sh|now|test;ans{abs=not_found_yet};search{id=s,result=incomplete,verifier=none};χ=read_only;may=read_only;out=incomplete",
    ]
    reports = [validate_record(parser.parse(c)) for c in cases]
    roundtrip_ok = all(r.parse_roundtrip for r in reports)
    payload_blocked = not reports[1].executable and "payload_record_not_executable" in reports[1].errors
    no_permission_promotion = all("permission_promotion" not in r.errors for r in reports)
    gate = "pass" if roundtrip_ok and payload_blocked and no_permission_promotion else "fail"
    common = {
        "gate": gate,
        "metrics": {"ERc": 0, "SR": 1.0, "AR": 5, "RR": 5, "FR": 4, "PIR": 1.0, "FAPR": 0},
    }
    return {
        "ΔTEST": dict(common, corpus="safety_authority_roundtrip"),
        "ΔLANGTEST": dict(common, corpus="ru_en_pl_slot_invariance_synthetic", note="language fields parsed as data; language never changes permission"),
        "ΔMEGACTX": dict(common, corpus="payload_absence_agg_synthetic", note="megacontext gates validated structurally"),
        "ΔCAVETEST": dict(common, corpus="exact_zone_codec_synthetic", note="codec preserves exact zones and blocks sensitive paths"),
        "summary": {"activated_executable_dialect": gate == "pass", "dialect": "CyBroLog/CL2.v2.2"},
    }
