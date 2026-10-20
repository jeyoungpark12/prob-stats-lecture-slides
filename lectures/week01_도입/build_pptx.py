"""예시: 1주차 확률변수와 확률분포 (13장). 새 차시는 이 파일을 lectures/weekNN_주제/build_pptx.py 로 복사해 내용만 교체.
(lectures/week01_도입/build_pptx.py 와 같은 내용)

실행 위치: 차시 폴더 (images/, animations/out/ 이 있는 곳)
    python build_pptx.py [출력경로]
"""
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] if Path(__file__).parent.name == "references" \
    else Path(__file__).resolve().parents[2] / ".claude" / "skills" / "lecture-slides"
sys.path.insert(0, str(SKILL / "scripts"))
from pptx_kit import C, MSO_ANCHOR, PP_ALIGN, Deck  # noqa: E402

HERE = Path.cwd()
OUT = sys.argv[1] if len(sys.argv) > 1 else HERE / "output" / "01_확률변수와_확률분포.pptx"
d = Deck(base=HERE)

# 1. 표지
s = d.slide(C.NAVY, "오늘은 확률분포 단원의 첫 시간으로, 확률변수와 확률분포를 다룹니다. "
                    "동전과 주사위처럼 우연한 결과를 숫자로 바꾸어 다루는 것이 오늘의 주제입니다.")
d.photo(s, "ai_cover", 0, 0, 13.333, 7.5)  # 왼쪽이 비어 있는 AI 생성 배경 → 글자는 왼쪽에
d.text(s, 0.8, 1.9, 6.5, 0.5, "Ⅲ. 통계 · 1. 확률분포", 20, C.ORANGE, True)
d.text(s, 0.8, 2.5, 6.5, 2.2, ["확률변수와", "확률분포"], 60, C.BG, True, spacing=1.05)
d.text(s, 0.8, 4.75, 6.5, 0.6, "우연한 결과를 숫자로 바꾸는 방법", 26, C.LINE)
d.footer(s, "확률과 통계 · 공학계열 1학년 · " + d.credit("ai_cover"), C.ON_DARK2)

# 1-1. 인트로 영상 (전면, 슬라이드가 열리면 자동 재생)
s = d.slide(C.NAVY, "8초 인트로 영상. 동전 → 주사위 → 막대그래프 → 종 모양 곡선. "
                    "'던질 때마다 결과는 달라도, 많이 모으면 모양이 생긴다'는 질문으로 시작해 주세요. "
                    "[영상: 슬라이드가 열리면 자동 재생, 소리 있음]")
d.movie(s, "intro", 0, 0, 13.333, 7.5, folder=HERE / "intro", autoplay=True)
d.text(s, 0.6, 6.95, 12.1, 0.35, d.credit("intro"), 12, C.ON_DARK2)

# 2. 학습 목표
s = d.slide(C.BG, "오늘의 목표는 세 가지입니다. 확률변수가 무엇인지, 이산확률변수의 분포를 표와 그래프로 "
                  "나타내는 법, 그리고 연속확률변수에서는 확률을 왜 넓이로 구하는지입니다.")
d.title(s, "학습 목표")
for i, (n, h, desc, col) in enumerate([
        ("01", "확률변수의 뜻", "시행 결과에 실수를 대응시키는 규칙의 이해", C.BLUE),
        ("02", "이산확률변수", "확률분포를 표와 그래프, 확률질량함수로 표현", C.BLUE),
        ("03", "연속확률변수", "확률밀도함수와 넓이로 구하는 확률의 의미 파악", C.ORANGE_D)]):
    x = 0.6 + i * 4.1
    d.box(s, x, 1.7, 3.85, 4.6, C.WHITE)
    d.box(s, x, 1.7, 3.85, 0.12, col, rounded=False)
    d.text(s, x + 0.4, 2.1, 3.1, 0.8, n, 40, col, True)
    d.text(s, x + 0.4, 3.0, 3.1, 0.7, h, 26, C.NAVY, True)
    d.text(s, x + 0.4, 3.8, 3.1, 2.0, desc, 18, C.TEXT2, spacing=1.4)
d.footer(s, "교과서 Ⅲ-1 확률분포 · 확률변수와 확률분포")

# 3. 비유 사진 슬라이드 (사진 왼쪽 + 대응 카드 + 핵심 문장)
s = d.slide(C.BG, "은행 번호표를 떠올려 보세요. 손님이 누구든 번호 하나를 받습니다. "
                  "확률변수도 시행 결과가 무엇이든 숫자 하나를 붙여 주는 규칙입니다.")
d.title(s, "비유로 시작: 은행 번호표")
d.photo(s, "ticket", 0.6, 1.5, 4.6, 5.2)
d.card(s, 5.7, 1.6, 7.0, 1.4, C.GRAY, "은행 번호표", "손님마다 번호 하나 발행")
d.card(s, 5.7, 3.25, 7.0, 1.4, C.BLUE, "확률변수", "시행 결과마다 실수 하나 대응")
d.box(s, 5.7, 5.05, 7.0, 1.4, C.NAVY)
d.text(s, 6.1, 5.05, 6.4, 1.4, [[("결과에 숫자를 붙이는 규칙", 24, C.BG, True)],
                                [("= 확률변수", 24, C.ORANGE, True)]], anchor=MSO_ANCHOR.MIDDLE)
d.footer(s, d.credit("ticket"))

# 4. 애니메이션 전면 슬라이드
s = d.slide(C.BG, "(앞, 뒤)와 (뒤, 앞)이 모두 1로 모이는 점을 강조. 그래서 X=1의 확률이 가장 큼. [영상: 클릭하면 재생]")
d.title(s, "확률변수: 결과에 숫자를 붙이는 규칙")
d.movie(s, "RandomVariable", 1.67, 1.35, 10.0, 5.625)
d.footer(s, "예: 동전 한 개를 두 번 던지는 시행 · 영상 클릭 시 재생")

# 5. 표 + 영상 나란히
s = d.slide(C.BG, "네 결과가 모두 1/4씩이므로 X=1은 1/2. 막대를 이어 붙이면 길이가 정확히 1.")
d.title(s, "이산확률변수의 확률분포")
d.text(s, 0.6, 1.6, 5.4, 0.9, [[("값을 ", 22), ("셀 수 있는", 22, C.BLUE, True), (" 확률변수", 22)],
                               [("→ 이산확률변수", 22, C.NAVY, True)]])
d.table(s, 0.6, 2.9, 5.4, 1.3, [["X", "0", "1", "2", "합계"], ["P(X=x)", "1/4", "1/2", "1/4", "1"]],
        [1.4, 1.0, 1.0, 1.0, 1.0], center=True)
d.text(s, 0.6, 4.6, 5.4, 1.2, [[("P(X = xᵢ) = pᵢ", 24, C.BLUE, True)], [("확률질량함수", 22)]])
d.movie(s, "PMFBars", 6.4, 1.6, 6.33, 3.56)
d.text(s, 6.4, 5.35, 6.33, 0.5, "막대를 이어 붙이면 합계 1", 18, C.GRAY, align=PP_ALIGN.CENTER)
d.footer(s, "동전 두 번 던지기: 앞면이 나온 횟수 X의 확률분포 · 영상 클릭 시 재생")

# 6. 성질 카드 + 비유 사진
s = d.slide(C.BG, "피자 조각 크기는 제각각이어도 모두 모으면 정확히 한 판. 확률도 모두 더하면 1.")
d.title(s, "확률질량함수의 두 가지 성질")
d.photo(s, "pizza", 0.6, 1.5, 4.6, 5.2)
d.card(s, 5.7, 1.5, 7.0, 1.75, C.BLUE, "성질 1 · 각 확률은 0 이상 1 이하", "0 ≤ pᵢ ≤ 1", 18, 30)
d.card(s, 5.7, 3.45, 7.0, 1.75, C.ORANGE_D, "성질 2 · 모든 확률의 합은 1", "p₁ + p₂ + ⋯ + pₙ = 1", 18, 30)
d.box(s, 5.7, 5.5, 7.0, 1.2, C.NAVY)
d.text(s, 6.1, 5.5, 6.4, 1.2, [[("비유: ", 22, C.ORANGE, True), ("조각을 모두 모으면 피자 한 판", 22, C.BG, True)]],
       anchor=MSO_ANCHOR.MIDDLE)
d.footer(s, d.credit("pizza"))

# 7. 사진 두 장 비교 비유
s = d.slide(C.BG2, "계단은 정해진 높이에만, 경사로는 어느 높이에서든 멈출 수 있음. 앞이 이산, 뒤가 연속.")
d.title(s, "비유: 계단과 경사로")
for i, (name, h, desc, col) in enumerate([("stairs", "이산 = 계단", "정해진 높이에만 멈춤, 중간 값 없음", C.BLUE),
                                          ("ramp", "연속 = 경사로", "어느 높이에서든 멈춤 가능", C.ORANGE_D)]):
    x = 0.6 + i * 6.2
    d.photo(s, name, x, 1.4, 5.9, 3.9)
    d.text(s, x, 5.45, 5.9, 0.55, h, 28, col, True)
    d.text(s, x, 6.05, 5.9, 0.5, desc, 20, C.TEXT2)
d.footer(s, f"{d.credit('stairs')} / {d.credit('ramp')}")

# 8. 애니메이션
s = d.slide(C.BG, "공이 계단은 한 칸씩, 경사로는 미끄러지듯 올라감. [영상: 클릭하면 재생]")
d.title(s, "이산 vs 연속: 끊긴 값과 이어진 값")
d.movie(s, "StairsVsRamp", 1.67, 1.35, 10.0, 5.625)
d.footer(s, "영상 클릭 시 재생")

# 9. 좁은 사진 + 큰 영상 + 핵심 알약
s = d.slide(C.BG2, "확률은 넓이. 3분~7분은 4 × 1/10 = 0.4. 한 점은 넓이 0. (대기 시간 수치는 예시)")
d.title(s, "연속확률변수: 확률 = 그래프 아래 넓이")
d.photo(s, "subway", 0.6, 1.4, 3.5, 4.4)
d.text(s, 0.6, 5.95, 3.5, 0.8, [[("예: 10분 간격 지하철", 18, C.ORANGE_D, True)], [("기다리는 시간 X", 18, C.NAVY, True)]])
d.movie(s, "DensityArea", 4.5, 1.4, 8.23, 4.63)
for i, t in enumerate(["f(x) ≥ 0", "전체 넓이 = 1", "P(X = a) = 0"]):
    d.box(s, 4.5 + i * 2.8, 6.2, 2.6, 0.6, C.WHITE, line=C.LINE)
    d.text(s, 4.5 + i * 2.8, 6.2, 2.6, 0.6, t, 18, C.NAVY, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
d.footer(s, d.credit("subway") + " · 영상 클릭 시 재생")

# 10-1. 공학 현장 그림 두 장 (AI 생성)
s = d.slide(C.BG, "공장에서 불량품이 몇 개 나오는지는 셀 수 있으니 이산, 센서가 재는 신호는 끊김 없이 변하니 연속. "
                  "다음 장의 표로 정리합니다.")
d.title(s, "공학 현장의 이산과 연속")
for i, (name, h, desc, col) in enumerate([
        ("ai_factory", "이산: 불량품 개수", "0개, 1개, 2개… 셀 수 있는 값", C.BLUE),
        ("ai_sensor", "연속: 센서 신호", "온도·전압처럼 끊김 없이 변하는 값", C.ORANGE_D)]):
    x = 0.6 + i * 6.2
    d.photo(s, name, x, 1.4, 5.9, 3.9)
    d.text(s, x, 5.45, 5.9, 0.55, h, 28, col, True)
    d.text(s, x, 6.05, 5.9, 0.5, desc, 20, C.TEXT2)
d.footer(s, d.credit("ai_factory"))

# 10. 비교표
s = d.slide(C.BG, "불량품 개수는 이산, 센서 오차·부품 수명은 연속. '몇 개냐, 얼마나냐'로 구분.")
d.title(s, "이산 vs 연속: 공학 현장의 예")
d.table(s, 0.6, 1.6, 12.1, 4.6, [
    ["구분", "이산확률변수 (계단)", "연속확률변수 (경사로)"],
    ["취하는 값", "셀 수 있는 값", "구간 안의 모든 실수"],
    ["분포 표현", "확률질량함수 P(X = x)", "확률밀도함수 f(x)"],
    ["확률 계산", "확률의 합", "그래프 아래 넓이"],
    ["공학 예시", "불량품 개수, 패킷 손실 수", "센서 측정 오차, 부품 수명"]],
    [2.5, 4.8, 4.8], head_fills=[C.NAVY, C.BLUE, C.ORANGE])
d.footer(s, '판단 기준: "몇 개?"면 이산, "얼마나?"면 연속')

# 11. 요약 + 퀴즈 (정답은 노트)
s = d.slide(C.NAVY, "정답. Q1: 이산. Q2: 1/8, 3/8, 3/8, 1/8. Q3: 폭 4 × 높이 k = 1 이므로 k = 1/4.")
d.title(s, "요약과 확인 퀴즈", C.BG)
d.text(s, 0.6, 1.5, 5.0, 0.5, "오늘의 핵심", 20, C.ORANGE, True)
d.text(s, 0.6, 2.1, 5.0, 2.6, ["확률변수: 결과 → 실수의 대응", "이산: 확률질량함수, 합 = 1", "연속: 확률밀도함수, 넓이 = 확률"],
       22, C.BG, spacing=1.9)
d.photo(s, "ai_student", 0.6, 4.6, 4.6, 2.1)
d.text(s, 6.2, 1.5, 6.5, 0.5, "퀴즈", 20, C.ORANGE, True)
for i, q in enumerate(["Q1. 주사위 한 개의 눈 X: 이산 또는 연속 판단",
                       "Q2. 동전 세 개를 던질 때 앞면의 개수 X의 확률분포표 작성",
                       "Q3. 0 ≤ X ≤ 4, f(x) = k (상수)일 때 k의 값"]):
    y = 2.1 + i * 1.55
    d.box(s, 6.2, y, 6.5, 1.35, C.CARD_DARK)
    d.text(s, 6.5, y, 5.9, 1.35, q, 20, C.BG, anchor=MSO_ANCHOR.MIDDLE, spacing=1.3)
d.footer(s, d.credit("ai_student"), C.ON_DARK2)

d.save(OUT)
