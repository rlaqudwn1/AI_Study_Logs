# [Protocol] 강의노트DB (Lecture Note DB)
> **ID**: `2ccc84b2-acec-81cb-850c-000b731caf47` | **Objective**: 올인원 강의 노트 및 학습 자료의 체계적 관리
> **Parent**: '올인원 강의 노트' (Page) > '네부캠 강의노트' (Page) > '강의노트DB' (Inline DB)

## 1. Schema & Rules (Compact)

```yaml
Properties:
  강의 노트 (Title):
    Type: Title
    Required: True
    Description: "강의 주제 또는 노트의 제목"

  강의명 (Select):
    Type: Select
    Required: True
    Options:
      - "Pytorch" (Orange)
      - "수학" (Blue)
      - "컴퓨터 비전" (Gray)
      - "AI LIFECYLE" (Default)
      - "RecSys" (Pink)
      - "대회준비" (Brown)
      - "생성" (Red)
      - "BERT" (Orange)
      - "면접" (Green)
      - "coding" (Yellow)
    Rule: "지정된 옵션 값만 사용해야 하며, 새로운 옵션을 임의로 추가하지 않는다."

  강의자료 (Files):
    Type: Files & Media
    Required: False
    Description: "강의 관련 PDF, 이미지, 또는 첨부 파일"

  메모 (Rich Text):
    Type: Rich Text
    Required: False
    Description: "강의 관련 간단한 메모 또는 요약"

  작성 날짜 (Date):
    Type: Date
    Required: False
    Format: "YYYY-MM-DD"
    Description: "노트 작성일 또는 강의 수강일"

Validation:
  - If "강의명" is Missing -> Prompt user to select a category.
  - Check "강의 노트" is not empty.
```

## 2. Workflow Logic

### A. New Note Creation
**Trigger**: 사용자가 새로운 강의 노트를 추가하고자 할 때
1.  **Check**: `강의명`에 해당하는 카테고리가 `Select` 옵션에 존재하는지 확인한다.
2.  **Action**:
    - 존재하면 해당 옵션을 선택하여 페이지를 생성한다.
    - 존재하지 않으면 가장 유사한 상위 카테고리(예: 'coding', '수학')를 선택하거나 사용자에게 확인한다 (옵션 추가 금지).
3.  **Title**: 노트의 핵심 내용을 요약하여 `강의 노트` 제목으로 설정한다.

### B. Material Attachment
**Trigger**: 사용자가 강의 자료(PDF 등)를 업로드 요청할 때
1.  **Action**: `강의자료` 속성에 파일을 업로드한다.

## 3. Agent Critical Warnings
- ⚠️ **DO NOT**: `강의명` (Select) 속성에 없는 새로운 값을 임의로 생성하여 넣지 않는다. (Schema Corruption 방지)
- ⚠️ **DO NOT**: `강의노트DB`의 구조(속성 이름, 타입)를 변경하거나 삭제하지 않는다.
- ⚠️ **DO NOT**: `작성 날짜` 형식을 임의의 텍스트로 넣지 않는다 (반드시 Date 객체 사용).
