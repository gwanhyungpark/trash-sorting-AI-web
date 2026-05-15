import os
import re
from typing import Dict, List, Tuple

import gradio as gr


CATEGORY_INFO: Dict[str, Dict[str, str]] = {
    "paper": {
        "name": "종이류",
        "box": "종이류 수거함",
        "how": "테이프, 비닐, 스프링, 음식물 등 이물질을 제거한 뒤 배출하세요.",
        "tip": "젖었거나 기름이 많이 묻은 종이는 재활용이 어려워 일반쓰레기로 버리는 경우가 많습니다.",
    },
    "plastic": {
        "name": "플라스틱류",
        "box": "플라스틱 수거함",
        "how": "내용물을 비우고 물로 가볍게 헹군 뒤, 라벨과 뚜껑은 가능한 분리하세요.",
        "tip": "페트병은 찌그러뜨려 부피를 줄이면 수거와 운반에 도움이 됩니다.",
    },
    "vinyl": {
        "name": "비닐류",
        "box": "비닐류 수거함",
        "how": "음식물이나 물기를 제거하고 깨끗한 상태로 배출하세요.",
        "tip": "라면 봉지처럼 안쪽이 더러운 비닐은 헹구거나 닦은 뒤 배출하는 것이 좋습니다.",
    },
    "glass": {
        "name": "유리류",
        "box": "유리병 수거함",
        "how": "내용물을 비우고 뚜껑을 제거한 뒤 깨지지 않게 배출하세요.",
        "tip": "깨진 유리나 거울은 재활용 유리병과 다르게 처리해야 하므로 신문지 등으로 감싸 일반쓰레기 또는 지자체 기준에 따라 배출하세요.",
    },
    "metal": {
        "name": "캔·고철류",
        "box": "캔/금속 수거함",
        "how": "내용물을 비우고 가능한 한 압착해서 배출하세요.",
        "tip": "부탄가스, 스프레이 캔은 반드시 구멍을 뚫거나 완전히 비운 뒤 지역 기준에 따라 배출해야 합니다.",
    },
    "food": {
        "name": "음식물류",
        "box": "음식물 쓰레기통",
        "how": "물기를 최대한 제거한 뒤 음식물 쓰레기로 배출하세요.",
        "tip": "뼈, 조개껍데기, 과일 씨처럼 사료화가 어려운 것은 일반쓰레기인 경우가 많습니다.",
    },
    "electronics": {
        "name": "소형 폐가전",
        "box": "폐가전 수거함 또는 지자체 수거 신청",
        "how": "배터리를 분리할 수 있으면 따로 분리하고, 소형 폐가전 수거함이나 수거 서비스를 이용하세요.",
        "tip": "전자제품은 일반 재활용품과 섞지 않는 것이 안전합니다.",
    },
    "battery": {
        "name": "폐건전지/배터리",
        "box": "폐건전지 수거함",
        "how": "일반쓰레기나 재활용품에 섞지 말고 전용 수거함에 넣으세요.",
        "tip": "배터리는 화재 위험이 있어 따로 분리 배출하는 것이 중요합니다.",
    },
    "clothing": {
        "name": "의류/섬유류",
        "box": "의류 수거함",
        "how": "세탁 가능한 상태의 옷은 의류 수거함에 넣고, 심하게 오염된 천은 일반쓰레기로 배출하세요.",
        "tip": "젖은 옷이나 오염된 옷은 다른 의류까지 오염시킬 수 있습니다.",
    },
    "hazardous": {
        "name": "주의 폐기물",
        "box": "전용 수거 장소 또는 지자체 문의",
        "how": "형광등, 약품, 날카로운 물건 등은 일반 수거함에 바로 넣지 말고 전용 배출 방법을 확인하세요.",
        "tip": "다칠 위험이 있는 물건은 단단히 포장하고 겉면에 표시하면 안전합니다.",
    },
    "medicine": {
        "name": "폐의약품",
        "box": "약국 또는 보건소 폐의약품 수거함",
        "how": "약은 하수구나 일반쓰레기로 버리지 말고 폐의약품 수거함을 이용하세요.",
        "tip": "알약, 물약, 연고 등은 종류에 따라 포장 방법이 다를 수 있으므로 수거함 안내를 확인하세요.",
    },
    "general": {
        "name": "일반쓰레기",
        "box": "종량제 봉투",
        "how": "재활용이 어렵거나 이물질 제거가 힘든 경우 종량제 봉투에 배출하세요.",
        "tip": "재활용 마크가 있어도 음식물, 기름, 흙 등이 심하게 묻으면 재활용이 어려울 수 있습니다.",
    },
}

KEYWORDS: Dict[str, List[str]] = {
    "paper": ["종이", "신문", "책", "노트", "상자", "박스", "택배", "골판지", "휴지심", "paper", "box", "cardboard"],
    "plastic": ["플라스틱", "페트", "pet", "병", "샴푸", "세제", "용기", "뚜껑", "plastic", "bottle"],
    "vinyl": ["비닐", "봉지", "라면봉지", "과자봉지", "랩", "필름", "vinyl", "wrapper", "bag"],
    "glass": ["유리", "유리병", "병뚜껑", "거울", "깨진", "glass", "mirror"],
    "metal": ["캔", "고철", "철", "알루미늄", "참치캔", "음료캔", "스프레이", "부탄", "metal", "can"],
    "food": ["음식", "밥", "김치", "과일", "껍질", "채소", "남은", "찌꺼기", "food"],
    "electronics": ["전자", "충전기", "케이블", "이어폰", "키보드", "마우스", "휴대폰", "가전", "electronic", "charger"],
    "battery": ["건전지", "배터리", "보조배터리", "리튬", "battery"],
    "clothing": ["옷", "의류", "양말", "수건", "천", "셔츠", "바지", "clothes", "cloth"],
    "hazardous": ["형광등", "전구", "칼", "바늘", "깨진유리", "깨진 유리", "화학", "페인트", "hazard", "knife"],
    "medicine": ["약", "알약", "물약", "연고", "의약품", "medicine", "pill"],
}

MATERIAL_TO_CATEGORY = {
    "종이": "paper",
    "플라스틱": "plastic",
    "비닐": "vinyl",
    "유리": "glass",
    "금속/캔": "metal",
    "음식물": "food",
    "전자제품": "electronics",
    "건전지/배터리": "battery",
    "의류": "clothing",
    "약/화학물질": "medicine",
    "날카롭거나 위험한 물건": "hazardous",
}

DANGER_WORDS = ["깨진", "날카", "칼", "바늘", "형광등", "전구", "약", "배터리", "부탄", "스프레이"]


def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def score_categories(text: str, materials: List[str]) -> Tuple[Dict[str, int], List[str]]:
    scores = {key: 0 for key in CATEGORY_INFO}
    reasons = []

    for category, words in KEYWORDS.items():
        for word in words:
            if word.lower() in text:
                scores[category] += 3
                reasons.append(f"'{word}' 단어가 {CATEGORY_INFO[category]['name']}와 관련됨")

    for material in materials:
        category = MATERIAL_TO_CATEGORY.get(material)
        if category:
            scores[category] += 5
            reasons.append(f"선택한 재질 '{material}' 반영")

    if any(word in text for word in ["배터리", "건전지", "보조배터리", "리튬"]):
        scores["battery"] += 8
    if any(word in text for word in ["약", "알약", "물약", "연고", "의약품"]):
        scores["medicine"] += 8
    if any(word in text for word in ["형광등", "칼", "바늘", "화학", "페인트"]):
        scores["hazardous"] += 8

    return scores, reasons


def make_confidence(best_score: int, second_score: int) -> int:
    if best_score <= 0:
        return 45
    gap = max(0, best_score - second_score)
    confidence = 55 + best_score * 5 + gap * 4
    return max(45, min(95, confidence))


def classify_trash(item_text: str, materials: List[str], contamination: int, is_empty: bool, is_dry: bool) -> str:
    text = normalize(item_text)
    materials = materials or []

    if not text and not materials:
        return "### 입력이 부족합니다\n버릴 물건의 이름이나 재질을 하나 이상 입력해 주세요."

    scores, reasons = score_categories(text, materials)

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_category, best_score = sorted_scores[0]
    second_score = sorted_scores[1][1]

    recyclable = {"paper", "plastic", "vinyl", "glass", "metal", "clothing"}
    changed_by_condition = False
    if best_category in recyclable:
        if contamination >= 70 or not is_empty or not is_dry:
            if best_category != "glass" and best_category != "metal":
                best_category = "general"
                changed_by_condition = True

    if any(word in text for word in DANGER_WORDS):
        for special in ["battery", "medicine", "hazardous", "metal", "glass"]:
            if scores.get(special, 0) == max(scores.values()) or scores.get(special, 0) >= 6:
                best_category = special
                break

    info = CATEGORY_INFO[best_category]
    confidence = make_confidence(best_score, second_score)

    reason_lines = []
    for reason in reasons[:4]:
        reason_lines.append(f"- {reason}")
    if changed_by_condition:
        reason_lines.append("- 오염도, 물기, 내용물 상태 때문에 재활용보다 일반쓰레기 배출이 더 안전하다고 판단함")
    if not reason_lines:
        reason_lines.append("- 입력 정보가 적어서 일반적인 배출 기준을 우선 적용함")

    condition_note = []
    condition_note.append(f"오염도: {contamination}/100")
    condition_note.append("내용물 비움: 예" if is_empty else "내용물 비움: 아니오")
    condition_note.append("물기 제거: 예" if is_dry else "물기 제거: 아니오")

    return f"""
## 분류 결과: {info['name']}

**추천 배출 위치:** {info['box']}  
**예상 신뢰도:** 약 {confidence}%

### 배출 방법
{info['how']}

### 판단 근거
{chr(10).join(reason_lines)}

### 입력 상태
- {condition_note[0]}
- {condition_note[1]}
- {condition_note[2]}

### 참고
{info['tip']}

> 지역별 분리배출 기준은 조금씩 다를 수 있으므로, 실제 제출물에는 '지역별 기준 확인 필요'라고 적어두면 더 안전합니다.
"""


def build_app() -> gr.Blocks:
    with gr.Blocks(title="AI 분리배출 도우미") as demo:
        gr.Markdown(
            """
# AI 분리배출 도우미
버릴 물건의 이름과 상태를 입력하면, 어떤 방식으로 배출하면 좋을지 추천해 주는 웹 프로그램이다.

이 프로그램은 입력 문장과 선택한 재질을 분석해서 가장 알맞은 분리배출 항목을 추정한다.
"""
        )

        with gr.Row():
            with gr.Column():
                item_text = gr.Textbox(
                    label="버릴 물건 설명",
                    placeholder="예: 라벨이 붙은 페트병, 기름 묻은 피자 박스, 오래된 건전지",
                    lines=3,
                )
                materials = gr.CheckboxGroup(
                    label="해당되는 재질 또는 특징을 선택하세요",
                    choices=list(MATERIAL_TO_CATEGORY.keys()),
                )
                contamination = gr.Slider(0, 100, value=20, step=5, label="오염도")
                is_empty = gr.Checkbox(value=True, label="내용물을 비웠다")
                is_dry = gr.Checkbox(value=True, label="물기를 제거했다")
                button = gr.Button("분리배출 방법 추천", variant="primary")

            with gr.Column():
                output = gr.Markdown(label="결과")

        button.click(
            classify_trash,
            inputs=[item_text, materials, contamination, is_empty, is_dry],
            outputs=output,
        )

        gr.Examples(
            examples=[
                ["라벨이 붙은 투명 페트병", ["플라스틱"], 10, True, True],
                ["기름이 많이 묻은 피자 박스", ["종이"], 85, False, False],
                ["다 쓴 건전지", ["건전지/배터리"], 0, True, True],
                ["깨진 유리컵", ["유리", "날카롭거나 위험한 물건"], 5, True, True],
                ["남은 밥과 반찬", ["음식물"], 50, False, False],
            ],
            inputs=[item_text, materials, contamination, is_empty, is_dry],
        )

        gr.Markdown(
            """
---
### 프로그램 설명
- 입력한 물건 이름에서 핵심 단어를 찾고, 선택한 재질과 오염 상태를 함께 반영한다.
- 재활용 가능성이 있어도 오염이 심하면 일반쓰레기로 안내한다.
- 배터리, 약, 깨진 유리처럼 안전 문제가 있는 항목은 전용 배출을 우선한다.
"""
        )

    return demo


if __name__ == "__main__":
    app = build_app()
    port = int(os.environ.get("PORT", 7860))
    app.launch(server_name="0.0.0.0", server_port=port)
