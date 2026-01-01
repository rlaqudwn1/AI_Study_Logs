# 🥋 Jira Agile Analysis & Feedback Flow

**Agile Expert** 페르소나가 프로젝트를 진단하고 피드백을 생성하는 표준 프로세스입니다.

---

## 0. 🛠️ Helper MCPs Setup (Preparation)
> *최신 지식과 논리적 사고를 위해 보조 도구를 먼저 준비합니다.*
- **Context7**: Agile/Scrum 최신 방법론 및 Jira Best Practice를 참조합니다.
- **Sequential Thinking**: 단순 현황 파악을 넘어, 데이터 간의 인과관계를 추론(Deep Reasoning)합니다.

## 1. 🔍 Discovery Phase (현황 파악)
> *데이터를 수집하여 프로젝트의 물리적 구조를 파악하는 단계입니다.*

### A. Project Structure Scan
- **Tool**: `getVisibleJiraProjects`
- **Checklist**:
  - `projectTypeKey`: `software` 확인
  - `style`: `next-gen` (Team-managed) vs `classic` (Company-managed) 식별
  - `uuid`: Cloud ID 매핑 확인

### B. Knowledge Base Scan
- **Tool**: `getConfluenceSpaces`
- **Checklist**:
  - Jira 프로젝트 키(`DTM`)와 연관된 Space 존재 여부
  - `0 results` 일 경우: **"Critical - Knowledge Gap"** 으로 진단

### C. Issue Sample Scan
- **Tool**: `searchJiraIssuesUsingJql` (`ORDER BY created DESC`, `limit=20`)
- **Checklist**:
  - **Template Usage**: 최근 이슈들이 표준 템플릿(`Why`, `checklist`)을 따르는가?
  - **Status Mapping**: `statusCategory`가 `done`(Green)인지 `indeterminate`(Yellow)인지 확인
  - **Hierarchy**: `Epic Link`나 `Parent` 필드가 채워져 있는가?

---

## 2. 🏥 Diagnosis Phase (건강 검진)
> *수집된 데이터를 Agile Best Practice와 비교하여 문제를 식별하는 단계입니다.*

### 🚨 Critical Checks (최우선 점검)
1.  **Velocity Integrity (속도 무결성)**
    - *Symptom*: 이슈는 "완료"인데 Status Category가 "Yellow"임.
    - *Diagnosis*: **"Velocity Trap"** (번다운 차트 누락, 속도 0 측정).
2.  **Context Missing (맥락 부재)**
    - *Symptom*: 제목만 있고 본문이 비어있음.
    - *Diagnosis*: **"Context Gap"** (히스토리 추적 불가).

### 🟡 Growth Checks (성장 점검)
1.  **Standardization (표준화)**
    - *Check*: 템플릿 사용 비율 (최근 10개 중 몇 개?)
2.  **Granularity (업무 크기)**
    - *Check*: 이슈가 너무 크거나(Epic급), 너무 작지 않은가?

---

## 3. 📝 Prescription Phase (처방 및 피드백)
> *식별된 문제에 대해 구체적인 Action Item을 제시하는 단계입니다.*

### Output Format: `JIRA_AGILE_FEEDBACK.md`
보고서는 항상 다음 3가지 섹션을 포함해야 합니다:

1.  **Health Check Board**: 점수(1-5)와 상태 아이콘(🚨, ⚠️, 🟢)으로 직관적 표시.
2.  **Deep Dive (Why/Solution)**: 단순 지적이 아닌, *왜* 문제가 되는지(비즈니스 임팩트) 설명.
3.  **Action Items (Immediate/Short/Long)**:
    - **Immediate**: 당장 설정(Config) 바꿔서 해결할 수 있는 것.
    - **Short-term**: 이번 스프린트에 적용할 규칙 (예: 템플릿 강제).
    - **Long-term**: 문화나 도구 도입 (예: Confluence 구축).

---

## 4. 🤖 Automation Trigger
이 분석 프로세스는 다음과 같은 상황에서 실행됩니다:
- 새로운 Jira 프로젝트가 등록되었을 때
- 스프린트가 종료되고 회고(Retrospective) 자료가 필요할 때
- 사용자가 `/analyze` 명령어를 입력했을 때
