from __future__ import annotations

import argparse
import json
import sys

from .parser import CyBroLogParser, render_record
from .validator import validate_record, run_benchmark_suite
from .codec import cave_codec


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="cybrolog")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("bench")
    parse_p = sub.add_parser("parse")
    parse_p.add_argument("record", nargs="?")
    val_p = sub.add_parser("validate")
    val_p.add_argument("record", nargs="?")
    cmp_p = sub.add_parser("compress")
    cmp_p.add_argument("text", nargs="?")
    cmp_p.add_argument("--mode", default="lite")
    args = p.parse_args(argv)

    if args.cmd == "bench":
        print(json.dumps(run_benchmark_suite(), ensure_ascii=False, indent=2))
        return 0
    if args.cmd in {"parse", "validate"}:
        text = args.record or sys.stdin.read()
        ast = CyBroLogParser().parse(text)
        if args.cmd == "parse":
            print(json.dumps(ast.to_canonical(), ensure_ascii=False, indent=2))
        else:
            rep = validate_record(ast)
            print(json.dumps(rep.__dict__, ensure_ascii=False, indent=2))
            return 0 if rep.executable else 2
        return 0
    if args.cmd == "compress":
        result = cave_codec(args.text or sys.stdin.read(), mode=args.mode)
        print(result.output)
        return 0 if result.validation.result == "pass" else 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
