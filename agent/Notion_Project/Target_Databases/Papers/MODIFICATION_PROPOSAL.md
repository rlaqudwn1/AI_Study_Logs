# MODIFICATION_PROPOSAL: Papers
> **Status**: Proposed | **Version**: v1.0 | **Role**: Schema Architect

## 1. 개요
- **Target**: Papers (논문 관리 DB)
- **Goal**: 단순 스크랩을 넘어선 '연구 자산화'. 실험 및 학습 기록과 연동되는 Knowledge Base 구축.

## 2.5 벤치마킹 레퍼런스
- **🏆 [Notion Student & Research Category](https://www.notion.so/templates/category/students)**: 공식 갤러리의 연구 및 학습 관리 템플릿 모음. (Reading List, Thesis Planning 등)
- **🏆 [Academic Reading List](https://www.notion.so/templates/reading-list)**: 공식 Reading List 템플릿. 상태(Status) 및 태그 관리 방식 참조.

## 3. 제안 전략

### [Create] Property: Reading Status
- **Type**: Status
- **Options**: 📥 Inbox -> 🧐 Reading -> 📝 Summarizing -> ✅ Done
- **Reasoning**: "공식 Reading List 템플릿의 흐름을 반영하여, 읽기 진행 상황을 체계적으로 관리."

### [Create] Property: Key Keywords (Tags)
- **Type**: Multi-Select
- **Options**: CV, NLP, Transformer, Diffusion, Survey
- **Reasoning**: "연구 분야별로 논문을 빠르게 필터링하기 위함."

### [Create] Property: Related Experiments
- **Type**: Relation (to Experiment Table)
- **Reasoning**: "해당 논문의 아이디어를 차용하여 진행한 실험을 역추적(Back-link) 할 수 있도록 함."

### [Create] Property: PDF / Link
- **Type**: Files & Media / URL
- **Reasoning**: "원문 접근성을 높임."
