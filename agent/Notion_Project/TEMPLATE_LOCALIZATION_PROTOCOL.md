# [Protocol] Notion Template Localization (템플릿 한글화)
> **Objective**: Automate the localization of imported English Notion Templates using AI Tools.

## 1. Standard Dictionary (Korean Mapping)

```yaml
Common_Properties:
  Title: 제목
  Name: 이름
  Date: 날짜
  Created time: 생성일
  Edited time: 수정일
  Tags: 태그
  Status: 상태
  Type: 유형
  Category: 카테고리
  Files & media: 파일 및 미디어
  URL: 링크
  Person: 담당자
  Summary: 요약
  Checkbox: 체크박스
```

## 2. Workflow Logic

### A. Discovery & Planning (탐색 및 기획)
**Trigger**: User provides `[Page Name]`.
1.  **Search**: Find Page/DB ID using `notion_API-post-search`.
2.  **Schema Scan**: Read current properties and options.
3.  **Sequential Thinking**: 
    - **Analyze**: Break down the schema structure.
    - **Draft**: Create a renaming map (English -> Korean).
    - **Constraint Check**: Identify `Status` properties that cannot be renamed.
4.  **Context7 Verification**:
    - **Query**: "Best Korean translation for [Term] in [Context]?"
    - **Role**: Ensure professional and standard terminology (e.g., 'Retrospective' -> '회고').

### B. Property Localization (속성 한글화)
**Action**: Execute `update_a_data_source`.
1.  **Rename**: Change property names based on the plan.
2.  **Status Handling**: 
    - **Rule**: Keep English keys. 
    - **Option**: (If possible) Add Korean description or use only for color mapping.

### C. Option Migration (옵션 한글화)
**Target**: `Select`, `Multi-Select`.
1.  **Create**: Add new Korean options via `update_a_data_source`.
2.  **Migrate**: Iterate pages -> Update English option to Korean option.
3.  **Delete**: Remove old English options.

### D. Content Translation (내용 한글화)
**Target**: Template Pages & Descriptions.
1.  **Context7**: "Translate this template instruction to natural Korean."
2.  **Update**: Replace text while preserving blocks (Toggles, Callouts).

## 3. Agent Critical Warnings
- ⚠️ **DO NOT**: Skip `Sequential Thinking`. Complex migrations require step-by-step validation.
- ⚠️ **DO NOT (Status)**: Attempting to rename Status options causes API errors.
