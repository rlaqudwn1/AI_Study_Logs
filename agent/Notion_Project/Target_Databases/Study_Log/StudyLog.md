# [Protocol] Study Log (학습 기록)
> **ID**: `2dcc84b2-acec-806f-8dc3-fa5dc821da55` | **Objective**: Learning Tracker & Active Recall System

## 1. Schema & Rules (Compact)

```yaml
Properties:
  Lecture Name (강의명/제목): { Type: Title, Required: True }
  Category (분류): { Type: Select }
  Review Status (복습 일정):
    Type: Date
    Logic: "SPACED_REPETITION" # 1d, 3d, 1w intervals
  Confidence (이해도):
    Type: Select
    Options: [⭐⭐⭐, ⭐⭐, ⭐]
  Key Findings (핵심 요약): { Type: Rich Text, Length: Short }
  Link (자료 링크): { Type: URL }
  Content Structure:
    - Toggle Q&A: { Question: "Toggle Header", Answer: "Toggle Content" }

Validation:
  - All questions for Active Recall must be in Toggle Blocks.
```

## 2. Workflow Logic

### A. Daily Logging
**Trigger**: User shares learning notes.
1.  **Categorize**: Select `Category` and subject.
2.  **Toggle Creation**: Convert key concepts into **Q&A Toggles**.
    - Q: "What is X?"
    - A: (Hidden in toggle) "X is Y..."
3.  **Assessment**: Set initial `Confidence` based on user sentiment.

### B. Review Cycle
**Trigger**: Review Notification or Session.
1.  **Recall Test**: Expand toggles to check answers.
2.  **Update**: Update `Review Status` date to next interval.

## 3. Agent Critical Warnings
- ⚠️ **DO NOT**: Write answers in open text (Must be hidden in Toggle for Active Recall).
