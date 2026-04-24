from __future__ import annotations

from dataclasses import dataclass, field
import re


@dataclass
class CodecValidation:
    result: str
    errors: list[str] = field(default_factory=list)
    exact_zones: list[str] = field(default_factory=list)


@dataclass
class CodecResult:
    output: str
    validation: CodecValidation


SENSITIVE_PATTERNS = [
    ".ssh/", ".aws/", ".gnupg/", ".kube/", ".docker/",
    "id_rsa", "id_ed25519", "credentials", "secrets", "password", "token", "private_key", ".pem", ".key",
]

EXACT_RE = re.compile(
    r"(`[^`]*`|https?://\S+|/(?:[\w.-]+/)*[\w.-]+|\b\d{4}-\d{2}-\d{2}\b|\b[a-f0-9]{12,}\b)"
)

DROP_WORDS = {
    "please", "kindly", "just", "really", "very", "basically", "actually", "the", "a", "an",
    "i", "would", "like", "to", "you", "can", "could", "maybe",
}


def cave_codec(text: str, mode: str = "lite", source_path: str | None = None) -> CodecResult:
    if source_path and any(p.lower() in source_path.lower() for p in SENSITIVE_PATTERNS):
        return CodecResult(text, CodecValidation("fail", ["sensitive_path"], []))
    zones = EXACT_RE.findall(text)
    placeholders: dict[str, str] = {}
    protected = text
    for i, zone in enumerate(zones):
        ph = f"__ZONE_{i}__"
        placeholders[ph] = zone
        protected = protected.replace(zone, ph, 1)

    compressed = _compress_words(protected, mode)
    for ph, zone in placeholders.items():
        compressed = compressed.replace(ph, zone)

    errors = ["lost_exact_zone" for z in zones if z not in compressed]
    return CodecResult(compressed, CodecValidation("fail" if errors else "pass", errors, zones))


def _compress_words(text: str, mode: str) -> str:
    if mode == "off":
        return text
    words = text.split()
    out: list[str] = []
    for word in words:
        bare = re.sub(r"[^\w-]", "", word).lower()
        if mode in {"full", "ultra"} and bare in DROP_WORDS:
            continue
        if mode == "lite" and bare in {"please", "kindly", "basically", "actually"}:
            continue
        out.append(word)
    result = " ".join(out)
    result = result.replace(" in order to ", " to ").replace(" because ", " ∵ ").replace(" therefore ", " ∴ ")
    if mode == "ultra":
        result = result.replace(" and ", "+").replace(" then ", "→")
    return result.strip()
