from __future__ import annotations

from dataclasses import dataclass, field
import json
import re
from typing import Any

SUPPORTED_DIALECTS = {"CL2.v2.2", "CyBroLog.v2.2", "CyBroLog/CL2.v2.2"}


@dataclass
class CyBroLogRecord:
    dialect: str
    env: dict[str, Any] = field(default_factory=dict)
    actor: str | None = None
    recipient: str | None = None
    time: str | None = None
    scope: str | None = None
    fields: dict[str, Any] = field(default_factory=dict)
    atoms: list[str] = field(default_factory=list)
    raw: str = ""

    def to_canonical(self) -> dict[str, Any]:
        return {
            "dialect": self.dialect,
            "env": _sort_obj(self.env),
            "actor": self.actor,
            "recipient": self.recipient,
            "time": self.time,
            "scope": self.scope,
            "fields": _sort_obj(self.fields),
            "atoms": list(self.atoms),
        }


def _sort_obj(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _sort_obj(value[k]) for k in sorted(value)}
    if isinstance(value, list):
        return [_sort_obj(v) for v in value]
    return value


class CyBroLogParser:
    """Small strict parser for the executable CL2.v2.2 subset.

    The parser is intentionally conservative: it parses the surface into a
    canonical AST, preserves quoted delimiters, and leaves unknown objects as
    strings rather than granting them semantics.
    """

    def parse(self, text: str) -> CyBroLogRecord:
        raw = text.strip()
        parts = _split_top(raw, "|")
        if len(parts) < 2 or not (parts[0].startswith("ψ=") or parts[0].startswith("psi=")):
            raise ValueError("missing dialect discriminant")
        dialect = parts[0].split("=", 1)[1].strip()
        if dialect not in SUPPORTED_DIALECTS and dialect.startswith("CyBroLog"):
            raise ValueError("unsupported historical CyBroLog dialect for executable mode")

        idx = 1
        env: dict[str, Any] = {}
        if idx < len(parts) and parts[idx].startswith("env{"):
            env = _parse_braced(parts[idx], "env")
            idx += 1

        if idx >= len(parts) or not parts[idx].startswith("@"):
            raise ValueError("missing route")
        route = parts[idx][1:]
        if ">" in route:
            actor, recipient = route.split(">", 1)
        else:
            actor, recipient = route, None
        idx += 1

        time = parts[idx] if idx < len(parts) else None
        scope_and_fields = parts[idx + 1] if idx + 1 < len(parts) else ""
        if ";" in scope_and_fields:
            scope, field_text = scope_and_fields.split(";", 1)
        else:
            scope, field_text = scope_and_fields, ""

        fields: dict[str, Any] = {}
        atoms: list[str] = []

        def set_field(key: str, value: Any) -> None:
            if key in fields:
                raise ValueError(f"duplicate_field:{key}")
            fields[key] = value

        for item in _split_top(field_text, ";"):
            item = item.strip()
            if not item:
                continue
            if item.startswith("⟦") and item.endswith("⟧"):
                atoms.append(item)
                continue
            if re.match(r"^[A-Za-z_][\w-]*\{", item) or re.match(r"^[α-ωΑ-Ωπχγεηοκρσμψ]+\{", item):
                key = item.split("{", 1)[0]
                set_field(key, _parse_braced(item, key))
                continue
            if item.startswith("π=PO{"):
                set_field("π", _parse_braced(item.split("=", 1)[1], "PO"))
                continue
            if item.startswith("pi=PO{"):
                set_field("pi", _parse_braced(item.split("=", 1)[1], "PO"))
                continue
            if "=" in item:
                key, val = item.split("=", 1)
                set_field(key.strip(), _parse_value(val.strip()))
            elif ":" in item:
                key, val = item.split(":", 1)
                set_field(key.strip(), _parse_value(val.strip()))
            else:
                atoms.append(item)
        return CyBroLogRecord(dialect, env, actor, recipient, time, scope, fields, atoms, raw)


def render_record(record: CyBroLogRecord) -> str:
    chunks: list[str] = [f"ψ={record.dialect}"]
    if record.env:
        chunks.append("env" + _render_obj(record.env))
    route = f"@{record.actor or ''}"
    if record.recipient:
        route += f">{record.recipient}"
    chunks.extend([route, record.time or "now"])
    body: list[str] = []
    for atom in record.atoms:
        body.append(atom)
    for key in _field_order(record.fields):
        value = record.fields[key]
        if key in {"π", "pi"} and isinstance(value, dict):
            body.append(f"{key}=PO{_render_obj(value)}")
        elif isinstance(value, dict):
            body.append(f"{key}{_render_obj(value)}")
        else:
            body.append(f"{key}={_render_value(value)}")
    return "|".join(chunks + [f"{record.scope or 'shared'};" + ";".join(body)])


def _field_order(fields: dict[str, Any]) -> list[str]:
    preferred = [
        "authn", "mc", "plane", "lan", "tok", "task", "ctxgraph", "focus",
        "obj", "obj:module", "obj:channel", "obj:payload_ref", "obj:quoted_text", "obj:note",
        "ans", "η", "ο", "γ", "ε", "search", "agg", "vld", "cmp", "zone", "val", "fix", "mcmp", "rb", "χ", "may", "π", "pi", "anchor", "ckpt", "out"
    ]
    return [k for k in preferred if k in fields] + sorted(k for k in fields if k not in preferred)


def _split_top(text: str, sep: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    stack: list[str] = []
    quote = False
    escape = False
    pairs = {"}": "{", "]": "["}
    for ch in text:
        if escape:
            buf.append(ch); escape = False; continue
        if ch == "\\":
            if not quote:
                raise ValueError("raw_backslash_outside_quotes")
            buf.append(ch); escape = True; continue
        if ch == '"':
            quote = not quote; buf.append(ch); continue
        if not quote:
            if ch in "{[":
                stack.append(ch)
            elif ch in "}]":
                if not stack or stack[-1] != pairs[ch]:
                    raise ValueError("unbalanced_delimiter_or_quote")
                stack.pop()
            elif ch == sep and not stack:
                parts.append("".join(buf)); buf = []; continue
        buf.append(ch)
    if quote or stack:
        raise ValueError("unbalanced_delimiter_or_quote")
    parts.append("".join(buf))
    return parts


def _parse_braced(text: str, name: str) -> dict[str, Any]:
    prefix = f"{name}{{"
    if name == "PO" and text.startswith("PO{"):
        prefix = "PO{"
    if not text.startswith(prefix) or not text.endswith("}"):
        raise ValueError(f"malformed {name} object")
    inner = text[len(prefix):-1]
    out: dict[str, Any] = {}
    for item in _split_top(inner, ","):
        item = item.strip()
        if not item:
            continue
        if "=" in item:
            k, v = item.split("=", 1)
            key = k.strip()
            if key in out:
                raise ValueError(f"duplicate_object_key:{name}.{key}")
            out[key] = _parse_value(v.strip())
        else:
            key = item.strip()
            if key in out:
                raise ValueError(f"duplicate_object_key:{name}.{key}")
            out[key] = True
    return out


def _parse_value(text: str) -> Any:
    text = text.strip()
    if text == "true": return True
    if text == "false": return False
    if text == "none": return None
    if text.startswith('"') and text.endswith('"'):
        return json.loads(text)
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1]
        if not inner.strip(): return []
        return [_parse_value(x.strip()) for x in _split_top(inner, ",")]
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if re.fullmatch(r"-?\d+\.\d+", text):
        return float(text)
    return text


def _render_obj(obj: dict[str, Any]) -> str:
    return "{" + ",".join(f"{k}={_render_value(obj[k])}" for k in sorted(obj)) + "}"


def _render_value(value: Any) -> str:
    if value is True: return "true"
    if value is False: return "false"
    if value is None: return "none"
    if isinstance(value, list):
        return "[" + ",".join(_render_value(v) for v in value) + "]"
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value)
    if not s or any(ch in s for ch in ';|=[]{}",') or s.strip() != s:
        return json.dumps(s, ensure_ascii=False)
    return s
