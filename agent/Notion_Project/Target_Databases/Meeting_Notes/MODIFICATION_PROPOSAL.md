# MODIFICATION_PROPOSAL: Meeting Notes
> **Status**: Proposed | **Version**: v1.0 | **Role**: Schema Architect

## 1. 개요
- **Target**: Meeting Notes (회의록 DB)
- **Goal**: AI 기반 자동 요약 및 Action Item 관리 최적화, 2025년 협업 트렌드 반영.

## 2.5 벤치마킹 레퍼런스
- **🏆 [Notion Meeting Notes Category](https://www.otion.so/templates/category/meetings)**: Notion 공식 템플릿 갤러리의 회의록 모음. (다양한 회의 유형별 템플릿 확인 가능)
- **💡 [Fellow.ai Notion Templates](https://fellow.app/notion-templates/)**: (Curation Source) Agenda 및 Action Item 중심의 구조적 템플릿.

## 3. 제안 전략

### [Create] Property: AI Summary
- **Type**: Text (or AI Block)
- **Options**: Notion AI 'Ask AI' 블록 활용 권장
- **Reasoning**: "최신 트렌드에 맞춰 회의 종료 후 AI 요약을 상단에 배치, 신속한 정보 공유 유도."

### [Create] Property: Action Items
- **Type**: Text (Checklist) or Relation
- **Reasoning**: "회의에서 도출된 과제(Task)를 명확히 기록. Fellow.ai 템플릿의 'Action Items' 섹션 구조 차용."

### [Update] Property: Meeting Type
- **Type**: Select
- **Options**: Daily Scrum, Weekly Sync, 1:1, Brainstorming
- **Reasoning**: "공식 템플릿들에서도 공통적으로 사용하는 분류 방식으로, 회의 성격에 맞는 템플릿 자동 적용을 위함."
