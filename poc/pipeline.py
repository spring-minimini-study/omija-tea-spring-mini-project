"""
하루한장 - AI 일기 생성 파이프라인 POC
Step 1: Gemini Flash  → 이미지 분석 (병렬)
Step 2: GPT-4o        → 일기 생성
"""

import asyncio
import base64
import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from google import genai
from openai import AsyncOpenAI

# ── 환경 변수 ──────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "asdf")

genai.configure(api_key=GEMINI_API_KEY)
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)


# ── 데이터 모델 ────────────────────────────────────────────

@dataclass
class PhotoMeta:
    """사진 1장의 메타데이터 (EXIF, 날씨 API 결과 등)"""
    image_path: str
    taken_at: str           # "08:42"
    location: str           # "서울 마포구 합정역"
    weather: str = ""       # "맑음, 14°C"

@dataclass
class PhotoAnalysis:
    """Gemini Flash가 분석한 결과 — 팩트 위주"""
    meta: PhotoMeta
    subjects: list[str]     # 사진에 찍힌 주요 피사체/사물 (예: ["아메리카노", "노트북", "테이블"])
    setting: str            # 촬영 환경/장소 유형 (예: "실내 카페", "야외 공원", "지하철 역사")
    people: dict            # 인물 정보 {"count": 2, "description": "20-30대 남녀 2명, 마주 앉아 있음"}
    actions: list[str]      # 관찰되는 행동들 (예: ["대화 중", "음료 마시는 중"])
    visible_text: list[str] # 사진 속 보이는 텍스트/간판 (없으면 [])
    lighting: str           # 조명/시간대 단서 (예: "자연광, 오후", "실내 형광등", "역광")
    colors: list[str]       # 주요 색감 (예: ["베이지", "흰색", "초록"])
    raw_response: str = ""  # 디버깅용 원본 응답

@dataclass
class DiaryInput:
    """일기 생성에 필요한 전체 입력"""
    date: str                               # "2026년 4월 14일 월요일"
    photos: list[PhotoMeta] = field(default_factory=list)
    user_memo: str = ""                     # 유저 한 줄 메모
    mood: str = ""                          # 유저가 선택한 오늘의 무드


# ── Step 1: Gemini Flash 이미지 분석 ──────────────────────

GEMINI_ANALYSIS_PROMPT = """이 사진에서 보이는 것들을 객관적인 사실만 분석하세요.
추측이나 감정 해석 없이, 사진에서 실제로 관찰되는 것만 기술하세요.
마크다운 코드블록 없이 순수 JSON만 출력하세요.

{
  "subjects": ["사진에 찍힌 주요 사물/피사체 목록 (예: 아메리카노 컵, 노트북, 나무 테이블)"],
  "setting": "촬영 장소 유형 (예: 실내 카페, 야외 공원, 지하철 역사, 사무실)",
  "people": {
    "count": 0,
    "description": "인물이 있다면 외형/자세/행동을 객관적으로 묘사. 없으면 빈 문자열"
  },
  "actions": ["관찰되는 행동들 (예: 의자에 앉아 있음, 컵을 들고 있음, 걷고 있음)"],
  "visible_text": ["사진 속 간판/텍스트 (읽을 수 있는 것만, 없으면 빈 배열)"],
  "lighting": "조명 특성 (예: 창문을 통한 자연광, 실내 형광등, 역광, 저녁 노을)",
  "colors": ["사진의 주요 색감 3개 이내 (예: 베이지, 갈색, 흰색)"]
}"""


def _load_image_base64(image_path: str) -> tuple[str, str]:
    """이미지를 base64로 인코딩. (data, mime_type) 반환"""
    path = Path(image_path)
    suffix = path.suffix.lower()
    mime_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".heic": "image/heic",
    }
    mime_type = mime_map.get(suffix, "image/jpeg")
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8"), mime_type


def _parse_gemini_response(raw: str) -> dict:
    """Gemini 응답에서 JSON 파싱 (마크다운 fence 방어)"""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        # 첫 줄(```json), 마지막 줄(```) 제거
        cleaned = "\n".join(lines[1:-1])
    return json.loads(cleaned)


async def analyze_photo_with_gemini(photo: PhotoMeta) -> PhotoAnalysis:
    """Gemini Flash로 사진 1장 분석 (비동기)"""
    print(f"  [Gemini] 분석 중: {photo.image_path} ({photo.taken_at})")

    image_data, mime_type = _load_image_base64(photo.image_path)

    # Gemini API는 현재 동기 방식 → asyncio executor로 비동기 처리
    loop = asyncio.get_event_loop()

    def _call_gemini():
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content([
            {
                "inline_data": {
                    "mime_type": mime_type,
                    "data": image_data,
                }
            },
            GEMINI_ANALYSIS_PROMPT,
        ])
        return response.text

    raw_response = await loop.run_in_executor(None, _call_gemini)

    try:
        parsed = _parse_gemini_response(raw_response)
    except json.JSONDecodeError:
        print(f"  [경고] JSON 파싱 실패. 원본: {raw_response[:200]}")
        parsed = {
            "subjects": [],
            "setting": "알 수 없음",
            "people": {"count": 0, "description": ""},
            "actions": [],
            "visible_text": [],
            "lighting": "알 수 없음",
            "colors": [],
        }

    return PhotoAnalysis(
        meta=photo,
        subjects=parsed.get("subjects", []),
        setting=parsed.get("setting", ""),
        people=parsed.get("people", {"count": 0, "description": ""}),
        actions=parsed.get("actions", []),
        visible_text=parsed.get("visible_text", []),
        lighting=parsed.get("lighting", ""),
        colors=parsed.get("colors", []),
        raw_response=raw_response,
    )


async def analyze_all_photos(photos: list[PhotoMeta]) -> list[PhotoAnalysis]:
    """모든 사진을 병렬로 분석"""
    tasks = [analyze_photo_with_gemini(p) for p in photos]
    results = await asyncio.gather(*tasks)
    # 시간순 정렬
    return sorted(results, key=lambda r: r.meta.taken_at)


# ── Step 2: GPT-4o 일기 생성 ──────────────────────────────

def _build_diary_prompt(diary_input: DiaryInput, analyses: list[PhotoAnalysis]) -> str:
    """GPT-4o에게 전달할 프롬프트 구성"""

    photos_block = ""
    for i, analysis in enumerate(analyses, 1):
        weather_str = f"\n- 날씨: {analysis.meta.weather}" if analysis.meta.weather else ""
        people = analysis.people
        people_str = (
            f"{people['count']}명 — {people['description']}"
            if people.get("count", 0) > 0
            else "없음"
        )
        visible_text_str = ", ".join(analysis.visible_text) if analysis.visible_text else "없음"

        photos_block += f"""
--- 기록 {i} ({analysis.meta.taken_at}) ---
- 장소: {analysis.meta.location} / 환경: {analysis.setting}{weather_str}
- 찍힌 것들: {", ".join(analysis.subjects)}
- 인물: {people_str}
- 관찰된 행동: {", ".join(analysis.actions)}
- 조명/시간대 단서: {analysis.lighting}
- 주요 색감: {", ".join(analysis.colors)}
- 보이는 텍스트: {visible_text_str}
"""

    memo_line = diary_input.user_memo if diary_input.user_memo else "없음"
    mood_line = diary_input.mood if diary_input.mood else "없음"

    return f"""당신은 사용자의 하루를 감성적으로 기록하는 일기 작가입니다.
아래 정보를 바탕으로 자연스럽고 담담한 한국어 일기를 작성해주세요.

[오늘의 정보]
- 날짜: {diary_input.date}
- 오늘의 무드: {mood_line}

[시간순 기록]
{photos_block}
[유저 메모]
{memo_line}

[작성 규칙]
- 5~8문장, 200~300자 내외
- 반말 일기체 (~했다, ~였다, ~이었다)
- 시간 흐름(아침→점심→저녁)을 살려 서사로 자연스럽게 연결
- 장면 묘사 + 감정/생각을 함께 담기
- 유저 메모가 있다면 핵심 테마로 활용
- 오늘의 무드가 있다면 글 전체 톤에 반영
- 마지막 문장은 하루를 마무리하는 짧은 감상으로 끝내기
- 날짜나 날씨 정보를 기계적으로 나열하지 말 것"""


async def generate_diary_with_gpt4o(
    diary_input: DiaryInput,
    analyses: list[PhotoAnalysis],
    tone: str = "담담한 일상체",
) -> str:
    """GPT-4o로 일기 생성"""
    print("\n  [GPT-4o] 일기 생성 중...")

    system_prompt = (
        f"당신은 {tone}으로 하루를 기록하는 일기 작가입니다. "
        "주어진 정보를 바탕으로 자연스럽고 감성적인 한국어 일기를 씁니다. "
        "JSON이나 목록 형식이 아닌, 자연스러운 산문 형태로만 응답하세요."
    )

    user_prompt = _build_diary_prompt(diary_input, analyses)

    response = await openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.8,   # 창의성 살짝 높게
        max_tokens=600,
    )

    return response.choices[0].message.content.strip()


# ── 메인 파이프라인 ────────────────────────────────────────

async def run_pipeline(diary_input: DiaryInput, tone: str = "담담한 일상체") -> dict:
    """
    전체 파이프라인 실행
    Returns: { "analyses": [...], "diary": "..." }
    """
    print(f"\n{'='*50}")
    print(f"  하루한장 파이프라인 시작")
    print(f"  날짜: {diary_input.date} | 사진: {len(diary_input.photos)}장")
    print(f"{'='*50}\n")

    # Step 1: 이미지 병렬 분석 (Gemini Flash)
    print("[Step 1] Gemini Flash - 이미지 분석")
    analyses = await analyze_all_photos(diary_input.photos)

    print("\n  분석 결과 요약:")
    for a in analyses:
        print(f"    {a.meta.taken_at} | {a.meta.location} | {a.scene[:30]}...")

    # Step 2: 일기 생성 (GPT-4o)
    print(f"\n[Step 2] GPT-4o - 일기 생성 (톤: {tone})")
    diary = await generate_diary_with_gpt4o(diary_input, analyses, tone)

    print(f"\n{'='*50}")
    print("  생성된 일기")
    print(f"{'='*50}")
    print(diary)
    print(f"{'='*50}\n")

    return {
        "date": diary_input.date,
        "tone": tone,
        "analyses": [
            {
                "time": a.meta.taken_at,
                "location": a.meta.location,
                "setting": a.setting,
                "subjects": a.subjects,
                "people": a.people,
                "actions": a.actions,
                "lighting": a.lighting,
                "colors": a.colors,
                "visible_text": a.visible_text,
            }
            for a in analyses
        ],
        "diary": diary,
    }


# ── 실행 예시 ──────────────────────────────────────────────

if __name__ == "__main__":
    # 테스트용 입력 — 실제 이미지 경로로 바꿔서 실행
    diary_input = DiaryInput(
        date=datetime.today().strftime("%Y년 %-m월 %-d일 ") + ["월", "화", "수", "목", "금", "토", "일"][datetime.today().weekday()] + "요일",
        photos=[
            PhotoMeta(
                image_path="./sample_images/morning.jpg",
                taken_at="08:42",
                location="서울 마포구 합정역",
                weather="맑음, 14°C",
            ),
            PhotoMeta(
                image_path="./sample_images/lunch.jpg",
                taken_at="12:31",
                location="서울 종로구 광화문",
                weather="맑음, 18°C",
            ),
            PhotoMeta(
                image_path="./sample_images/evening.jpg",
                taken_at="18:15",
                location="서울 용산구 한강공원",
                weather="맑음, 16°C",
            ),
        ],
        user_memo="대학 동기 만나서 한강까지 걸었다",
        mood="설레는",
    )

    result = asyncio.run(run_pipeline(diary_input, tone="담담한 일상체"))

    # 결과 JSON 저장
    with open("./diary_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("결과가 diary_result.json 에 저장되었습니다.")