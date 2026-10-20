"""1주차 확률변수와 확률분포 애니메이션 (manim CE, LaTeX 없이 Text만 사용)

렌더링: manim -r 1920,1080 --fps 30 scenes.py <장면이름>
"""
from manim import *

FONT = "Malgun Gothic"
BG = "#F7F6F2"
NAVY = "#1F2A44"
BLUE = "#2F6FDB"
ORANGE = "#F2A65A"
GRAY = "#6A7489"
LIGHT = "#DCE6F8"

config.background_color = BG


def T(s, size=36, color=NAVY, weight=NORMAL):
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


class RandomVariable(Scene):
    """동전 두 번 던지기: 근원사건 → X의 값 대응"""

    def construct(self):
        outcomes = ["(앞, 앞)", "(앞, 뒤)", "(뒤, 앞)", "(뒤, 뒤)"]
        targets = [2, 1, 1, 0]

        pills = VGroup()
        for s in outcomes:
            box = RoundedRectangle(width=3.2, height=0.9, corner_radius=0.45,
                                   fill_color=WHITE, fill_opacity=1, stroke_color="#C9D3E6")
            pills.add(VGroup(box, T(s, 34)))
        pills.arrange(DOWN, buff=0.35).shift(LEFT * 4.5 + DOWN * 0.3)

        circles = {}
        for v, y in [(2, pills[0].get_y()), (1, (pills[1].get_y() + pills[2].get_y()) / 2), (0, pills[3].get_y())]:
            c = Circle(radius=0.55, fill_color=NAVY, fill_opacity=1, stroke_width=0)
            circles[v] = VGroup(c, T(str(v), 44, BG, BOLD)).move_to([3.4, y, 0])

        s_label = T("표본공간 S", 30, GRAY, BOLD).next_to(pills, UP, buff=0.4)
        x_label = T("X의 값", 30, GRAY, BOLD).next_to(circles[2], UP, buff=0.4)
        rule = T("X = 앞면이 나온 횟수", 34, BLUE, BOLD).to_edge(UP, buff=0.5)

        self.play(FadeIn(s_label), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.3) for p in pills], lag_ratio=0.2))
        self.play(Write(rule))
        self.play(FadeIn(x_label), *[GrowFromCenter(c) for c in circles.values()])

        arrows = VGroup()
        for p, v in zip(pills, targets):
            a = Arrow(p.get_right(), circles[v].get_left(), buff=0.15, color=BLUE, stroke_width=5)
            arrows.add(a)
            self.play(GrowArrow(a), Indicate(p, color=BLUE, scale_factor=1.05), run_time=0.8)
        self.wait(0.4)

        self.play(arrows[1].animate.set_color(ORANGE), arrows[2].animate.set_color(ORANGE),
                  circles[1][0].animate.set_fill(ORANGE))
        note = VGroup(T("두 결과가", 30, "#C8691E", BOLD), T("X = 1로 모임", 30, "#C8691E", BOLD)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(circles[1], RIGHT, buff=0.35)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(2)


class PMFBars(Scene):
    """확률분포 막대그래프 → 이어 붙이면 합 1"""

    def construct(self):
        base_y = -2.0
        unit = 7.0  # 확률 1 = 7 단위 높이
        axis = Line([-4.5, base_y, 0], [4.5, base_y, 0], color=NAVY, stroke_width=4)
        title = T("X의 확률분포", 40, NAVY, BOLD).to_edge(UP, buff=0.5)
        self.play(Write(title), Create(axis))

        probs = [(0, 0.25, "1/4", BLUE), (1, 0.5, "1/2", ORANGE), (2, 0.25, "1/4", BLUE)]
        bars, vals, xs = VGroup(), VGroup(), VGroup()
        for i, (x, p, lab, col) in enumerate(probs):
            cx = (i - 1) * 2.6
            bar = Rectangle(width=1.6, height=p * unit, fill_color=col, fill_opacity=1, stroke_width=0)
            bar.move_to([cx, base_y + p * unit / 2, 0])
            bars.add(bar)
            vals.add(T(lab, 40, NAVY, BOLD).next_to(bar, UP, buff=0.2))
            xs.add(T(str(x), 36).next_to([cx, base_y, 0], DOWN, buff=0.3))
        self.play(FadeIn(xs))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.35), run_time=2)
        self.play(LaggedStart(*[FadeIn(v, shift=DOWN * 0.2) for v in vals], lag_ratio=0.2))
        self.wait(1)

        # 막대를 눕혀 한 줄로 이어 붙이기
        total_w = 10.0
        y = -0.3
        targets, left = VGroup(), -total_w / 2
        for (x, p, lab, col) in probs:
            r = Rectangle(width=p * total_w, height=1.2, fill_color=col, fill_opacity=1, stroke_color=BG, stroke_width=4)
            r.move_to([left + p * total_w / 2, y, 0])
            targets.add(r)
            left += p * total_w
        self.play(FadeOut(vals), FadeOut(xs), FadeOut(axis),
                  *[ReplacementTransform(b, t) for b, t in zip(bars, targets)], run_time=1.6)
        labels = VGroup(*[T(lab, 40, NAVY if col == ORANGE else BG, BOLD).move_to(t)
                          for (x, p, lab, col), t in zip(probs, targets)])
        heads = VGroup(*[T(f"P(X={x})", 30, GRAY, BOLD).next_to(t, UP, buff=0.25)
                         for (x, p, lab, col), t in zip(probs, targets)])
        self.play(FadeIn(labels), FadeIn(heads))
        brace = Brace(targets, DOWN, color=NAVY)
        total = T("합계 = 1", 48, NAVY, BOLD).next_to(brace, DOWN, buff=0.3)
        self.play(GrowFromCenter(brace), Write(total))
        self.wait(2)


class DensityArea(Scene):
    """확률밀도함수: 확률 = 그래프 아래 넓이, 한 점의 확률 = 0"""

    def construct(self):
        ox, oy, sx, h = -5.0, -2.2, 1.0, 2.2  # 원점, x 1분 = 1단위, f(x)=1/10 높이
        x_axis = Arrow([ox - 0.3, oy, 0], [ox + 11, oy, 0], buff=0, color=NAVY, stroke_width=4, tip_length=0.25)
        y_axis = Arrow([ox, oy - 0.3, 0], [ox, oy + 4.2, 0], buff=0, color=NAVY, stroke_width=4, tip_length=0.25)
        title = T("10분 간격 지하철 대기 시간 X", 38, NAVY, BOLD).to_edge(UP, buff=0.4)
        xl = T("X (분)", 26, GRAY).next_to(x_axis.get_end(), DOWN, buff=0.2)
        self.play(Write(title), GrowArrow(x_axis), GrowArrow(y_axis), FadeIn(xl))

        full = Rectangle(width=10 * sx, height=h, fill_color=LIGHT, fill_opacity=1, stroke_width=0)
        full.move_to([ox + 5 * sx, oy + h / 2, 0])
        top = Line([ox, oy + h, 0], [ox + 10 * sx, oy + h, 0], color=NAVY, stroke_width=5)
        fx = T("y = f(x)", 30, NAVY, BOLD).next_to(top.get_end(), UP, buff=0.2)
        ylab = T("1/10", 28).next_to([ox, oy + h, 0], LEFT, buff=0.2)
        ticks = VGroup(*[T(str(v), 26).next_to([ox + v * sx, oy, 0], DOWN, buff=0.2) for v in (0, 10)])
        self.play(FadeIn(full), Create(top), FadeIn(fx), FadeIn(ylab), FadeIn(ticks))
        whole = T("전체 넓이 = 10 × 1/10 = 1", 32, BLUE, BOLD).move_to([ox + 5 * sx, oy + h / 2, 0])
        self.play(Write(whole))
        self.wait(1)
        self.play(FadeOut(whole))

        a = 3.0
        b = ValueTracker(3.0)
        shade = always_redraw(lambda: Rectangle(
            width=max((b.get_value() - a) * sx, 0.001), height=h, fill_color=BLUE, fill_opacity=0.9, stroke_width=0
        ).move_to([ox + (a + b.get_value()) / 2 * sx, oy + h / 2, 0]))
        area = always_redraw(lambda: T(
            f"P(3 ≤ X ≤ {b.get_value():.1f}) = {(b.get_value() - a) / 10:.2f}", 34, NAVY, BOLD
        ).move_to([ox + 5 * sx, oy + h + 1.3, 0]))
        a_tick = T("3", 26).next_to([ox + a * sx, oy, 0], DOWN, buff=0.2)
        b_tick = always_redraw(lambda: T(f"{b.get_value():.1f}", 26, BLUE, BOLD)
                               .next_to([ox + b.get_value() * sx, oy, 0], DOWN, buff=0.7))
        self.play(FadeIn(shade), FadeIn(area), FadeIn(a_tick), FadeIn(b_tick))
        self.play(b.animate.set_value(7.0), run_time=3, rate_func=smooth)
        self.wait(1)

        # 구간을 한 점으로 줄이기
        self.play(b.animate.set_value(3.0), run_time=2.5, rate_func=smooth)
        self.play(FadeOut(area), FadeOut(b_tick))
        point =T("한 점의 넓이 = 0  →  P(X = 3) = 0", 34, "#C8691E", BOLD).move_to([ox + 5 * sx, oy + h / 2, 0])
        self.play(FadeIn(point, shift=UP * 0.2))
        self.wait(2)


class StairsVsRamp(Scene):
    """이산 = 계단(뚝뚝 끊긴 값), 연속 = 경사로(모든 값)"""

    def construct(self):
        def panel(cx, name, sub, col):
            head = T(name, 40, col, BOLD).move_to([cx, 3.0, 0])
            s = T(sub, 28, GRAY).next_to(head, DOWN, buff=0.15)
            return VGroup(head, s)

        left = panel(-3.6, "이산: 계단", "셀 수 있는 값만", BLUE)
        right = panel(3.6, "연속: 경사로", "구간 안의 모든 실수", "#C8691E")
        div = DashedLine([0, 3.3, 0], [0, -3.3, 0], color="#C9D3E6")
        self.play(FadeIn(left), FadeIn(right), Create(div))

        # 계단
        x0, y0, w, hh = -6.4, -2.6, 1.1, 0.9
        pts = [[x0, y0, 0]]
        for i in range(5):
            pts += [[x0 + i * w, y0 + (i + 1) * hh, 0], [x0 + (i + 1) * w, y0 + (i + 1) * hh, 0]]
        stairs = VMobject(color=BLUE, stroke_width=6).set_points_as_corners(pts)
        # 경사로
        ramp = Line([0.8, y0, 0], [6.4, y0 + 5 * hh, 0], color=ORANGE, stroke_width=6)
        self.play(Create(stairs), Create(ramp), run_time=1.5)

        ball_l = Dot(radius=0.18, color=NAVY).move_to([x0 + w / 2, y0 + hh + 0.2, 0])
        ball_r = Dot(radius=0.18, color=NAVY).move_to(ramp.get_start() + UP * 0.2)
        self.play(FadeIn(ball_l), FadeIn(ball_r))

        vals = VGroup(T("0", 26, BLUE, BOLD).next_to(ball_l, UP, buff=0.25))
        self.add(vals[0])
        for i in range(1, 5):
            target = [x0 + (i + 0.5) * w, y0 + (i + 1) * hh + 0.2, 0]
            self.play(ball_l.animate.move_to(target), path_arc=-1.2, run_time=0.5)
            vals.add(T(str(i), 26, BLUE, BOLD).next_to(target, UP, buff=0.25))
            self.add(vals[-1])
        self.play(MoveAlongPath(ball_r, ramp.copy().shift(UP * 0.2)), run_time=2.5, rate_func=linear)

        caption = T("값이 뚝뚝 끊김 vs 값이 끊김 없이 이어짐", 32, NAVY, BOLD).to_edge(DOWN, buff=0.35)
        self.play(Write(caption))
        self.wait(2)
