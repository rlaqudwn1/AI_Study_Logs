# [Protocol] User Data Hub (데이터셋)
> **Objective**: Dataset Catalog & Governance

## 1. Schema & Rules (Compact)

```yaml
Properties:
  Dataset Name (데이터셋명): { Type: Title, Required: True }
  Data Owner (관리자): { Type: Person, Role: "Steward" }
  Specs (스펙):
    Type: Multi-Select
    Options: [CSV, Parquet, JSON, Image, Text]
  Source Link (S3/DVC): { Type: URL, Purpose: "Pointer to actual data" }
  Description: { Type: Text }

Validation:
  - 'Source Link' must point to valid storage (S3/DVC/HuggingFace).
```

## 2. Workflow Logic

### A. Registration
**Trigger**: New dataset acquired/created.
1.  **Assign**: Set `Data Owner`.
2.  **Describe**: Add technical specs (Format, Size).
3.  **Link**: Add URL to `Source Link`.

## 3. Agent Critical Warnings
- ⚠️ **DO NOT**: Upload large files directly to Notion (Use pointers).
