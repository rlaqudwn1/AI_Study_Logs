# PASS1 Pipeline

## Purpose
Create pass1.jsonl by grouping candidate franchise or series titles from titles.tsv.

## Input
- titles.tsv
  - Tab-separated columns: item, title
  - One item per line

## Output
- pass1.jsonl (JSONL)
  - One franchise per line
  - Required fields:
    - franchise_key (string)
    - franchise_name (string)
    - items (list of {item, title})
  - Optional fields:
    - confidence (0.0-1.0)
    - ambiguous (true/false)
    - notes (string)

## Rules
- Do not invent items or titles.
- Exclude singletons (not a franchise).
- Use ambiguous or notes for remakes, reboots, or same-name titles.
- items must only contain items from the input list.

## Step 1: Make batches
Sort titles and split into batches for LLM prompts.

Command:
```
python tools/make_pass1_batches.py --titles titles.tsv --out_dir pass1_inputs --batch_size 500
```

Output:
- pass1_inputs/batch_001.txt
- pass1_inputs/batch_002.txt
- ...

Each batch file line format:
```
item<TAB>title
```

## Step 2: LLM prompt (PASS1)
SYSTEM:
You are clustering movie titles into franchise candidates.
CRITICAL:
- You MUST NOT add any new movies.
- You MUST use only the provided item and title lines.
- Exclude singletons (not a series).
- Output JSONL only.
Each output line must match:
{"franchise_key":"...","franchise_name":"...","items":[{"item":123,"title":"..."}],"confidence":0.0-1.0,"ambiguous":true/false,"notes":"..."}

Guidance:
- franchise_key should be a stable slug (lowercase, alnum and underscores).
- If multiple continuities or remakes exist, mark ambiguous=true and explain in notes.

USER:
BATCH_TSV:
<<<paste one batch file content here>>>

## Step 3: Save outputs
- Save each batch output to pass1_out/batch_001_out.jsonl, pass1_out/batch_002_out.jsonl, ...
- Ensure each line is valid JSON and contains franchise_key + items.

## Step 4: Merge outputs
Merge all PASS1 outputs into a single pass1.jsonl.

Command:
```
python tools/merge_pass1_outputs.py --in_dir pass1_out --out pass1.jsonl
```

Merge rules:
- Merge by franchise_key.
- Deduplicate items by item id within a franchise.
- Sort items by year extracted from title (YYYY), then title, then item.
- Report anomalies where the same item appears in multiple franchises.
