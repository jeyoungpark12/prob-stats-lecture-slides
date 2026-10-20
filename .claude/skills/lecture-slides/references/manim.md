# manim 애니메이션 작성 요령

## 환경 제약 (Windows, LaTeX 없음)

- `pip install manim` 으로 충분 (영상 인코딩은 PyAV가 처리, ffmpeg 별도 설치 불필요).
- LaTeX가 없으므로 `MathTex`, `Tex`, `DecimalNumber`, `Axes(...).add_coordinates()`, `NumberLine(include_numbers=True)`는 실패함.
  모든 글자는 `Text(..., font="Malgun Gothic")`. 분수는 "1/4", 첨자는 유니코드(pᵢ, p₁)나 "p_i" 대신 문장으로.
- 실시간으로 바뀌는 숫자는 `ValueTracker` + `always_redraw(lambda: Text(f"{v.get_value():.2f}"))`.
- 한글 출력이 깨지면 `PYTHONIOENCODING=utf-8`을 붙여 실행.

## 스타일 (슬라이드와 맞추기)

```python
FONT = "Malgun Gothic"
BG, NAVY, BLUE, ORANGE = "#F7F6F2", "#1F2A44", "#2F6FDB", "#F2A65A"
config.background_color = BG
```
배경을 슬라이드 배경색과 같게 하면 영상이 슬라이드에 자연스럽게 녹아듦. 강조는 주황 하나만.

## 장면 설계

- 한 장면 = 한 아이디어, 10~20초. 마지막 2초는 `self.wait(2)`로 완성된 화면 유지(이 화면이 포스터가 됨).
- 좌표축은 `Line`/`Arrow`로 직접 그리고 눈금 숫자는 `Text`로 배치. 화면 범위는 가로 ±7.1, 세로 ±4.
- 글자 크기 26 이상(1080p 기준), 제목 38~40.
- 움직임이 개념을 보여줘야 함: 대응은 화살표가 하나씩, 분포는 막대가 자라남, 넓이는 구간이 넓어짐,
  극한은 구간이 한 점으로 줄어듦. 장식용 움직임은 넣지 않기.

## 렌더링과 확인

```bash
cd animations
manim -ql -s --disable_caching scenes.py SceneName            # 빠른 확인용 마지막 화면
manim -r 1920,1080 --fps 30 --disable_caching scenes.py SceneName
manim -r 1920,1080 -s --disable_caching scenes.py SceneName   # 포스터용 고화질 PNG
mkdir -p out && cp media/videos/scenes/1080p30/SceneName.mp4 out/ \
  && cp media/images/scenes/SceneName_ManimCE_*.png out/SceneName.png
```
마지막 화면 PNG를 Read로 보고 확인할 것: 글자 겹침, 화면 밖 잘림, 앞 단계에서 남은 글자(FadeOut 누락),
같은 자리에 두 숫자가 겹치는 눈금(움직이는 눈금은 `buff`를 다르게).

## 예시 장면 (1주차)

`lectures/week01_도입/animations/scenes.py`:
- `RandomVariable`: 근원사건 4개 → 화살표 → X의 값 0, 1, 2 (두 결과가 1로 모이는 것 강조)
- `PMFBars`: 막대가 자라난 뒤 눕혀 이어 붙이면 합계 1
- `DensityArea`: 균등분포, 구간 [3, b]가 넓어지며 확률 실시간 표시 → 한 점으로 줄면 0
- `StairsVsRamp`: 계단(이산) vs 경사로(연속), 공이 뛰어오름 vs 미끄러짐
