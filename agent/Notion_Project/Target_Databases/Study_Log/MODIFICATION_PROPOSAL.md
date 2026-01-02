# MODIFICATION_PROPOSAL: Study Log
> **Status**: Proposed | **Version**: v1.0 | **Role**: Schema Architect

## 1. 개요
- **Target**: Study Log (학습 기록 & 스킬 트래커)
- **Analyzed Source Page**: ID `2cdc84b2` (Detected Properties: `강의명`, `강의자료`, `강의 노트`)
- **Goal**: Active Recall 및 Spaced Repetition 학습법이 적용된 성장 기록 시스템.

## 2.5 벤치마킹 레퍼런스
- **🏆 [Notion Education Category](https://www.notion.so/templates/category/education)**: Notion 공식 교육용 템플릿 모음. (강의 노트, 학습 계획표 등)
- **🏆 [Bookstorm Active Recall](https://medium.com/@bookstorm/a-free-notion-template-to-practice-active-recall-technique-5ae2562486c7)**: (Curation Source - Article) Active Recall 기법을 적용한 템플릿 구조 설명 및 링크 포함.

## 3. 제안 전략

### [Create] Property: Review Status (Spaced Repetition)
- **Type**: Date / Formula
- **Reasoning**: "공식 교육 템플릿들에서 자주 보이는 '복습 일정' 관리 기능을 도입하여 장기 기억 효율 증대."

### [Create] Property: Confidence Level
- **Type**: Select (⭐⭐⭐)
- **Reasoning**: "메타인지 강화를 위해 자신의 이해도를 3단계로 평가."

### [UX] Template: Toggle Q&A
- **Structure**: 질문(Toggle) -> 답(Content)
- **Reasoning**: "Bookstorm 템플릿에서 강조하는 Active Recall 방식(가리고 외우기)을 템플릿 기본 구조로 채택."
