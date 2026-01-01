# 목표 (Objective)
현재 존재하는 Notion 페이지와 데이터베이스 구조를 분석하여, AI 에이전트가 **오류 없이 안전하게 데이터를 입력(Input)**할 수 있도록 돕는 **`AGENT_PROTOCOL.md` (입력 매뉴얼)**을 생성하는 것입니다.
*   **Key Distinction**: 이 워크플로우는 DB 구조를 개선하거나 제안(`Proposal`)하는 것이 **아니라**, **현재 구조에 맞춰 올바르게 사용하는 법**을 정의하는 데 집중합니다.

# 작업 흐름 (Workflow)

0.  **도구 준비 (Helper MCPs Setup)**
    *   **Context7**: 입력 필드의 값(Value)에 대한 표준 참조. (예: "Technical Difficulty 필드에 들어갈 표준 척도는 무엇인가?")
    *   **Sequential Thinking**: 현재 컬럼들의 조합을 보고 **입력 제약조건(Constraint)**을 논리적으로 추론. (예: "Status가 Done이면 Completed Date는 필수값이어야 한다"는 규칙 도출)

1.  **현재 상태 분석 (Current State Analysis)**
    *   **Notion MCP**: 페이지 제목, DB 컬럼(Property), 기존 데이터 샘플을 읽어옵니다.
    *   **Pattern Recognition**:
        *   어떤 필드가 필수(Required)인지?
        *   특정 Select 옵션의 의미는 무엇인지?
        *   제목 포맷(Naming Convention)이 존재하는지?

2.  **안전 프로토콜 수립 (Safety Protocol Definition)**
    *   AI가 데이터를 넣을 때 **절대 어기면 안 되는 규칙**을 정의합니다.
    *   *작성 항목*:
        *   **Schema Definition**: 각 필드의 정확한 타입과 허용 값.
        *   **Validation Rules**: "이 필드가 A이면 저 필드는 B여야 한다."
        *   **Input Formatting**: 텍스트 톤, 길이 제한, 마크다운 사용 여부.

3.  **매뉴얼 문서화 및 배포 (Documentation & Deployment)**
    *   위 규칙들을 **`AGENT_PROTOCOL.md`** 파일로 생성합니다.
    *   생성된 프로토콜을 해당 Notion 페이지 상단에 **Callout 블록** 등으로 삽입하여, 이후 접근하는 모든 에이전트가 이 규칙을 먼저 읽고 따르도록 강제합니다.
    *   *결과물*: **"Human/AI 공용 데이터 입력 안전 가이드"**