# 📚 Notion DB 업로드

- 이 프로젝트는 AI 모델의 실험 결과를 쉽게 **Notion 데이터베이스**에 저장하고 관리하기 위한 파이썬 스크립트입니다.  
- 자신의 Notion DB column에 맞게 "upload_to_notion" 함수에 properties를 변경해서 활용하시기 바랍니다. 
---

## 🎯 핵심 기능

- ✅ **모델 결과를 Notion에 자동 업로드**
- ✅ JSON 파일로 결과를 저장 후 업로드하거나, JSON 없이 바로 업로드 가능
- ✅ 데이터가 없을 경우 기본값 자동 설정

---

## 📌 프로젝트 구성

| 파일명                        | 설명                                       |
|------------------------------|------------------------------------------|
| `notion_upload_with_json.py`  | 결과를 JSON 파일로 저장한 뒤 Notion DB에 업로드 |
| `notion_upload_without_json.py` | JSON 파일 저장 없이 바로 Notion DB에 업로드  |

---
## 📦 필요 패키지 설치
```bash
pip install notion-client python-dotenv
```
---

## 🛠️ 사전 설정하기 (환경변수) - Notion 서버 마스터만 진행

1. **Notion Integration 생성하기**
   - [Notion Integration 페이지](https://www.notion.so/my-integrations)에서 Integration을 만들고 API 키를 발급받습니다.
   - Notion에서 사용할 데이터베이스를 Integration에 공유 권한을 부여합니다.
   - API를 공유합니다.

2. 환경 변수 설정 (`.env` 파일)

- 프로젝트 폴더에 `.env` 파일을 만들고 아래와 같이 입력합니다:

```bash
NOTION_API_KEY=여기에_당신의_NOTION_API_KEY_입력
NOTION_DATABASE_ID=여기에_당신의_DATABASE_ID_입력
```
- 환경변수를 직접 코드에 설정하고 싶다면 아래 방법을 사용하세요 (권장하지 않음):
```python
os.environ["NOTION_API_KEY"] = "your_notion_api_key"
os.environ["NOTION_DATABASE_ID"] = "your_notion_database_id"
```
---

## 🚀 실행 방법

### 1️⃣ JSON 파일 저장 후 Notion 업로드 방식
```bash
python notion_upload_with_json.py
```
### 2️⃣ JSON 파일 없이 바로 Notion 업로드 방식
```bash
python notion_upload_without_json.py
```
### 🗂️ 데이터 예시
```json
{
    "Title": "AI 모델 학습 결과",
    "Model": ["ResNet50", "Mobile0.25"],
    "상태": "완료",  // ["시작전", "진행중", "완료"] 중 선택
    "Loss_A": 0.023,
    "Loss_B": 0.045,
    "Loss_C": 0.012,
    "weight_pth": "/path/to/weights.pth",
    "Create Date": "2024-03-18T14:00:00Z",
    "start_time": "2024-03-18 14:00",
    "end_time": "2024-03-18 17:00",
    "Epoch": 1,
    "batch_size": "32",
    "In_channel": 3,
    "out_channel": 1,
    "AP": 0.87,
    "Lr": 0.001,
    "steps": "10000"
}
```
💡 참고:
데이터에서 특정 키가 빠져도 기본값으로 자동 입력됩니다.
e.g., "Loss_C" 누락 시, "0.0" 자동으로 업로드

---

## ⚠️ 주의사항

- Notion 데이터베이스의 컬럼 이름은 코드에서 지정된 이름과 정확히 일치해야 합니다.
- 사전에 Notion 페이지에서 데이터베이스가 생성되지 않으면 스크립트 실행 시 오류가 발생합니다.
