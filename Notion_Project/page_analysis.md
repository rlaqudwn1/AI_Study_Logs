# 목표 (Objective)
Notion 페이지 또는 데이터베이스를 분석하여, 외부 AI 에이전트가 **Notion MCP**를 통해 해당 페이지의 데이터를 자율적으로 읽고(Read), 쓰고(Create), 수정(Update)할 수 있도록 하는 **기술 명세서 (`AGENT_PROTOCOL.md`)**를 작성하는 것입니다.

# 작업 흐름 (Workflow)

1.  **스키마 탐색 및 지식 참조 (Schema Discovery w/ Context7)**
    *   **Notion MCP**: 대상 페이지의 모든 속성 이름, 타입(Select, Multi-select, Relation 등), 옵션 목록을 스캔합니다.
    *   **Context7**: 탐색된 속성들이 해당 도메인(예: 프롬프트 엔지니어링)의 표준이나 모범 사례에 부합하는지 `Context7`을 통해 관련 라이브러리나 문서를 참조하여 검증합니다.

2.  **논리적 추론 및 규칙 설계 (Reasoning w/ Sequential Thinking)**
    *   **Sequential Thinking MCP**: 단순한 나열이 아닌, 데이터 입력 시나리오를 단계적으로 사고하여 비즈니스 로직을 수립합니다.
        *   *각 단계에서 "이 속성 값이 A일 때, B 필드는 필수인가?"를 스스로 질문하고 검증합니다.*
    *   속성 간의 의존성(Dependency)과 필수 입력 조건(Constraints)을 명확히 정의합니다.

3.  **프로토콜 생성 (Protocol Generation)**
    *   분석된 내용을 바탕으로 **`AGENT_PROTOCOL.md`** 파일을 생성합니다.
    *   포함 내용:
        *   **Schema Map**: 필드명과 데이터 타입 매핑 (JSON 구조 권장)
        *   **Action Rules**: 데이터 입력/수정 시 반드시 지켜야 할 규칙
        *   **Few-shot Examples**: 올바른 데이터 입력 예시