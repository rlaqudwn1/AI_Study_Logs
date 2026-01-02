# MODIFICATION_PROPOSAL: DataTailor Dashboard
> **Status**: Proposed | **Version**: v1.0 | **Role**: Schema Architect

## 1. 개요
- **Target**: DataTailor Dashboard (메인 대시보드)
- **Goal**: 프로젝트의 모든 리소스(논문, 실험, 데이터)를 연결하는 통합 관제탑(Control Tower) 구축.

## 2.5 벤치마킹 레퍼런스
- **🏆 [PARA Dashboard by Arafat Rodro](https://arafatrodro.gumroad.com/l/PARA-Dashboard)**: (Gumroad) PARA 방법론을 적용한 대시보드 구조의 실제 예시.
- **🏆 [Notion Project Management Category](https://www.notion.so/templates/category/project-management)**: Notion 공식 PM 템플릿 갤러리.

## 3. 제안 전략

### [UX] Structure: PARA Method
- **Action**: Projects(실험), Areas(연구 분야), Resources(논문/데이터), Archives(완료) 구분.
- **Reasoning**: "Arafat Rodro의 템플릿과 같이 명확한 구획(Section)을 나누어 정보의 성격에 따라 직관적으로 접근."

### [UX] Widget: Navigation Bar
- **Action**: Synced Block을 활용한 상단 네비게이션.
- **Reasoning**: "어떤 하위 페이지에서도 메인 대시보드로 즉시 복귀할 수 있는 UX 제공."

### [MX] Linked Views
- **Action**: 'Recent Experiments', 'To-Read Papers' 등 핵심 DB의 필터링 된 뷰 배치.
- **Reasoning**: "대시보드 진입 즉시 '오늘 해야 할 일'을 파악할 수 있도록 함."
