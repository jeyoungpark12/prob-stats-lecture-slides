---
name: lecture-slides
description: 교과서 PDF를 바탕으로 강의 슬라이드(.pptx)를 만드는 워크플로. manim 애니메이션 영상, 인터넷(Wikimedia Commons)에서 찾은 비유 사진, 발표자 노트, 요약·퀴즈까지 넣은 PowerPoint 파일을 lectures/ 폴더에 저장. 사용자가 강의자료, 수업 슬라이드, PPT, 차시/주차/단원 자료, "N주차 만들어줘", "이 단원 슬라이드", 기존 강의자료 수정·추가를 말하면 형식을 명시하지 않아도 반드시 이 스킬 사용.
---

# 강의 슬라이드 제작

교과서 내용을 그림·애니메이션 중심의 PowerPoint 강의자료로 바꾸는 과정. 수업 정보와 누적된 취향은
프로젝트 루트의 `CLAUDE.md`에 있고, 이 스킬은 그 규칙을 지키며 매번 같은 품질로 만드는 방법을 담고 있음.

## 0. 시작 전 확인

1. 프로젝트 루트 `CLAUDE.md`를 읽기. 특히 **피드백 누적** 항목은 사용자가 이전에 고친 내용이라 최우선 반영.
2. 이번에 만들 범위(단원·차시)를 확인. 사용자가 말하지 않았으면 교과서 목차를 보고 다음 차시를 제안.
3. 작업 폴더: `lectures/weekNN_주제/` (없으면 `images/`, `animations/`, `output/`와 함께 생성).

## 1. 교과서 읽기

```bash
python <skill>/scripts/extract_pdf.py "sources/<교과서>.pdf" <작업폴더>/_textbook
python <skill>/scripts/extract_pdf.py "sources/<교과서>.pdf" <작업폴더>/_textbook --render 4-8
```

- 첫 줄은 전체 텍스트를 `text.txt`로 추출. 한글 교과서 PDF는 **숫자·수식·기호가 깨지는 경우가 많음**
  (예: "9"가 X, "1	9" 가 P(X…)). 텍스트로는 개념 흐름만 파악하고, 숫자·수식·예제가 필요한 쪽은
  `--render`로 PNG를 만들어 Read로 직접 보기. 깨진 텍스트에서 숫자를 추측해 쓰지 말 것.
- 교과서 수치를 확인할 수 없어 직접 만든 예시는 발표자 노트에 "예시 수치"라고 적어 둠.

그다음 `outline.md`를 작성(꼭 넣을 개념, 교과서 쪽수, 예제, 비유 아이디어). 사용자가 이미 써 둔
`outline.md`가 있으면 그것을 따름.

## 2. 슬라이드 구성

기본 흐름(분량은 CLAUDE.md 기준):

1. 표지 → 2. 학습 목표
3. 개념마다 **비유 사진 → 애니메이션 → 정리(표·성질)** 순서. 학생이 일상 경험으로 먼저 감을 잡고,
   움직이는 그림으로 구조를 본 뒤, 마지막에 정식 정의를 보면 이해가 쉬움.
4. 개념 비교(표, 공학 예시) → 마지막 요약 + 퀴즈 3문항(정답은 발표자 노트)

글쓰기 규칙:
- 슬라이드 글은 **명사형 종결** ("표본 평균의 분포", "합은 1"). "~다/~요" 금지. 발표자 노트는 말하는 대본이라 일반 문장.
- 한 슬라이드 한 아이디어, 글머리표 5개 이하. 글보다 그림.
- 공대생 대상이면 공학 예시(불량품 개수, 센서 오차, 부품 수명, 대기열).
- 용어·기호는 교과서 표기를 따름.

좋은 비유의 조건: 학생이 매일 보는 장면이고, 개념의 **구조**가 그대로 대응됨.
예) 확률변수 = 번호표(결과마다 번호 하나), 확률의 합 1 = 피자 한 판, 이산/연속 = 계단/경사로.

## 3. manim 애니메이션

`references/manim.md`를 읽고 작성. 핵심만:
- `animations/scenes.py`에 장면별 클래스. LaTeX가 없으므로 `Text`만 사용(MathTex, 숫자 눈금 Axes, DecimalNumber 금지).
- 렌더링: `manim -r 1920,1080 --fps 30 --disable_caching scenes.py <장면>` 후 `-s`로 마지막 화면 PNG를 만들어 **Read로 확인**하고 겹침·잘림을 고친 뒤 확정.
- 완성본은 `animations/out/<장면>.mp4`와 `<장면>.png`(포스터 이미지)로 복사.

## 4. 비유 사진 찾기

```bash
python <skill>/scripts/commons_fetch.py <scratchpad>/candidates "stairs steps" "whole pizza sliced" ...
```

- 검색어는 **구체적인 영어 장면 묘사**. 스크립트가 자유 라이선스(CC0, CC BY, CC BY-SA, 퍼블릭 도메인)만 받고
  `_sheet.jpg`(한눈에 보기)와 `meta.json`(작가·라이선스)을 만듦. 시트를 Read로 보고 고르기.
- 고른 사진은 `images/<짧은이름>.jpg`로 복사하고 `images/credits.json`에 메타데이터 저장.
  출처 표기는 라이선스 조건이므로 슬라이드 하단에 반드시 넣기.
- 위키미디어는 요청이 많으면 429(요청 제한)를 반환. 스크립트가 자동으로 기다렸다 재시도하므로 오래 걸리면
  백그라운드로 돌리고 그동안 애니메이션 작업.
- 맞는 사진이 없으면 억지로 넣지 말고 검색어를 바꾸거나 그 슬라이드는 애니메이션만 사용.

### AI 생성 영상·이미지 (Google Flow, 사용자가 요청할 때)

인트로 영상이나 실사 사진으로 구하기 어려운 장면(공장 검사, 센서 신호, 표지 배경 등)은 Claude in Chrome으로
Google Flow(https://labs.google/fx/tools/flow → flow.google.com)에서 생성.
- 사용자 계정의 **크레딧을 쓰므로** 생성 전 확인 창에서 비용(예: 영상 1개 12 크레딧)을 사용자에게 알리고, 요청 범위 안에서만 "승인"(항상 승인 X).
- 프롬프트는 영어 장면 묘사 + "No text, no letters" (AI가 넣는 글자는 깨짐) + 덱 팔레트(navy, warm orange).
  표지용은 "empty space on the left"로 글자 자리 확보.
- 결과 화면 상단 다운로드 버튼 → 이미지 1K, 영상 720p(원본). `~/Downloads`에서 `images/ai_*.jpg`, `intro/intro.mp4`로 복사.
- 영상 포스터: PyAV로 마지막 프레임을 `intro/intro.png`로 저장. `credits.json`에 `{"text": "영상: Google Flow(Veo)로 생성"}`처럼 표기 문구 추가.
- 인트로 영상은 `d.movie(s, "intro", 0, 0, 13.333, 7.5, folder=HERE / "intro", autoplay=True)`로 전면·자동 재생.

## 5. PowerPoint 만들기

`<작업폴더>/build_pptx.py`를 작성해 `scripts/pptx_kit.py`의 `Deck`을 사용. 전체 예시는
`references/example_build.py`(1주차 확률변수와 확률분포, 11장). 새 차시는 이 파일을 복사해 내용만 바꾸는 것이 빠름.

```bash
python <작업폴더>/build_pptx.py   # → output/NN_제목.pptx
```

`Deck`이 처리해 주는 것: 16:9, 한글 글꼴(맑은 고딕, 동아시아 글꼴까지 지정), 사진 가운데 자르기,
manim 영상 + 포스터 삽입, 표, 발표자 노트, 출처 문구.

## 6. 미리보기 확인

```bash
python <skill>/scripts/preview.py "<작업폴더>/output/NN_제목.pptx" <scratchpad>/preview
```

PowerPoint로 모든 슬라이드를 PNG로 내보내고 `sheet.png` 한 장으로 합침. Read로 보고 글자 넘침, 겹침,
사진 잘림을 고친 뒤 다시 빌드. (PowerPoint가 없는 컴퓨터면 이 단계를 건너뛰고 사용자에게 확인을 부탁.)

## 7. 보고

- 저장 경로(전체 경로), 슬라이드 구성 표, 애니메이션 목록, 사용한 사진과 라이선스.
- 확인하지 못한 것은 솔직히(예: 영상 재생 자체는 미확인, 교과서 수치 대신 쓴 예시).
- 사용자가 고친 점을 말하면 `CLAUDE.md`의 **피드백 누적**에 한 줄로 추가해서 다음 차시에도 반영.

## 파일 정리 규칙

```
lectures/weekNN_주제/
├── outline.md
├── build_pptx.py
├── animations/  scenes.py, out/*.mp4, out/*.png
├── images/      *.jpg, credits.json
└── output/      NN_제목.pptx
```
임시 파일(교과서 추출본, 후보 사진, 미리보기)은 scratchpad나 `_` 로 시작하는 폴더에.
