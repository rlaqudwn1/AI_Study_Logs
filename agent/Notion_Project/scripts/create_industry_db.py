import os
import csv
import sys
from notion_client import Client
from dotenv import load_dotenv

# ======================================================================================
# [설정 영역]
# ======================================================================================

# 2. 타겟 페이지 및 데이터베이스 ID 설정
PARENT_PAGE_ID = "2e2c84b2-acec-807f-828a-c5044f5f00c3"  # 기업 분석 대시보드 페이지
COMPANY_DB_ID = "2e2c84b2-acec-81a8-9be4-000b6bdfb907"   # 기업 목록 DB
PESTEL_DB_ID = "2e2c84b2-acec-810d-9b39-000beac65707"    # PESTEL 분석 DB
FIVE_FORCES_DB_ID = "2e2c84b2-acec-810a-a554-000bfeddde23" # 5-Forces 분석 DB

CSV_FILE_PATH = r"c:\Users\rlaqu\Documents\GitHub\AI_Study_Logs\agent\Notion_Project\Target_Databases\Industry_Analysis\industry_template.csv"

# ======================================================================================
# [Main Logic]
# ======================================================================================
def main():
    # 0. 환경 변수 로드 (.env 파일이 있다면 로드)
    #    - 반드시 실행 최상단에 위치해야 합니다.
    load_dotenv()

    # 1. Notion API Key 설정
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")
    if not NOTION_TOKEN:
        print("⚠️  환경변수에 'NOTION_TOKEN'이 없습니다.")
        NOTION_TOKEN = input("👉 Notion Integration Secret Key를 입력하세요: ").strip()

    notion = Client(auth=NOTION_TOKEN)

    print(f"🚀 '산업 분석 DB' 생성을 시작합니다... (Parent Page: {PARENT_PAGE_ID})")

    # 1. DB 생성
    try:
        new_db = notion.databases.create(
            parent={"type": "page_id", "page_id": PARENT_PAGE_ID},
            title=[{"type": "text", "text": {"content": "산업 분석 DB"}}],
            icon={"type": "emoji", "emoji": "🏭"},
            properties={
                "산업명": {"title": {}},
                "시장 규모 (TAM)": {"rich_text": {}},
                "CAGR (성장률)": {"number": {"format": "percent"}},
                "주요 트렌드 (Key Trend)": {"rich_text": {}},
                "핵심 성공 요인 (KSF)": {"rich_text": {}},
                "상태 (Status)": {
                    "select": {
                        "options": [
                            {"name": "Active", "color": "green"},
                            {"name": "Planned", "color": "gray"},
                            {"name": "In Progress", "color": "blue"},
                        ]
                    }
                },
                # Relation Properties - 권한 문제로 생성 실패 시 주석 처리
                # "관련 기업": {
                #     "relation": {
                #         "database_id": COMPANY_DB_ID,
                #         "type": "dual_property",
                #         "dual_property": {"synced_property_name": "산업 분석"} 
                #     }
                # },
                # "PESTEL 분석": {
                #     "relation": {
                #         "database_id": PESTEL_DB_ID,
                #         "type": "dual_property",
                #         "dual_property": {"synced_property_name": "산업 (Industry)"}
                #     }
                # },
                # "5-Forces 분석": {
                #     "relation": {
                #         "database_id": FIVE_FORCES_DB_ID,
                #         "type": "dual_property",
                #         "dual_property": {"synced_property_name": "산업 (Industry)"}
                #     }
                # }
            }
        )
        db_id = new_db["id"]
        print(f"✅ DB 생성 완료! ID: {db_id}")
        print(f"🔗 링크: {new_db['url']}")
        
    except Exception as e:
        print(f"❌ DB 생성 실패: {e}")
        return

    # 2. CSV 데이터 입력
    if not os.path.exists(CSV_FILE_PATH):
        print(f"⚠️ CSV 파일이 없습니다: {CSV_FILE_PATH}")
        return

    print("\n📦 CSV 데이터를 입력합니다...")
    
    with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            try:
                # CAGR 퍼센트 문자열("35%")을 숫자(0.35)로 변환 시도
                cagr_val = None
                if row.get("CAGR (성장률)"):
                    clean_cagr = row["CAGR (성장률)"].replace("%", "").strip()
                    try:
                        cagr_val = float(clean_cagr) / 100
                    except:
                        cagr_val = None

                notion.pages.create(
                    parent={"database_id": db_id},
                    properties={
                        "산업명": {"title": [{"text": {"content": row["산업명"]}}]},
                        "시장 규모 (TAM)": {"rich_text": [{"text": {"content": row.get("시장 규모 (TAM)", "")}}]},
                        "주요 트렌드 (Key Trend)": {"rich_text": [{"text": {"content": row.get("주요 트렌드 (Key Trend)", "")}}]},
                        "핵심 성공 요인 (KSF)": {"rich_text": [{"text": {"content": row.get("핵심 성공 요인 (KSF)", "")}}]},
                        "CAGR (성장률)": {"number": cagr_val} if cagr_val is not None else {"number": None},
                        "상태 (Status)": {"select": {"name": row.get("상태 (Status)", "Planned")}}
                    }
                )
                print(f"   - 입력 성공: {row['산업명']}")
                count += 1
            except Exception as e:
                print(f"   - ❌ 입력 실패 ({row.get('산업명')}): {e}")

    print(f"\n✨ 모든 작업이 완료되었습니다. 총 {count}건 입력됨.")

if __name__ == "__main__":
    main()
