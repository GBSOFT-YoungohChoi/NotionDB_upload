from notion_client import Client
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timezone

# 환경 변수 로드
load_dotenv()

# Notion API 키 및 데이터베이스 ID 불러오기
notion_api = os.getenv("NOTION_API_KEY")
database_id = os.getenv("NOTION_DATABASE_ID")

'''
dotenv를 사용하지 않고 os에 직접 설정하는 
# 환경 변수 직접 설정
os.environ["NOTION_API_KEY"] = "your_notion_api_key_here"
os.environ["NOTION_DATABASE_ID"] = "your_database_id_here"

# 환경 변수 불러오기
notion_api = os.environ["NOTION_API_KEY"]
database_id = os.environ["NOTION_DATABASE_ID"]
'''

# Notion API 클라이언트 초기화
notion = Client(auth=notion_api)


def save_model_results_to_json(file_path, data):
    """모델 결과를 JSON 파일로 저장"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def upload_to_notion(data):
    """딕셔너리 데이터를 Notion에 업로드 하기위해, 딕셔너리 데이터의 column속성값들을 미리 입력해주는 과정
    GPT에 원하는 데이터에 맞게 속성값을 변환해달라는 prompt 입력시 잘 바껴서 나오기 때문에 빠른 진행을 위해
    각자에게 맞는 속성입력후 GPT를 통한 변환 추천드림"""

    # 상태 값이 유효한지 확인하고 기본값 설정
    valid_statuses = ["시작전", "진행중", "완료"]
    status_value = data.get("상태", "진행중")  # 기본값: "진행중"

    # 만약 유효하지 않은 값이라면 기본값 "진행중"으로 설정
    if status_value not in valid_statuses:
        status_value = "진행중"

    # start_time과 end_time을 변환 (입력값이 없으면 기본값 적용)
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    # Notion db에 date를 업로드할 경우, 날짜를 변환해주어야 하므로 변환을 위해 날짜를 입력하고 변환함 
    # start_time과 end_time을 변환 (입력값이 없으면 기본값 적용)
    if start_time:
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc).isoformat()
    else:
        start_time = datetime.now(timezone.utc).isoformat()

    if end_time:
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc).isoformat()
    else:
        end_time = datetime.now(timezone.utc).isoformat()


    # 속성값을 설정해줌 
    # 아래의 model_result라는 딕트를 업로드해주기 위한 과정임 
    # 현재 지정되어있는 각각의 값들은 default값으로 지정되어있음
    properties = {
        "Create Date": {
            "date": {"start": data.get("Create Date", datetime.now(timezone.utc).isoformat())}
        },
        "상태": {
            "status": {"name": status_value}
        },
        "Title": {
            "title": [{"text": {"content": data["Title"]}}]
        },
        "Model": {
            "multi_select": [{"name": t} for t in data.get("Model", [])]
        },
        "Loss_A": {
            "number": data.get("Loss_A", 0.0)
        },
        "Loss_B": {
            "number": data.get("Loss_B", 0.0)
        },
        "Loss_C": {
            "number": data.get("Loss_C", 0.0)
        },
        "weight_pth": {
            "rich_text": [{"text": {"content": data.get("weight_pth", "")}}]
        },
        "Run Date": {
            "date": {
                "start": start_time,
                "end": end_time
            }
        },
        "Lr": {
            "number": data.get("Lr", 0.001)
        },
        "steps": {
            "rich_text": [{"text": {"content": str(data.get("steps", ""))}}]
        },
        "batch_size": {
            "rich_text": [{"text": {"content": str(data.get("batch_size", ""))}}]
        },
        "Epoch": {
            "number": data.get("Epoch", 1)
        },
        "In_channel": {
            "number": data.get("In_channel", 3)
        },
        "out_channel": {
            "number": data.get("out_channel", 1)
        },
        "AP": {
            "number": data.get("AP", 0.0)
        }
    }

    # Notion DB에 업로드
    # Notion DB가 Notion Pge에 사전에 생성되어있지 않으면 에러가 발생함
    notion.pages.create(
        parent={"database_id": database_id},
        properties=properties
    )
    print(f"<Database> 모델 결과가 Notion에 성공적으로 업로드되었습니다.")


# 예제 데이터 (모델 학습 결과)
# column변수의 값을 누락할 경우, 위의 속성에서 설정한 default값이 notion db에 업로드됨
model_results = {
    "상태": "완료",
    "Title": "AI 모델 학습 결과",
    "Model": ["ResNet50", "Mobile0.25"],
    "Loss_A": 0.023,
    "Loss_B": 0.045,
    "Loss_C": 0.012,
    "weight_pth": "/path/to/weights.pth",
    "Create Date": datetime.now(timezone.utc).isoformat(),
    "Lr": 0.001,
    "steps": "10000",
    "batch_size": "32",
    "Epoch": 50,
    "In_channel": 3,
    "out_channel": 1,
    "AP": 0.87,
    "start_time": "2024-03-18 14:00",  # 시작 시간
    "end_time": "2024-03-18 17:00"  # 종료 시간
}

# JSON 파일로 저장
json_file_path = "model_results.json"
save_model_results_to_json(json_file_path, model_results)

# Notion에 업로드
upload_to_notion(model_results)
