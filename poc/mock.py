"""
mock_test.py — 실제 이미지 없이 파이프라인 전체 로직을 테스트
Gemini 분석 결과를 mock으로 대체해서 GPT-4o 일기 생성만 실행
"""

import asyncio
import json
from datetime import datetime
from unittest.mock import patch, AsyncMock

from pipeline import (
    DiaryInput,
    PhotoMeta,
    PhotoAnalysis,
    generate_diary_with_gpt4o,
    run_pipeline,
)

# ── Mock 분석 데이터 (실제 이미지 없이 테스트) ───────────────

MOCK_ANALYSES = [
    PhotoAnalysis(
        meta=PhotoMeta(
            image_path="mock_morning.jpg",
            taken_at="08:42",
            location="서울 마포구 합정역",
            weather="맑음, 14°C",
        ),
        subjects=["벚꽃 가로수", "지하철 역 출입구", "보도블록", "가로등"],
        setting="야외 지하철역 출입구 앞 거리",
        people={"count": 0, "description": ""},
        actions=["카메라 방향으로 거리가 찍힘, 보행자 없음"],
        visible_text=["2호선", "합정"],
        lighting="오전 자연광, 맑은 하늘",
        colors=["연분홍", "회색", "하늘색"],
    ),
    PhotoAnalysis(
        meta=PhotoMeta(
            image_path="mock_lunch.jpg",
            taken_at="12:31",
            location="서울 종로구 광화문",
            weather="맑음, 18°C",
        ),
        subjects=["라떼 2잔", "원형 나무 테이블", "스마트폰", "냅킨"],
        setting="실내 카페",
        people={"count": 2, "description": "20대 후반으로 보이는 남녀 각 1명, 테이블을 사이에 두고 마주 앉아 있음"},
        actions=["대화 중", "음료를 손에 들고 있음"],
        visible_text=["COFFEE"],
        lighting="창문을 통한 자연광, 오후 측광",
        colors=["베이지", "흰색", "갈색"],
    ),
    PhotoAnalysis(
        meta=PhotoMeta(
            image_path="mock_evening.jpg",
            taken_at="18:15",
            location="서울 용산구 한강공원",
            weather="맑음, 16°C",
        ),
        subjects=["한강 수면", "석양", "산책로", "벤치", "원거리 아파트 단지"],
        setting="야외 한강 둔치 공원",
        people={"count": 2, "description": "두 사람이 강을 바라보며 나란히 서 있음, 뒷모습"},
        actions=["강 방향을 바라보며 서 있음"],
        visible_text=[],
        lighting="저녁 노을, 역광, 주황-붉은 하늘",
        colors=["주황", "붉은색", "남색"],
    ),
]


async def test_diary_generation_only():
    """GPT-4o 일기 생성만 테스트 (Gemini mock)"""
    print("\n=== [Mock 테스트] 일기 생성 ===")

    diary_input = DiaryInput(
        date="2026년 4월 14일 화요일",
        user_memo="대학 동기 만나서 한강까지 걸었다",
        mood="설레는",
    )

    tones = ["담담한 일상체", "감성적인 문체", "유머러스한 문체"]

    for tone in tones:
        print(f"\n--- 톤: {tone} ---")
        diary = await generate_diary_with_gpt4o(diary_input, MOCK_ANALYSES, tone=tone)
        print(diary)
        print()


async def test_full_pipeline_mocked():
    """Gemini 호출을 mock으로 대체해서 전체 파이프라인 테스트"""
    print("\n=== [Mock 테스트] 전체 파이프라인 ===")

    diary_input = DiaryInput(
        date="2026년 4월 14일 화요일",
        photos=[a.meta for a in MOCK_ANALYSES],  # 메타데이터만 넘김
        user_memo="대학 동기 만나서 한강까지 걸었다",
        mood="설레는",
    )

    # analyze_all_photos를 mock으로 대체
    async def mock_analyze_all(photos):
        print("  [Mock] Gemini 분석 건너뜀 (mock 데이터 사용)")
        return MOCK_ANALYSES

    with patch("pipeline.analyze_all_photos", side_effect=mock_analyze_all):
        result = await run_pipeline(diary_input, tone="담담한 일상체")

    with open("./mock_diary_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("결과 저장: mock_diary_result.json")


if __name__ == "__main__":
    import sys

    mode = sys.argv[1] if len(sys.argv) > 1 else "diary"

    if mode == "diary":
        # GPT-4o 일기 생성만 (빠른 품질 확인)
        asyncio.run(test_diary_generation_only())
    elif mode == "full":
        # 전체 파이프라인 (Gemini mock)
        asyncio.run(test_full_pipeline_mocked())
    else:
        print("Usage: python mock_test.py [diary|full]")