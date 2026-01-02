# MODIFICATION_PROPOSAL: User Data Hub (Dataset Catalog)
> **Status**: Proposed | **Version**: v1.0 | **Role**: Schema Architect

## 1. 개요
- **Target**: User Data Hub (데이터셋 카탈로그)
- **Goal**: 머신러닝 데이터셋의 거버넌스 및 버전 관리 체계 구축.

## 2.5 벤치마킹 레퍼런스
- **🏆 [Notion Engineering Wiki](https://www.notion.so/templates/engineering-wiki)**: Notion 공식 엔지니어링 위키 템플릿. (기술 문서 및 리소스 관리 구조가 데이터셋 관리에 적합)
- **💡 [Iterative MLOps](https://iterative.ai/)**: (Curation Source - 개념) 데이터 버전 관리(DVC) 및 카탈로그의 필수 메타데이터 속성 참조.

## 3. 제안 전략

### [Create] Property: Data Owner (Steward)
- **Type**: Person
- **Reasoning**: "엔지니어링 위키의 문서 관리자(Owner) 개념을 도입하여, 데이터셋의 유지보수 책임자를 명확히 함."

### [Create] Property: Technical Specs
- **Type**: Multi-Select
- **Options**: Format(CSV/Parquet), Size, Source
- **Reasoning**: "데이터 엔지니어가 필요한 핵심 메타데이터를 빠르게 파악."

### [Create] Property: Version Link
- **Type**: URL (DVC/S3)
- **Reasoning**: "Notion 자체가 아닌 외부 스토리지(S3, DVC)의 실제 데이터 위치를 가리키는 포인터 역할 수행."
