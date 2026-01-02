# [Protocol] Papers (논문 DB)
> **Objective**: Academic Knowledge Base & Research Assets

## 1. Schema & Rules (Compact)

```yaml
Properties:
  Title (논문 제목): { Type: Title, Required: True }
  Reading Status (읽기 상태):
    Type: Status
    Map: { "Inbox": "수집", "Reading": "읽는중", "Summarizing": "요약중", "Done": "완료" }
  Keywords (태그):
    Type: Multi-Select
    Options: [CV, NLP, Transformer, Diffusion, Survey]
  Related Experiments (관련 실험): { Type: Relation(Experiment_Table) }
  Link (PDF/URL): { Type: URL }
  Publication Year: { Type: Number }

Validation:
  - If Status == 'Done' -> Must have 'Keywords'.
```

## 2. Workflow Logic

### A. Paper Scrapping
**Trigger**: Finding a relevant paper.
1.  **Input**: Title and Link.
2.  **Status**: Set to `Inbox`.

### B. Deep Reading
**Trigger**: Starting analysis.
1.  **Status**: Update to `Reading`.
2.  **Tagging**: Add `Keywords` (CV, NLP, etc.).
3.  **Link**: Connect to `Related Experiments` if testing the idea.

## 3. Agent Critical Warnings
- ⚠️ **DO NOT**: Create duplicate tags (Search before creating).
