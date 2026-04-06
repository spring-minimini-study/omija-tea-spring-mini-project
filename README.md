# 📸 하루한장 — 하루를 사진으로 모으고, AI가 일기로 완성하는 앱

## 1. 서비스 개요

| 항목 | 내용 |
|------|------|
| 서비스명 | **하루한장** (가칭) |
| 한줄 소개 | 하루 동안 사진을 모으면, AI가 그날의 일기를 써주는 앱 |
| 핵심 가치 | "기록은 최소로, 추억은 최대로" |
| 타겟 유저 | 일기를 쓰고 싶지만 귀찮은 사람, 사진은 자주 찍는 사람 |
| 기술 스택 | Flutter (클라이언트) + Java/Spring Boot (서버) |

---

## 2. 핵심 Pain Point & Solution

### 문제
- 나이가 들수록 기억력이 흐려진다
- 일기를 쓰고 싶지만 매일 긴 글을 쓰는 건 부담스럽다
- 사진첩에 사진은 수백 장인데, 정리도 안 되고 맥락도 없다

### 해결
- 하루에 **3~4장의 사진**을 시간대별로 모은다
- 낮에는 **푸시 알림**으로 사진 촬영을 유도한다
- 밤에 앱을 열면 모인 사진들을 확인하고 **한 줄 메모**만 추가한다
- AI가 여러 장의 사진 + 메타데이터 + 메모를 조합하여 **하루의 서사가 담긴 일기**를 생성한다

---

## 3. 핵심 사용 플로우

### 하루 타임라인

```
 ☀️ 아침 (9:00)                  🔔 푸시: "좋은 아침! 오늘 첫 순간을 남겨보세요"
    │                              → 유저: 출근길 사진 촬영 📷
    │
 🍚 점심 (12:30)                 🔔 푸시: "점심은 뭐 드셨어요?"
    │                              → 유저: 점심 사진 촬영 📷
    │
 🌆 오후 (17:00)                 🔔 푸시: "오후에 인상 깊은 순간이 있었나요?"
    │                              → 유저: 퇴근길/카페 사진 촬영 📷
    │
 🌙 저녁 (21:00)                 🔔 푸시: "오늘 하루를 마무리해볼까요? 📖"
    │                              → 유저: 앱 진입
    │                              → 모인 사진 3장 확인
    │                              → 한 줄 메모 추가
    │                              → ✨ AI 일기 생성
    ▼
 📝 오늘의 일기 완성!
```

### 핵심 포인트
- 낮에는 **사진 촬영만** (10초면 끝, 부담 없음)
- 밤에는 **일기 마무리만** (사진 확인 + 한 줄 메모 + 생성 버튼)
- 하루에 앱과 **3~4번 접점** → 자연스러운 리텐션
- 사진마다 시간대가 달라 AI가 **하루의 흐름을 서사로** 구성 가능

---

## 4. MVP 기능 정의

### 4.1 🔔 푸시 알림 & 사진 수집

하루 동안 시간대별로 푸시 알림을 보내 사진 촬영을 유도한다.

**푸시 스케줄 (기본 설정):**

| 시간대 | 기본 시각 | 프롬프트 예시 |
|--------|----------|-------------|
| 아침 | 09:00 | "좋은 아침! 오늘의 첫 순간을 남겨보세요 ☀️" |
| 점심 | 12:30 | "점심은 뭐 드셨어요? 📸" |
| 오후 | 17:00 | "오후에 인상 깊은 순간이 있었나요?" |
| 저녁 (마무리) | 21:00 | "오늘 하루를 마무리해볼까요? 📖" |

**규칙:**
- 아침/점심/오후 푸시: 탭하면 **카메라 or 갤러리 선택** 화면으로 바로 이동
- 저녁 푸시: 탭하면 **일기 작성 화면**으로 이동
- 푸시 시각은 유저가 **설정에서 커스터마이징** 가능
- 사진은 하루 **최대 4장**까지 등록 가능
- 푸시를 무시해도 OK — 밤에 갤러리에서 직접 골라도 됨

### 4.2 📷 사진 업로드 & 메타데이터 추출

푸시를 통해 또는 갤러리에서 선택한 사진을 서버에 업로드한다.

**추출하는 메타데이터:**

| 항목 | 출처 | 예시 |
|------|------|------|
| 촬영 일시 | EXIF | 2026-04-06 12:34 |
| 촬영 위치 (위경도) | EXIF GPS | 37.5665, 126.9780 |
| 장소명 | Reverse Geocoding API | 서울 종로구 세종대로 |
| 날씨 | Weather API (위치+시간 기반) | 맑음, 18°C |

**사진 업로드 시점:**
- 사진 선택 즉시 서버에 업로드 (백그라운드)
- 메타데이터 추출 + AI 사진 분석도 이 시점에 비동기 처리
- 밤에 일기 쓸 때는 이미 분석이 끝나 있어 대기 시간 없음

### 4.3 🤖 AI 사진 분석

서버에서 Vision AI를 통해 각 사진을 분석한다.

**분석 항목 (사진당):**

| 항목 | 설명 | 예시 |
|------|------|------|
| 장면 설명 | 사진 속 상황 묘사 | "카페에서 라떼를 마시고 있다" |
| 분위기/감정 | 사진의 전반적 무드 | 편안한, 활기찬, 쓸쓸한 |
| 핵심 키워드 | 주요 사물/장소/행동 | 카페, 라떼, 노트북, 오후 |
| 인원 수 | 혼자/둘/여럿 | 2명 |
| 활동 | 주요 활동 | 식사, 산책, 업무, 운동 |

### 4.4 ✏️ 일기 마무리 (한 줄 메모 + 생성)

저녁에 앱을 열면 오늘 모은 사진들을 타임라인으로 보여준다.

- 각 사진에 시간, 장소가 자동 표시됨
- 유저는 전체에 대한 **한 줄 메모** 작성 (선택사항, 최대 100자)
- "일기 만들기" 버튼으로 AI 일기 생성
- 사진이 0장이면 일기 작성 불가 (최소 1장 필요)

### 4.5 📝 AI 일기 생성

여러 장의 사진 분석 결과를 **시간순으로 조합**하여 하루의 서사를 구성한다.

**AI에게 전달되는 컨텍스트:**

```
- 날짜: 2026년 4월 6일 월요일

[사진 1 — 오전 8:42]
- 장소: 서울 마포구 합정역 근처
- 날씨: 맑음, 14°C
- 사진 분석: 지하철역 앞 벚꽃이 만개한 거리, 상쾌한 분위기

[사진 2 — 오후 12:31]
- 장소: 서울 종로구 광화문 근처
- 날씨: 맑음, 18°C
- 사진 분석: 카페에서 두 사람이 라떼를 마시며 대화, 편안한 분위기

[사진 3 — 오후 6:15]
- 장소: 서울 용산구 한강공원
- 날씨: 맑음, 16°C
- 사진 분석: 한강 둔치에서 석양을 바라보는 모습, 여유로운 분위기

- 유저 메모: "대학 동기 만나서 한강까지 걸었다"
```

**생성되는 일기 예시:**

> 4월 6일 월요일, 맑음
>
> 아침에 출근하는데 합정역 근처 벚꽃이 만개해 있었다.
> 올해도 꽃이 피었구나 싶었다.
> 점심엔 오랜만에 대학 동기를 만나 광화문 카페에서 라떼를 마셨다.
> 얘기가 끝이 없어서 결국 한강까지 같이 걸었다.
> 석양이 예뻤고, 이런 날이 또 있을까 싶었다.
> 바쁘다는 핑계로 미루지 말고 자주 만나야지.

**일기 톤 옵션 (MVP에서는 기본 1개, 추후 확장):**
- 담담한 일상체 (기본)
- 감성적인 문체
- 유머러스한 문체

### 4.6 📅 캘린더 뷰 (일기 모아보기)

- 월별 캘린더에 **대표 사진 썸네일**이 표시된다 (첫 번째 사진 or 유저 지정)
- 날짜를 탭하면 해당 날의 일기를 볼 수 있다
- 작성하지 않은 날은 비어있다 (압박 없이)

### 4.7 📖 일기 상세 보기 & 수정

- 사진 **가로 스크롤 캐러셀** + AI 생성 일기 + 메타정보를 한 화면에 표시
- 각 사진 아래에 시간/장소 표시
- AI가 쓴 일기를 유저가 자유롭게 수정 가능
- 수정 이력은 AIGenerationHistory에 보관

---

## 5. 추가 기능 제안 (Post-MVP)

MVP 이후 재미와 리텐션을 위해 추가할 만한 기능들:

### 🔁 N년 전 오늘 (리텐션 핵심)
- "1년 전 오늘 이런 일이 있었어요" 푸시 알림
- 과거 일기 + 사진을 다시 보여줌
- 타임캡슐 느낌으로 감성 자극

### 📊 월간/연간 리포트
- AI가 한 달치 일기를 분석하여 요약
- "이번 달 가장 많이 간 장소", "감정 흐름", "자주 만난 사람" 등
- 연말에 "올해의 하루한장" 연간 리포트 생성

### 🗺️ 추억 지도
- 일기를 쓴 장소를 지도 위에 핀으로 표시
- 핀을 탭하면 해당 장소에서의 일기들 모아보기
- "나는 주로 어디서 시간을 보내는가" 시각화

### 🎨 포토북 내보내기
- 월별/연별로 사진+일기를 예쁜 레이아웃으로 PDF 생성
- 실제 포토북 인쇄 서비스 연동 가능

### 🔥 연속 기록 (Streak)
- GitHub 잔디처럼 연속 작성일 시각화
- 연속 기록 깨지기 전 리마인더 푸시

### 💬 AI 질문
- "지난달에 뭐했더라?", "마지막으로 OO 만난 게 언제야?"
- 내 일기 데이터를 기반으로 AI가 답변

---

## 6. 화면 플로우 (MVP)

```
[앱 실행]
    │
    ▼
[홈 - 캘린더 뷰] ◄──────────────────────────────────┐
    │                                                 │
    ├─ 오늘 날짜 탭 ──▶ [오늘의 타임라인]                    │
    │                      │                          │
    │                      ├─ 사진 부족 ──▶ [사진 추가]      │
    │                      │               (카메라/갤러리)  │
    │                      │                          │
    │                      ├─ 사진 있음 ──▶ [사진 타임라인 확인] │
    │                      │                   │       │
    │                      │                   ▼       │
    │                      │             [한 줄 메모 입력]  │
    │                      │                   │       │
    │                      │                   ▼       │
    │                      │             [AI 일기 생성 ⏳]  │
    │                      │                   │       │
    │                      │                   ▼       │
    │                      │             [일기 완성! 미리보기]│
    │                      │                   │       │
    │                      │                   ├─ 수정   │
    │                      │                   ├─ 재생성  │
    │                      │                   └─ 저장 ──┘
    │                      │
    │                      └─ 이미 작성됨 ──▶ [일기 상세 보기]
    │
    ├─ 과거 날짜 탭 ──▶ [일기 상세 보기]
    │                      │
    │                      ├─ 수정
    │                      └─ 삭제
    │
    └─ 설정 ⚙️ ──▶ [설정 화면]
                      ├─ 푸시 알림 시각 설정
                      ├─ 일기 문체 설정
                      └─ 알림 ON/OFF


[푸시 알림 탭] (아침/점심/오후)
    │
    ▼
[빠른 사진 등록]
    ├─ 카메라로 촬영
    └─ 갤러리에서 선택
    │
    ▼
[업로드 완료! 앱 종료] ──▶ (백그라운드: 메타데이터 추출 + AI 분석)
```

---

## 7. 화면 상세 와이어프레임

### 7.1 홈 (캘린더 뷰)

```
┌──────────────────────────────┐
│  하루한장             ⚙️      │
│──────────────────────────────│
│        ◀  2026년 4월  ▶       │
│──────────────────────────────│
│  일   월   화   수   목   금   토 │
│            1    2    3    4   │
│          [📷] [📷]   ·    ·   │
│  5    6    7    8    9   10  11│
│  ·   [+]   ·    ·    ·    ·   · │
│ 12   13   14   15   16   17  18│
│  ·    ·    ·    ·    ·    ·   · │
│──────────────────────────────│
│                              │
│  🔥 3일 연속 작성 중!           │
│                              │
│  오늘의 사진: 2/4장 수집됨       │
│  ┌──────────────────────────┐│
│  │   📷 사진 추가하기 (+)       ││
│  └──────────────────────────┘│
│                              │
└──────────────────────────────┘
```

### 7.2 빠른 사진 등록 (푸시 탭 진입)

```
┌──────────────────────────────┐
│  ×                           │
│──────────────────────────────│
│                              │
│     📸 지금 이 순간을 남겨보세요   │
│                              │
│  ┌────────────┐ ┌────────────┐│
│  │            │ │            ││
│  │   📷       │ │   🖼️       ││
│  │  카메라     │ │  갤러리     ││
│  │            │ │            ││
│  └────────────┘ └────────────┘│
│                              │
│  오늘 등록한 사진 (2/4)         │
│  ┌────┐ ┌────┐               │
│  │ 📷 │ │ 📷 │               │
│  │8:42│ │12:31│              │
│  └────┘ └────┘               │
│                              │
└──────────────────────────────┘
```

### 7.3 일기 작성 — 오늘의 타임라인

```
┌──────────────────────────────┐
│  ← 오늘의 기록                 │
│──────────────────────────────│
│                              │
│  2026년 4월 6일 월요일          │
│  ☀️ 맑음 · 14~18°C            │
│                              │
│  ── 타임라인 ─────────────────  │
│                              │
│  🕗 08:42                     │
│  ┌──────────────────────────┐│
│  │     [벚꽃 사진]            ││
│  └──────────────────────────┘│
│  📍 서울 마포구 합정역 근처       │
│                              │
│  🕐 12:31                     │
│  ┌──────────────────────────┐│
│  │     [카페 사진]            ││
│  └──────────────────────────┘│
│  📍 서울 종로구 광화문 근처       │
│                              │
│  🕕 18:15                     │
│  ┌──────────────────────────┐│
│  │     [한강 석양 사진]        ││
│  └──────────────────────────┘│
│  📍 서울 용산구 한강공원         │
│                              │
│  ┌──────────────────────────┐│
│  │ 오늘 하루를 한 줄로 남겨보세요  ││
│  │                     0/100││
│  └──────────────────────────┘│
│                              │
│  ┌──────────────────────────┐│
│  │      ✨ 일기 만들기         ││
│  └──────────────────────────┘│
│                              │
└──────────────────────────────┘
```

### 7.4 일기 완성 뷰

```
┌──────────────────────────────┐
│  ← 2026.04.06 (월)     ✏️ 🗑️ │
│──────────────────────────────│
│                              │
│  ┌────────────────────────┐  │
│  │ [📷1] ← swipe → [📷2] │  │
│  │     사진 캐러셀 (3장)    │  │
│  │       · · ●            │  │
│  └────────────────────────┘  │
│                              │
│  ☀️ 맑음 14~18°C              │
│  📍 합정 → 광화문 → 한강공원     │
│                              │
│  ──────────────────────────  │
│                              │
│  아침에 출근하는데 합정역 근처     │
│  벚꽃이 만개해 있었다.           │
│  올해도 꽃이 피었구나 싶었다.     │
│  점심엔 오랜만에 대학 동기를      │
│  만나 광화문 카페에서 라떼를      │
│  마셨다. 얘기가 끝이 없어서      │
│  결국 한강까지 같이 걸었다.      │
│  석양이 예뻤고, 이런 날이       │
│  또 있을까 싶었다.              │
│                              │
│  ──────────────────────────  │
│  💬 "대학 동기 만나서 한강까지    │
│      걸었다"                  │
│  ──────────────────────────  │
│  #벚꽃 #카페 #한강 #동기        │
│                              │
│  ┌──────────────────────────┐│
│  │     🔄 다시 쓰기           ││
│  └──────────────────────────┘│
│                              │
└──────────────────────────────┘
```

---

## 8. 시스템 아키텍처

```
┌─────────────────┐              ┌───────────────────────────┐
│     Flutter      │              │      Spring Boot API       │
│    (Client)      │◄────REST────▶│                           │
│                  │              │  ┌─────────────────────┐   │
│ • 카메라/갤러리    │              │  │ AuthService         │   │
│ • 푸시 수신       │              │  │ PhotoService        │   │
│ • 캘린더 뷰       │              │  │ DiaryService        │   │
│ • 일기 뷰/편집    │              │  │ AIService           │   │
│                  │              │  │ NotificationService │   │
└─────────────────┘              │  │ LocationService     │   │
        │                        │  │ WeatherService      │   │
        │                        │  └─────────────────────┘   │
        │                        └─────────────┬───────────────┘
        │                                      │
   ┌────▼─────┐           ┌────────────────────┼────────────────────┐
   │  FCM     │           │                    │                    │
   │ (Push)   │           ▼                    ▼                    ▼
   └──────────┘     ┌──────────┐         ┌──────────┐        ┌──────────┐
                    │PostgreSQL│         │ S3/MinIO │        │ External │
                    │          │         │          │        │  APIs    │
                    │ • User   │         │ • 원본사진 │        │          │
                    │ • Diary  │         │ • 썸네일   │        │ • AI     │
                    │ • Photo  │         │          │        │   Vision │
                    │ • Tag    │         └──────────┘        │ • AI LLM │
                    │ • Mood   │                             │ • Geocode│
                    │ • Streak │                             │ • Weather│
                    │ • etc.   │                             │ • FCM    │
                    └──────────┘                             └──────────┘
```

### 사진 업로드 → 일기 생성 비동기 파이프라인

```
[유저: 사진 촬영/선택]
        │
        ▼
[Flutter: 사진 업로드 API 호출] ──────────────────────────────┐
        │                                                    │
        ▼                                                    ▼
[Spring: S3 업로드]                               [Spring: 비동기 처리 시작]
        │                                            │
        ├─ 즉시 응답 (photo_id, status: PROCESSING)    │
        │                                            │
        │                              ┌─────────────┼─────────────┐
        │                              ▼             ▼             ▼
        │                        [EXIF 추출]   [Reverse Geo]  [Weather API]
        │                              │             │             │
        │                              ▼             ▼             ▼
        │                        [Vision AI 분석]                   │
        │                              │                           │
        │                              ▼                           │
        │                     [Photo 레코드 업데이트]                 │
        │                     status: READY                        │
        │                                                          │
        ▼                                                          │
[밤: 유저가 "일기 만들기" 탭]                                         │
        │                                                          │
        ▼                                                          │
[Spring: 오늘의 Photo들 (status=READY) 조회]◄──────────────────────┘
        │
        ▼
[AI에게 전체 컨텍스트 전달 → 일기 생성]
        │
        ▼
[Diary 레코드 생성 + 응답]
```

---

## 9. API 설계 (MVP)

### 9.1 인증

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/v1/auth/signup` | 회원가입 |
| POST | `/api/v1/auth/login` | 로그인 (JWT 발급) |
| POST | `/api/v1/auth/refresh` | 토큰 갱신 |

### 9.2 사진 (Photo) — 낮에 사용

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/v1/photos` | 사진 업로드 (multipart + EXIF 메타 자동 추출) |
| GET | `/api/v1/photos?date=2026-04-06` | 특정 날짜의 사진 목록 조회 |
| GET | `/api/v1/photos/{id}` | 사진 상세 (분석 결과 포함) |
| DELETE | `/api/v1/photos/{id}` | 사진 삭제 |
| GET | `/api/v1/photos/{id}/status` | 사진 분석 상태 확인 (PROCESSING/READY/FAILED) |

### 9.3 일기 (Diary) — 밤에 사용

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/v1/diaries` | 일기 생성 (date + memo → AI 일기 생성 트리거) |
| GET | `/api/v1/diaries?year=2026&month=4` | 월별 일기 목록 (캘린더 뷰용) |
| GET | `/api/v1/diaries/{id}` | 일기 상세 조회 (사진 + 일기 + 태그 + 감정) |
| PUT | `/api/v1/diaries/{id}` | 일기 수정 (본문 편집) |
| DELETE | `/api/v1/diaries/{id}` | 일기 삭제 |

### 9.4 AI 생성

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/v1/ai/analyze-photo/{photoId}` | 사진 분석 요청 (보통 자동 트리거) |
| POST | `/api/v1/ai/generate-diary` | 일기 생성 요청 (date + memo) |
| POST | `/api/v1/ai/regenerate-diary/{diaryId}` | 일기 재생성 (이전 버전 히스토리 보관) |

### 9.5 설정 & 알림

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/v1/users/me/preferences` | 유저 설정 조회 |
| PUT | `/api/v1/users/me/preferences` | 유저 설정 수정 (푸시 시각, 문체 등) |
| PUT | `/api/v1/users/me/fcm-token` | FCM 토큰 등록/갱신 |

### 9.6 통계

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/v1/stats/streak` | 연속 작성 기록 조회 |
| GET | `/api/v1/stats/mood?year=2026&month=4` | 월별 감정 통계 |

---

## 10. 데이터 모델 (ERD)

### 테이블 관계도

```
User (1) ──── (N) Diary
  │                  │
  │                  ├──── (N) Photo ──── (1) Location
  │                  │         │
  │                  │         └──── (N) PhotoTag ──── (1) Tag
  │                  │
  │                  ├──── (1) Mood
  │                  │
  │                  └──── (N) AIGenerationHistory
  │
  ├──── (1) UserPreference
  │
  ├──── (N) Notification
  │
  └──── (1) Streak
```

---

### User
```sql
CREATE TABLE users (
    id              BIGSERIAL PRIMARY KEY,
    email           VARCHAR(255) UNIQUE NOT NULL,
    password        VARCHAR(255) NOT NULL,        -- BCrypt
    nickname        VARCHAR(50) NOT NULL,
    profile_image   VARCHAR(500),                 -- S3 URL
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### UserPreference
```sql
CREATE TABLE user_preferences (
    id                      BIGSERIAL PRIMARY KEY,
    user_id                 BIGINT UNIQUE REFERENCES users(id),

    -- 푸시 알림 설정
    push_enabled            BOOLEAN DEFAULT TRUE,
    push_morning_time       TIME DEFAULT '09:00',
    push_lunch_time         TIME DEFAULT '12:30',
    push_afternoon_time     TIME DEFAULT '17:00',
    push_evening_time       TIME DEFAULT '21:00',

    -- 일기 설정
    diary_tone              VARCHAR(20) DEFAULT 'casual',
    -- casual(담담), emotional(감성), humorous(유머)

    -- 디바이스
    fcm_token               VARCHAR(500),
    timezone                VARCHAR(50) DEFAULT 'Asia/Seoul',

    created_at              TIMESTAMP DEFAULT NOW(),
    updated_at              TIMESTAMP DEFAULT NOW()
);
```

### Location
```sql
CREATE TABLE locations (
    id              BIGSERIAL PRIMARY KEY,
    latitude        DOUBLE PRECISION NOT NULL,
    longitude       DOUBLE PRECISION NOT NULL,
    address         VARCHAR(500),                 -- 전체 주소
    place_name      VARCHAR(200),                 -- 간략 장소명 (ex: "합정역")
    city            VARCHAR(100),                 -- 시/도
    district        VARCHAR(100),                 -- 구/군
    created_at      TIMESTAMP DEFAULT NOW(),

    -- 같은 위치 재사용을 위한 근접 검색 (PostGIS 확장 시)
    UNIQUE (latitude, longitude)
);
```

### Photo
```sql
CREATE TABLE photos (
    id              BIGSERIAL PRIMARY KEY,
    user_id         BIGINT REFERENCES users(id),
    diary_id        BIGINT REFERENCES diaries(id),   -- 일기 생성 전에는 NULL
    location_id     BIGINT REFERENCES locations(id),

    -- 사진 파일
    photo_url       VARCHAR(500) NOT NULL,        -- S3 원본
    thumbnail_url   VARCHAR(500),                 -- S3 썸네일

    -- EXIF 메타데이터
    taken_at        TIMESTAMP NOT NULL,           -- 촬영 시간
    photo_date      DATE NOT NULL,                -- 촬영 날짜 (조회 편의)

    -- 날씨 (촬영 시점)
    weather         VARCHAR(50),                  -- 맑음, 흐림, 비 등
    temperature     DOUBLE PRECISION,             -- 기온 (°C)

    -- AI 분석 결과
    analysis_status VARCHAR(20) DEFAULT 'PENDING',
    -- PENDING → PROCESSING → READY → FAILED
    photo_analysis  JSONB,
    -- {
    --   "scene": "카페에서 라떼를 마시고 있다",
    --   "mood": "편안한",
    --   "keywords": ["카페", "라떼", "대화"],
    --   "people_count": 2,
    --   "activity": "식사"
    -- }

    -- 정렬
    display_order   INT DEFAULT 0,                -- 같은 날 사진 정렬 순서

    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_photos_user_date ON photos(user_id, photo_date);
```

### Diary
```sql
CREATE TABLE diaries (
    id              BIGSERIAL PRIMARY KEY,
    user_id         BIGINT REFERENCES users(id),
    diary_date      DATE NOT NULL,

    -- 일기 내용
    user_memo       VARCHAR(100),                 -- 유저 한 줄 메모
    ai_content      TEXT,                         -- AI 최초 생성 일기
    content         TEXT,                         -- 최종 일기 (유저 수정 반영)
    is_edited       BOOLEAN DEFAULT FALSE,

    -- 대표 사진 (캘린더 썸네일용)
    cover_photo_id  BIGINT REFERENCES photos(id),

    -- 하루 종합 날씨
    weather_summary VARCHAR(50),                  -- 대표 날씨
    temp_high       DOUBLE PRECISION,
    temp_low        DOUBLE PRECISION,

    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW(),

    UNIQUE (user_id, diary_date)                  -- 하루 1개 제한
);
```

### Tag & PhotoTag
```sql
CREATE TABLE tags (
    id              BIGSERIAL PRIMARY KEY,
    name            VARCHAR(50) UNIQUE NOT NULL,  -- 정규화된 태그명
    category        VARCHAR(30),                  -- place, food, activity, object, etc.
    usage_count     INT DEFAULT 0,                -- 사용 횟수 (인기 태그용)
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE photo_tags (
    id              BIGSERIAL PRIMARY KEY,
    photo_id        BIGINT REFERENCES photos(id) ON DELETE CASCADE,
    tag_id          BIGINT REFERENCES tags(id),
    confidence      DOUBLE PRECISION,             -- AI 분석 신뢰도 (0.0 ~ 1.0)

    UNIQUE (photo_id, tag_id)
);

CREATE INDEX idx_photo_tags_tag ON photo_tags(tag_id);
```

### Mood
```sql
CREATE TABLE moods (
    id              BIGSERIAL PRIMARY KEY,
    diary_id        BIGINT UNIQUE REFERENCES diaries(id) ON DELETE CASCADE,

    -- AI가 분석한 하루 전체 감정
    primary_mood    VARCHAR(30) NOT NULL,         -- 주요 감정 (편안한, 즐거운, 우울한 등)
    mood_score      INT CHECK (mood_score BETWEEN 1 AND 5),
    -- 1: 매우 부정 ~ 5: 매우 긍정
    mood_keywords   JSONB,                        -- ["편안한", "여유로운", "행복한"]

    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_moods_diary ON moods(diary_id);
```

### AIGenerationHistory
```sql
CREATE TABLE ai_generation_histories (
    id              BIGSERIAL PRIMARY KEY,
    diary_id        BIGINT REFERENCES diaries(id) ON DELETE CASCADE,

    version         INT NOT NULL,                 -- 1, 2, 3... (재생성 횟수)
    generated_content TEXT NOT NULL,              -- AI가 생성한 일기 내용
    prompt_used     TEXT,                         -- 사용된 프롬프트 (디버깅/개선용)
    model_version   VARCHAR(50),                  -- 사용된 AI 모델 버전

    -- 입력 컨텍스트 스냅샷 (당시 사진 분석 결과 등)
    input_context   JSONB,

    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_ai_history_diary ON ai_generation_histories(diary_id);
```

### Streak
```sql
CREATE TABLE streaks (
    id                  BIGSERIAL PRIMARY KEY,
    user_id             BIGINT UNIQUE REFERENCES users(id),

    current_streak      INT DEFAULT 0,            -- 현재 연속 일수
    longest_streak      INT DEFAULT 0,            -- 최장 연속 일수
    total_diary_count   INT DEFAULT 0,            -- 총 작성 일기 수
    last_diary_date     DATE,                     -- 마지막 일기 작성일

    updated_at          TIMESTAMP DEFAULT NOW()
);
```

### Notification
```sql
CREATE TABLE notifications (
    id              BIGSERIAL PRIMARY KEY,
    user_id         BIGINT REFERENCES users(id),

    type            VARCHAR(30) NOT NULL,
    -- PHOTO_REMIND: 사진 촬영 리마인더
    -- DIARY_REMIND: 일기 작성 리마인더
    -- STREAK_WARN: 연속 기록 위험 알림
    -- MEMORY: N년 전 오늘 (Post-MVP)

    title           VARCHAR(200),
    body            VARCHAR(500),
    sent_at         TIMESTAMP NOT NULL,
    is_read         BOOLEAN DEFAULT FALSE,
    read_at         TIMESTAMP,

    -- 연관 데이터
    related_diary_id  BIGINT REFERENCES diaries(id),
    related_photo_id  BIGINT REFERENCES photos(id),

    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_notifications_user ON notifications(user_id, sent_at DESC);
```

---

## 11. AI 프롬프트 설계

### 사진 분석 프롬프트 (Vision API, 사진당 1회)

```
이 사진을 분석해서 아래 JSON 형식으로 응답해주세요.

{
  "scene": "사진 속 장면을 한 문장으로 설명",
  "mood": "사진의 전반적인 분위기 (예: 편안한, 활기찬, 쓸쓸한, 즐거운)",
  "keywords": ["핵심 키워드", "최대 5개"],
  "people_count": 0,
  "activity": "주요 활동 (예: 식사, 산책, 업무, 운동)",
  "time_of_day": "추정 시간대 (아침/점심/오후/저녁/밤)"
}
```

### 일기 생성 프롬프트 (여러 사진 조합)

```
당신은 사용자의 하루를 기록하는 일기 작가입니다.
아래 정보를 바탕으로 자연스럽고 담담한 일기를 작성해주세요.

[오늘의 정보]
- 날짜: {diary_date} ({요일})
- 전체 날씨: {weather_summary}

[시간순 기록]

{photos를 시간순 정렬하여 반복}
--- 기록 {n} ({taken_at 시각}) ---
- 시간: {taken_at}
- 장소: {location.place_name} ({location.district})
- 날씨: {weather}, {temperature}°C
- 사진 속 장면: {photo_analysis.scene}
- 분위기: {photo_analysis.mood}
- 키워드: {photo_analysis.keywords}
- 함께한 사람 수: {photo_analysis.people_count}명
{/반복}

- 유저 메모: {user_memo} (없으면 "없음")

[작성 규칙]
- 여러 시간대의 기록을 시간 흐름에 따라 자연스럽게 연결해주세요
- 5~8문장, 200~300자 내외
- 반말 일기체 사용 (~했다, ~였다)
- 하루의 서사가 느껴지도록 아침→점심→저녁 흐름을 살려주세요
- 감정이나 생각을 자연스럽게 섞어주세요
- 유저 메모가 있다면 그 내용을 핵심 테마로 작성
- 유저 메모가 없다면 사진 분석 결과만으로 작성
- 마지막에 하루를 마무리하는 짧은 감상 한 줄을 넣어주세요
```

### 감정 분석 프롬프트 (일기 생성 후 자동)

```
아래 일기를 읽고 오늘 하루의 감정을 분석해주세요.

[일기]
{content}

아래 JSON 형식으로 응답해주세요.
{
  "primary_mood": "가장 주된 감정 (한 단어)",
  "mood_score": 1~5 사이 정수 (1: 매우 부정, 3: 보통, 5: 매우 긍정),
  "mood_keywords": ["감정 키워드", "최대 3개"]
}
```

---

## 12. MVP 개발 마일스톤

### Phase 1 — 기반 구축 (1주)
- [ ] Spring Boot 프로젝트 세팅 (JPA, Security, S3, FCM)
- [ ] Flutter 프로젝트 세팅 (카메라, 갤러리, 푸시)
- [ ] DB 스키마 생성 (전체 테이블)
- [ ] 회원가입/로그인 API + 화면
- [ ] FCM 토큰 등록

### Phase 2 — 사진 수집 파이프라인 (2주)
- [ ] 사진 업로드 API + S3 연동
- [ ] EXIF 메타데이터 추출
- [ ] Reverse Geocoding 연동 (위경도 → 장소명)
- [ ] Weather API 연동 (촬영 시점 날씨)
- [ ] AI 사진 분석 연동 (비동기 처리)
- [ ] 썸네일 생성
- [ ] 푸시 알림 스케줄러 (아침/점심/오후/저녁)

### Phase 3 — 일기 생성 & 관리 (1.5주)
- [ ] AI 일기 생성 API (다중 사진 컨텍스트 조합)
- [ ] AI 감정 분석 (일기 생성 후 자동)
- [ ] 일기 CRUD API
- [ ] 태그 자동 생성 + 저장
- [ ] AI 재생성 + 히스토리 관리
- [ ] Streak 자동 계산

### Phase 4 — 클라이언트 완성 (1.5주)
- [ ] 빠른 사진 등록 화면 (푸시 탭 → 카메라/갤러리)
- [ ] 오늘의 타임라인 + 메모 입력 화면
- [ ] AI 일기 생성 로딩 + 결과 화면
- [ ] 일기 상세 보기 (사진 캐러셀 + 본문)
- [ ] 일기 수정 화면
- [ ] 캘린더 뷰 (월별, 썸네일 표시)
- [ ] 설정 화면 (푸시 시각, 문체)

### Phase 5 — 마무리 (1주)
- [ ] UI 다듬기 + 로딩/에러 처리
- [ ] 오프라인 대응 (사진 로컬 큐잉)
- [ ] Streak 시각화
- [ ] 감정 캘린더 (무드 컬러)
- [ ] 테스트 + 버그 수정

**총 예상 기간: 약 7주 (토이 프로젝트 페이스)**

---

## 13. 기술 선택 메모

| 영역 | 선택 | 이유 |
|------|------|------|
| 클라이언트 | Flutter | iOS/Android 동시 지원, 빠른 UI 개발 |
| 백엔드 | Spring Boot 3.x | Java 생태계, 안정성, 비동기 처리 |
| DB | PostgreSQL | JSONB 지원, PostGIS 확장 가능, 인덱싱 |
| 파일 저장 | AWS S3 (or MinIO) | 사진 저장, CDN 연동, 썸네일 분리 저장 |
| 비동기 처리 | Spring @Async + ThreadPool | 사진 분석 비동기 파이프라인 |
| 푸시 알림 | Firebase Cloud Messaging (FCM) | Flutter 공식 지원, 무료 |
| AI (Vision) | Claude Vision / GPT-4o | 사진 분석용 |
| AI (Text) | Claude / GPT-4o | 일기 + 감정 분석용 |
| 위치 변환 | Kakao Maps API (or Google) | 한국 주소 정확도 높음 |
| 날씨 | OpenWeatherMap (or 기상청 API) | 과거 날씨 조회 가능 |
| 인증 | JWT (Access + Refresh) | 모바일 앱 표준 |
| 이미지 처리 | 서버: Thumbnailator / imgscalr | EXIF 추출 + 리사이징 |
| 스케줄러 | Spring @Scheduled | 푸시 알림 발송 배치 |
