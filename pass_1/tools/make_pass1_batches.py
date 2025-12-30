from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Any


def error_exit(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_titles(path: Path) -> tuple[list[tuple[int, str]], int]:
    if not path.exists():
        error_exit(f"Titles file not found: {path}")
    rows: list[tuple[int, str]] = []
    skipped = 0
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        for line_no, row in enumerate(reader, 1):
            if not row or all(not cell.strip() for cell in row):
                continue
            if len(row) < 2:
                skipped += 1
                continue
            item_raw = row[0].strip()
            title = row[1].strip()
            if not item_raw or not title:
                skipped += 1
                continue
            if line_no == 1 and item_raw.lower() == "item" and title.lower() == "title":
                continue
            try:
                item_id = int(item_raw)
            except ValueError:
                skipped += 1
                continue
            rows.append((item_id, title))
    return rows, skipped


def write_batch(path: Path, rows: list[tuple[int, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        for item_id, title in rows:
            handle.write(f"{item_id}\t{title}\n")


def chunk(rows: list[tuple[int, str]], batch_size: int) -> list[list[tuple[int, str]]]:
    return [rows[i:i + batch_size] for i in range(0, len(rows), batch_size)]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Split titles.tsv into batches for PASS1 prompts.",
    )
    parser.add_argument("--titles", required=True, help="Path to titles.tsv")
    parser.add_argument("--out_dir", default="pass1_inputs", help="Output directory")
    parser.add_argument("--batch_size", type=int, default=500, help="Items per batch")
    args = parser.parse_args()

    rows, skipped = read_titles(Path(args.titles))
    rows.sort(key=lambda r: (r[1].lower(), r[1], r[0]))
    batches = chunk(rows, args.batch_size)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for index, batch in enumerate(batches, 1):
        path = out_dir / f"batch_{index:03d}.txt"
        write_batch(path, batch)

    print(f"[OK] loaded titles: {len(rows)}")
    print(f"[OK] skipped lines: {skipped}")
    print(f"[OK] wrote batches: {len(batches)} files to {out_dir}")


if __name__ == "__main__":
    main()
