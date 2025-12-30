from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

YEAR_RE = re.compile(r"\((\d{4})\)\s*$")


def error_exit(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_item_id(value: Any) -> int | None:
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str):
        text = value.strip()
        if text.isdigit():
            return int(text)
    return None


def extract_year(title: Any) -> int | None:
    if not isinstance(title, str):
        return None
    match = YEAR_RE.search(title)
    if not match:
        return None
    try:
        return int(match.group(1))
    except ValueError:
        return None


def iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            raw = line.strip()
            if not raw:
                continue
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError as exc:
                error_exit(f"JSON parse failed in {path}:{line_no}: {exc}")
            if isinstance(obj, dict):
                yield obj


def list_input_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if path.is_dir():
        files = sorted(path.glob("*.jsonl"), key=lambda p: str(p))
        if not files:
            error_exit(f"No JSONL files found in directory: {path}")
        return files
    error_exit(f"Input path not found: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Merge PASS1 outputs into a single pass1.jsonl",
    )
    parser.add_argument("--in_dir", required=True, help="Directory or JSONL file with PASS1 outputs")
    parser.add_argument("--out", required=True, help="Output pass1.jsonl path")
    args = parser.parse_args()

    input_path = Path(args.in_dir)
    files = list_input_files(input_path)

    merged: dict[str, dict[str, Any]] = {}
    items_seen: dict[str, set[int]] = {}
    notes_seen: dict[str, set[str]] = {}
    global_item_index: dict[int, set[str]] = {}

    total_lines = 0
    skipped_rows = 0

    for path in files:
        for obj in iter_jsonl(path):
            total_lines += 1
            if "franchise_key" not in obj or "items" not in obj:
                skipped_rows += 1
                continue
            key = str(obj.get("franchise_key") or "").strip()
            if not key:
                skipped_rows += 1
                continue
            items = obj.get("items")
            if not isinstance(items, list):
                skipped_rows += 1
                continue

            aggregate = merged.setdefault(
                key,
                {
                    "franchise_key": key,
                    "franchise_name": "",
                    "items": [],
                },
            )

            name = obj.get("franchise_name")
            if isinstance(name, str) and name.strip() and not aggregate.get("franchise_name"):
                aggregate["franchise_name"] = name

            conf = obj.get("confidence")
            if isinstance(conf, (int, float)) and not isinstance(conf, bool):
                current = aggregate.get("confidence")
                value = float(conf)
                aggregate["confidence"] = max(current, value) if current is not None else value

            amb = obj.get("ambiguous")
            if isinstance(amb, bool):
                aggregate["ambiguous"] = bool(aggregate.get("ambiguous")) or amb
            elif aggregate.get("ambiguous") is None and amb not in (None, ""):
                aggregate["ambiguous"] = amb

            note = obj.get("notes")
            if isinstance(note, str) and note.strip():
                notes_seen.setdefault(key, set()).add(note.strip())

            seen_items = items_seen.setdefault(key, set())
            for item in items:
                if not isinstance(item, dict):
                    continue
                item_id = parse_item_id(item.get("item"))
                title = item.get("title")
                if item_id is None or not isinstance(title, str) or not title:
                    continue
                if item_id in seen_items:
                    continue
                seen_items.add(item_id)
                aggregate["items"].append({"item": item_id, "title": title})
                global_item_index.setdefault(item_id, set()).add(key)

    for key, aggregate in merged.items():
        notes = notes_seen.get(key)
        if notes:
            aggregate["notes"] = " | ".join(sorted(notes))
        items = aggregate.get("items", [])
        items.sort(
            key=lambda it: (
                extract_year(it.get("title")) or 9999,
                str(it.get("title") or "").lower(),
                it.get("item", 0),
            )
        )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as handle:
        for key in sorted(merged.keys()):
            aggregate = merged[key]
            handle.write(json.dumps(aggregate, ensure_ascii=False) + "\n")

    dup_items = {item: keys for item, keys in global_item_index.items() if len(keys) > 1}

    print(f"[OK] input files: {len(files)}")
    print(f"[OK] total lines: {total_lines}")
    print(f"[OK] skipped rows: {skipped_rows}")
    print(f"[OK] merged franchises: {len(merged)}")
    print(f"[OK] wrote output: {out_path}")
    print(f"[WARN] items_in_multiple_franchises: {len(dup_items)}")

    if dup_items:
        print("[WARN] examples: ")
        for item_id, keys in sorted(dup_items.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:10]:
            sample = ", ".join(sorted(keys)[:5])
            more = "" if len(keys) <= 5 else f" (+{len(keys) - 5} more)"
            print(f"  item {item_id} in {len(keys)} franchises: {sample}{more}")


if __name__ == "__main__":
    main()
