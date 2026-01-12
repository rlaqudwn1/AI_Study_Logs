# Steam User Crawler (스팀 유저 크롤러)

이 스크립트는 `steam_data/new_steam/players.csv`에 있는 유저 중 `private_steamids.csv`에 없는 유저들을 필터링하여 스팀 API를 통해 정보를 수집합니다.

## 사용법 (Usage)

터미널에서 아래 명령어를 실행하여 크롤링을 진행해주세요. (프로젝트 루트 `My_RecSys_Project` 또는 상위 폴더에서 경로에 유의하여 실행)

### 1. 데이터 준비 (Prepare)
이 단계는 **최초 1회만** 실행하면 됩니다. 전체 유저를 필터링하고 청크 파일로 나눕니다.
```bash
# Windows (PowerShell)
python src/script/crawl_steam_users.py --prepare --chunks_count 10
```
실행 후 `steam_data/new_steam/user_chunks/` 폴더에 `user_ids_0.txt` ~ `user_ids_9.txt` 파일이 생성되었는지 확인하세요.

### 2. 크롤링 실행 (Crawl)
준비된 청크 파일 중 하나를 선택하여 크롤링을 시작합니다. (예: 0번 청크)
```bash
python src/script/crawl_steam_users.py --chunk 0 --concurrency 10
```
- `--chunk`: 0 ~ 9 사이의 번호 (단일 청크 실행)
- `--from_chunk`: 지정한 번호부터 끝까지 순차적으로 실행 (예: `--from_chunk 2`)
- `--concurrency`: 동시 요청 수 (기본 10). 너무 높으면 스팀 API 요청 제한(Rate Limit)에 걸릴 수 있습니다.
- **중단 후 재실행**: 스크립트는 이미 크롤링된 유저를 자동으로 건너뜁니다.
  - **참고**: `game_count`가 0인 유저는 크롤링 실패로 간주하고 자동으로 재시도합니다.

## 주요 로직 설명

### 1. 비동기 스트림 처리 (Stream Processing)
기존의 100명 단위 배치 처리를 제거하고, **유저 한 명씩 비동기적으로(Async) 처리**하는 방식으로 변경했습니다.
- **장점**: 중간에 실패하더라도 성공한 유저는 즉시 저장되므로, 재시작 시 중복 작업이 최소화됩니다.
- `--concurrency` 옵션으로 동시에 처리할 유저 수를 조절합니다.

### 2. 수집 데이터 최적화
속도 향상을 위해 유저 프로필 정보(`GetPlayerSummaries`) 조회 단계를 제거했습니다.
- **`GetOwnedGames`** 만 호출하여 게임 플레이 시간 데이터를 수집합니다.
- API 호출 횟수가 절반으로 줄어들어 크롤링 속도가 빨라졌습니다.

### 3. Private ID 파일 읽기 예외 처리
`private_steamids.csv` 파일을 읽는 도중 문제가 발생했을 때 스크립트가 멈추지 않고 빈 집합으로 처리하여 계속 진행합니다.
