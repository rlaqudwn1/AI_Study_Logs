# [Protocol] Meeting Notes (회의록)
> **Objective**: Efficient Meeting Tracking & Action Item Distribution

## 1. Schema & Rules (Compact)

```yaml
Properties:
  Topic (주제): { Type: Title, Required: True }
  Date (날짜): { Type: Date, Default: "Today" }
  Meeting Type (회의 유형):
    Type: Select
    Options: [Daily Scrum, Weekly Sync, 1:1, Brainstorming]
  Participants (참석자): { Type: Person / Text }
  AI Summary (AI 요약): { Type: Text / AI Block, AutoGen: True }
  Action Items (할 일):
    Type: Checklist / Relation
    Format: "- [ ] @Person Task Description"

Validation:
  - All Action Items must have an Assignee.
```

## 2. Workflow Logic

### A. Pre-Meeting
**Trigger**: Scheduling a meeting.
1.  **Template**: Select template based on `Meeting Type`.
2.  **Agenda**: List discussion points.

### B. Post-Meeting
**Trigger**: Meeting ends.
1.  **Summarize**: Run Notion AI or write `AI Summary`.
2.  **Distribute**: Convert Action Items to Tasks (if Jira/Task DB connected) or tag users.

## 3. Agent Critical Warnings
- ⚠️ **DO NOT**: Leave Action Items unassigned.
