from __future__ import annotations

import argparse
import csv
import glob
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

YEAR_RE = re.compile(r"\((\d{4})\)\s*$")


@dataclass
class Pass1Entry:
    franchise_key: str
    franchise_name: str
    items: list[dict[str, Any]]
    items_by_index: list[dict[str, Any] | None]
    n_items: int
    raw_line: str


def error_exit(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def parse_year(title: Any) -> str:
    if not isinstance(title, str):
        return ""
    match = YEAR_RE.search(title)
    return match.group(1) if match else ""


def load_pass1(path: Path) -> tuple[dict[str, Pass1Entry], list[str]]:
    if not path.exists():
        error_exit(f"Pass1 file not found: {path}")
    entries: dict[str, Pass1Entry] = {}
    order: list[str] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            raw = line.rstrip("\n")
            if not raw.strip():
                continue
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError as exc:
                error_exit(f"JSON parse failed in {path}:{line_no}: {exc}")
            if not isinstance(obj, dict):
                continue
            if "franchise_key" not in obj or "items" not in obj:
                continue
            items = obj.get("items")
            if not isinstance(items, list):
                continue
            key = str(obj.get("franchise_key"))
            if key in entries:
                continue
            franchise_name = obj.get("franchise_name", "")
            if not isinstance(franchise_name, str):
                franchise_name = str(franchise_name)
            n_items = len(items)
            items_by_index: list[dict[str, Any] | None] = [None] * n_items
            for enum_i, item in enumerate(items):
                if not isinstance(item, dict):
                    continue
                idx_value = item.get("idx")
                idx = idx_value if is_int(idx_value) else enum_i
                if idx < 0 or idx >= n_items:
                    idx = enum_i
                if 0 <= idx < n_items and items_by_index[idx] is None:
                    items_by_index[idx] = item
            for i in range(n_items):
                if items_by_index[i] is None and i < len(items) and isinstance(items[i], dict):
                    items_by_index[i] = items[i]
            entries[key] = Pass1Entry(
                franchise_key=key,
                franchise_name=franchise_name,
                items=items,
                items_by_index=items_by_index,
                n_items=n_items,
                raw_line=raw,
            )
            order.append(key)
    return entries, order


def read_jsonl_file(path: Path) -> list[dict[str, Any]]:
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
            rows.append(obj)
    return rows


def expand_pass2_paths(pass2_arg: str) -> list[Path]:
    if any(ch in pass2_arg for ch in "*?[]"):
        matches = [Path(p) for p in glob.glob(pass2_arg)]
        if not matches:
            error_exit(f"No PASS2 files matched: {pass2_arg}")
        return sorted(matches, key=lambda p: str(p))

    path = Path(pass2_arg)
    if path.is_file():
        return [path]
    if path.is_dir():
        matches = sorted(path.glob("*.jsonl"), key=lambda p: str(p))
        if not matches:
            error_exit(f"No JSONL files in PASS2 directory: {path}")
        return matches
    error_exit(f"Pass2 path not found: {pass2_arg}")


def collect_pass2_rows(pass2_arg: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in expand_pass2_paths(pass2_arg):
        rows.extend(read_jsonl_file(path))
    return rows


def normalize_pass2_entry(
    entry: dict[str, Any],
    pass1: Pass1Entry,
) -> tuple[bool, dict[str, Any] | None, str | None]:
    use_for_sequence = entry.get("use_for_sequence")
    if not isinstance(use_for_sequence, bool):
        return False, None, "use_for_sequence_not_bool"
    normalized: dict[str, Any] = {
        "franchise_key": pass1.franchise_key,
        "use_for_sequence": use_for_sequence,
        "continuities": [],
    }
    if "confidence" in entry:
        conf = entry.get("confidence")
        if isinstance(conf, (int, float)) and not isinstance(conf, bool):
            normalized["confidence"] = float(conf)
    if "notes" in entry:
        notes = entry.get("notes")
        if isinstance(notes, str):
            normalized["notes"] = notes
    if not use_for_sequence:
        return True, normalized, None

    continuities = entry.get("continuities")
    if not isinstance(continuities, list) or not continuities:
        return False, None, "continuities_missing_or_empty"

    all_indices: set[int] = set()
    normalized_conts: list[dict[str, Any]] = []

    for cont in continuities:
        if not isinstance(cont, dict):
            return False, None, "continuity_not_object"
        continuity_key = cont.get("continuity_key")
        if not isinstance(continuity_key, str) or not continuity_key.strip():
            return False, None, "continuity_key_missing"
        has_indices = "ordered_indices" in cont
        has_items = "ordered_items" in cont
        if has_indices and has_items:
            return False, None, "ordered_indices_and_items_both_present"
        if has_items:
            return False, None, "ordered_items_not_allowed"
        if not has_indices:
            return False, None, "ordered_indices_missing"

        indices = cont.get("ordered_indices")
        if not isinstance(indices, list) or not indices:
            return False, None, "ordered_indices_missing_or_empty"
        if not all(is_int(idx) for idx in indices):
            return False, None, "ordered_indices_not_int"
        if any(idx < 0 or idx >= pass1.n_items for idx in indices):
            return False, None, "ordered_indices_out_of_range"
        if len(indices) != len(set(indices)):
            return False, None, "ordered_indices_duplicate"
        if any(idx in all_indices for idx in indices):
            return False, None, "ordered_indices_overlap_across_continuities"
        all_indices.update(indices)

        normalized_cont: dict[str, Any] = {
            "continuity_key": continuity_key,
            "ordered_indices": indices,
        }
        if "confidence" in cont:
            conf = cont.get("confidence")
            if isinstance(conf, (int, float)) and not isinstance(conf, bool):
                normalized_cont["confidence"] = float(conf)
        if "order_reason" in cont:
            order_reason = cont.get("order_reason")
            if isinstance(order_reason, str):
                normalized_cont["order_reason"] = order_reason
        normalized_conts.append(normalized_cont)

    normalized["continuities"] = normalized_conts
    return True, normalized, None


def index_pass2_rows(
    rows: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], set[str]]:
    indexed: dict[str, dict[str, Any]] = {}
    duplicates: set[str] = set()
    for obj in rows:
        fk = obj.get("franchise_key")
        if fk is None or fk == "":
            continue
        key = str(fk)
        if key in indexed:
            duplicates.add(key)
            continue
        indexed[key] = obj
    return indexed, duplicates


def validate_pass2(
    pass1_entries: dict[str, Pass1Entry],
    pass1_order: list[str],
    pass2_by_key: dict[str, dict[str, Any]],
    dup_keys: set[str],
) -> tuple[dict[str, dict[str, Any]], list[str], list[str], Counter[str]]:
    ok_entries: dict[str, dict[str, Any]] = {}
    ok_order: list[str] = []
    failed_keys: list[str] = []
    reason_counts: Counter[str] = Counter()

    for key in pass1_order:
        if key in dup_keys:
            reason_counts["duplicate_franchise_key_in_pass2"] += 1
            failed_keys.append(key)
            continue
        out_obj = pass2_by_key.get(key)
        if out_obj is None:
            reason_counts["missing_pass2_output"] += 1
            failed_keys.append(key)
            continue
        ok, normalized, reason = normalize_pass2_entry(out_obj, pass1_entries[key])
        if ok and normalized is not None:
            ok_entries[key] = normalized
            ok_order.append(key)
        else:
            reason_counts[reason or "unknown_failure"] += 1
            failed_keys.append(key)

    for key in pass2_by_key:
        if key not in pass1_entries:
            reason_counts["franchise_key_not_in_pass1"] += 1
    for key in dup_keys:
        if key not in pass1_entries:
            reason_counts["duplicate_franchise_key_in_pass2"] += 1

    return ok_entries, ok_order, failed_keys, reason_counts


def write_ok_jsonl(path: Path, ok_entries: dict[str, dict[str, Any]], ok_order: list[str]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for key in ok_order:
            entry = ok_entries.get(key)
            if entry is None:
                continue
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def write_retry_jsonl(
    path: Path,
    failed_keys: list[str],
    pass1_entries: dict[str, Pass1Entry],
) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for key in failed_keys:
            entry = pass1_entries.get(key)
            if entry is None:
                continue
            handle.write(entry.raw_line + "\n")


def write_franchise_installments_csv(
    path: Path,
    ok_entries: dict[str, dict[str, Any]],
    ok_order: list[str],
    pass1_entries: dict[str, Pass1Entry],
) -> None:
    fieldnames = [
        "franchise_key",
        "franchise_name",
        "continuity_key",
        "installment",
        "item",
        "title",
        "year",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for key in ok_order:
            normalized = ok_entries.get(key)
            if normalized is None:
                continue
            if not normalized.get("use_for_sequence"):
                continue
            pass1 = pass1_entries.get(key)
            if pass1 is None:
                continue
            for cont in normalized.get("continuities", []):
                cont_key = cont.get("continuity_key", "")
                indices = cont.get("ordered_indices", [])
                if not isinstance(indices, list):
                    continue
                for installment, idx in enumerate(indices, 1):
                    if not is_int(idx):
                        continue
                    if idx < 0 or idx >= len(pass1.items_by_index):
                        continue
                    item_entry = pass1.items_by_index[idx]
                    if not isinstance(item_entry, dict):
                        continue
                    item_id = item_entry.get("item")
                    title = item_entry.get("title")
                    year = parse_year(title)
                    writer.writerow(
                        {
                            "franchise_key": pass1.franchise_key,
                            "franchise_name": pass1.franchise_name,
                            "continuity_key": cont_key,
                            "installment": installment,
                            "item": "" if item_id is None else str(item_id),
                            "title": "" if title is None else str(title),
                            "year": year,
                        }
                    )


def print_reason_summary(reason_counts: Counter[str]) -> None:
    print("Failure reason summary (top 10):")
    if not reason_counts:
        print("None")
        return
    for reason, count in reason_counts.most_common(10):
        print(f"{reason}: {count}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate pass2 JSONL and generate retry and mapping outputs.",
    )
    parser.add_argument("--pass1", required=True, help="Path to pass1_idx.jsonl")
    parser.add_argument(
        "--pass2",
        required=True,
        help="Pass2 JSONL file, directory of JSONL files, or glob pattern",
    )
    parser.add_argument("--out-dir", default="artifacts", help="Output directory")
    args = parser.parse_args()

    pass1_entries, pass1_order = load_pass1(Path(args.pass1))
    pass2_rows = collect_pass2_rows(args.pass2)
    pass2_by_key, dup_keys = index_pass2_rows(pass2_rows)

    ok_entries, ok_order, failed_keys, reason_counts = validate_pass2(
        pass1_entries, pass1_order, pass2_by_key, dup_keys
    )

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ok_path = out_dir / "pass2_ok_normalized.jsonl"
    retry_path = out_dir / "pass2_retry_input.jsonl"
    csv_path = out_dir / "franchise_installments.csv"

    write_ok_jsonl(ok_path, ok_entries, ok_order)
    write_retry_jsonl(retry_path, failed_keys, pass1_entries)
    write_franchise_installments_csv(csv_path, ok_entries, ok_order, pass1_entries)
    print_reason_summary(reason_counts)


if __name__ == "__main__":
    main()
