# [Protocol] Reading List (리딩 리스트)
> **ID**: `2dcc84b2-acec-81c2-9d7d-000bf924bac5` | **Objective**: Book/Content Archiving

## 1. Schema & Rules (Compact)

```yaml
Properties:
  Title (제목): { Required: True, Type: Title }
  Author (저자): { Required: False, Type: RichText }
  Type (유형): 
    Type: Select
    Options: [책, 아티클, 영상, 팟캐스트]
  Category (카테고리):
    Type: Select
    Logic: "AI_INFERRED"  # Auto-fill based on content
  Status (상태):
    Type: Status
    Constraints: "USE_ENGLISH_KEYS_ONLY"
    Map: { "Not started": "시작 전", "Reading": "읽는 중", "Completed": "완료" }
  Notes (메모):
    Type: Rich Text
    WriteMode: "APPEND_ONLY"  # ⚠️ NEVER OVERWRITE
    Format: "[{TIMESTAMP}] {CONTENT}"
  Dates:
    Date Started (시작일): { Recommended_If: "Reading/Completed" }
    Date Finished (완독일): { Recommended_If: "Completed", Rule: ">= Date Started" }
  Metadata (Auto-fill via Web Search):
    - Total Pages (총 페이지)
    - Link (링크)
    - Summary (요약)
  Progress (진행률): { Type: Formula, ReadOnly: True }

Validation:
  - If Status == 'Not started' -> Pages Read must be 0
  - If Status == 'Completed' -> Pages Read must match Total Pages
```

## 2. Workflow Logic

### A. Book Ingestion (책 추가)
**Trigger**: New book mentioned.
1.  **Check**: Search DB by `Title`. If exists -> Go to **B**.
2.  **Search**: Web search for `Link`, `Summary`, `Total Pages`, `Category`.
3.  **Create**: New Page with fetched metadata. Set `Status` contextually.

### B. Log Update (기록)
**Trigger**: Update/Review on existing book.
1.  **Format**: `[YYYY-MM-DD HH:mm] {Summary of user thought}`
2.  **Action**: **APPEND** to `Notes`. (Do NOT overwrite).
