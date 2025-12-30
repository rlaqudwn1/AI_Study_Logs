from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def error_exit(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_pass1(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        error_exit(f"Pass1 file not found: {path}")
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            raw = line.strip()
            if not raw:
                continue
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError as exc:
                error_exit(f"JSON parse failed in {path}:{line_no}: {exc}")
            if not isinstance(obj, dict):
                continue
            if "franchise_key" not in obj or "items" not in obj:
                continue
            if not obj.get("franchise_key"):
                continue
            items = obj.get("items")
            if not isinstance(items, list):
                continue
            rows.append(obj)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def chunk(rows: list[dict[str, Any]], batch_size: int) -> list[list[dict[str, Any]]]:
    return [rows[i:i + batch_size] for i in range(0, len(rows), batch_size)]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Split pass1_idx JSONL into batches for PASS2 prompts.",
    )
    parser.add_argument("--pass1", required=True, help="Path to pass1_idx.jsonl")
    parser.add_argument("--batch-size", type=int, default=15, help="Franchises per batch")
    parser.add_argument("--out-dir", default="pass2_batches", help="Output directory")
    args = parser.parse_args()

    rows = read_pass1(Path(args.pass1))
    batches = chunk(rows, args.batch_size)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for index, batch in enumerate(batches, 1):
        path = out_dir / f"batch_{index:03d}.jsonl"
        write_jsonl(path, batch)

    print(f"[OK] loaded franchises: {len(rows)}")
    print(f"[OK] wrote batches: {len(batches)} files to {out_dir}")


if __name__ == "__main__":
    main()
