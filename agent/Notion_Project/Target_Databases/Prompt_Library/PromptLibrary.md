# [Protocol] Prompt Engineering Dashboard (프롬프트 대시보드)
> **ID**: `2dcc84b2-acec-815b-a057-000b99255047` | **Objective**: AI Prompt Testing & Version Control

## 1. Schema & Rules (Compact)

```yaml
Properties:
  Prompt Name (프롬프트 명):
    Type: Title
    NamingConvention: "[Task] Description" # e.g. [Coding] Python Generator
  Version (버전):
    Type: Rich Text
    Format: "vX.Y" # e.g. v1.0
  Category (카테고리):
    Type: Select
    Options: [콘텐츠 제작, 코드 생성, 자료 조사, 이미지 생성, 분석, 기타]
  AI Tool (AI 도구):
    Type: Select
    Options: [ChatGPT, Claude, Midjourney, DALL-E, Grok, Other]
  Status (상태):
    Type: Status
    Options: [Draft, Testing, Optimized, Archived]
  Success Rating (성공도 평가):
    Type: Select
    Options: [1 (미흡), 2 (보통), 3 (양호), 4 (우수), 5 (최우수)]
  Parameters (파라미터):
    Type: Multi-Select
    Options: [간결하게, 상세하게, 격식체, 캐주얼, 최대 500자, 창의적]
  Prompt Content (프롬프트 내용): { Type: Rich Text }
  Output Quality (결과 품질): { Type: Rich Text }
  Improvement Notes (개선 사항): { Type: Rich Text }

Validation:
  - If Status == 'Optimized' -> 'Success Rating' must be >= 4 (우수).
```

## 2. Workflow Logic

### A. New Prompt Registration
**Trigger**: Migrating or Creating a prompt.
1.  **Categorize**: Select `Category` and `AI Tool`.
2.  **Parameters**: detailed style/constraints.
3.  **Body**: Paste the full prompt in the Page Body (Code Block recommended).
4.  **Summary**: Paste the first ~100 chars into `Prompt Content` property.

### B. Testing & Optimization
**Trigger**: Running a test.
1.  **Log**: Record `Date Tested`.
2.  **Evaluate**: Fill `Success Rating` and `Output Quality`.
3.  **Refine**: Update `Improvement Notes` if needed.

## 3. Agent Critical Warnings
- ⚠️ **DO NOT (Status)**: Use Korean status keys (e.g. '완료') in API calls. Must use keys: `Draft`, `Testing`, `Optimized`.
