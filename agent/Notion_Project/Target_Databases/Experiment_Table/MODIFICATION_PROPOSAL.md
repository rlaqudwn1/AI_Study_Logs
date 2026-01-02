# MODIFICATION_PROPOSAL: Experiment Table
> **Status**: Proposed | **Version**: v1.0 | **Role**: Schema Architect

## 1. 개요
- **Target**: Experiment Table (실험 관리 DB)
- **Goal**: 실험의 재현성(Reproducibility) 확보 및 논문/데이터셋과의 유기적 연결.

## 2.5 벤치마킹 레퍼런스
- **🏆 [Notion Growth Experiment Tracker](https://www.notion.so/templates/growth-experiment-tracker)**: Notion 공식 실험 관리 템플릿. (Status, Prediction, Learnings 구조 참조)
- **💡 [ClickUp Experiment Plan & Results](https://clickup.com/templates/experiment-plan-and-results)**: (구조 참고 - Curation) 가설 수립 및 변수 통제 방법론.

## 3. 제안 전략

### [Create] Property: Status (Pipeline)
- **Type**: Status
- **Options**: 💡 Idea -> 🧪 Designing -> 🏃 Running -> 📊 Analyzing -> ✅ Completed / 🚫 Dropped
- **Reasoning**: "공식 템플릿의 파이프라인을 차용하여, 실험의 현재 단계를 명확히 시각화."

### [Create] Property: Hypothesis & Outcome
- **Type**: Text (Summary)
- **Reasoning**: "실험의 목적(가설)과 결론(Outcome)을 상단에 명시하여, 세부 내용을 열지 않고도 핵심을 파악."

### [Create] Property: Linked Paper / Dataset
- **Type**: Relation (to Papers, User Data Hub)
- **Reasoning**: "어떤 논문을 참고했는지, 어떤 데이터셋을 사용했는지 연결하여 연구의 추적성(Traceability) 강화."

### [UX] Template: Lab Notebook
- **Structure**: Objective -> Method/Code -> Results (Image/Metric) -> Discussion
- **Reasoning**: "과학적 실험 노트의 표준 형식을 따름."
