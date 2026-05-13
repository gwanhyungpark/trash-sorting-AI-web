# AI 분리배출 도우미

사용자가 버릴 물건의 이름, 재질, 오염 상태를 입력하면 알맞은 분리배출 방법을 추천하는 Gradio 웹 프로그램입니다.

## 실행 방법

```bash
pip install -r requirements.txt
python app.py
```

실행 후 터미널에 표시되는 주소로 접속하면 웹 화면을 확인할 수 있습니다.

## 배포 방법

Hugging Face Spaces에서 SDK를 Gradio로 선택한 뒤, 이 폴더의 파일을 업로드하면 됩니다.
Render를 사용할 경우 Start Command는 다음과 같이 설정합니다.

```bash
python app.py
```

Build Command는 다음과 같이 설정합니다.

```bash
pip install -r requirements.txt
```

## 주요 기능

- 물건 이름과 재질을 기반으로 배출 항목 추정
- 오염도, 물기, 내용물 여부 반영
- 배터리, 약, 깨진 유리 등 위험 항목 우선 처리
- 배출 방법과 판단 근거 출력
