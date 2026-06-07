import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction

st.title("삼각함수 그래프 시각화")
st.write("2022개정 교육과정 수학 수업용 삼각함수 그래프 도구")

page = st.sidebar.radio("페이지 선택", ["기본형", "그래프 보기"])

if page == "기본형":
    st.sidebar.header("단위원 기본형")
    func = st.sidebar.selectbox("함수 선택", ["sin", "cos", "tan"])
    angle = st.sidebar.slider("각도 θ (rad)", 0.0, 2 * np.pi, 0.0, 0.01)
    angle_deg = angle * 180 / np.pi

    cos_val = np.cos(angle)
    sin_val = np.sin(angle)
    tan_val = np.tan(angle)

    st.write("### 단위원과 삼각함수")
    st.write("단위원 위의 점은 `(cos θ, sin θ)`이고, `sin θ`는 y좌표, `cos θ`는 x좌표입니다.")
    st.write("`tan θ`는 `sin θ / cos θ`로 정의됩니다. cos θ = 0일 때는 점근선이 나타납니다.")
    st.write(f"- θ = {angle:.2f} rad ({angle_deg:.1f}°)")
    st.write(f"- cos θ = {cos_val:.3f}")
    st.write(f"- sin θ = {sin_val:.3f}")
    if np.isclose(cos_val, 0.0, atol=1e-6):
        st.write("- tan θ = 정의되지 않음 (cos θ = 0)")
    else:
        st.write(f"- tan θ = {tan_val:.3f}")

    fig_circle, ax_circle = plt.subplots(figsize=(5, 5))
    circle = plt.Circle((0, 0), 1, fill=False, color='black')
    ax_circle.add_patch(circle)
    ax_circle.axhline(0, color='gray', linewidth=0.5)
    ax_circle.axvline(0, color='gray', linewidth=0.5)
    ax_circle.plot([0, cos_val], [0, sin_val], color='blue', linewidth=2)
    ax_circle.scatter([cos_val], [sin_val], color='red', s=70, zorder=5)
    ax_circle.plot([0, cos_val], [sin_val, sin_val], color='red', linestyle='--', linewidth=1)
    ax_circle.plot([cos_val, cos_val], [0, sin_val], color='red', linestyle='--', linewidth=1)
    ax_circle.text(0.05, 0.9, r'$	heta$', fontsize=16, color='blue')
    ax_circle.set_xlim(-1.2, 1.2)
    ax_circle.set_ylim(-1.2, 1.2)
    ax_circle.set_aspect('equal', 'box')
    ax_circle.set_xlabel('x')
    ax_circle.set_ylabel('y')
    ax_circle.set_title('단위원과 θ')
    ax_circle.set_xticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax_circle.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    st.pyplot(fig_circle)

    x_plot = np.linspace(0, 2 * np.pi, 400)
    if func == "tan":
        x_plot = np.linspace(-np.pi / 2 + 0.1, np.pi / 2 - 0.1, 400)

    if func == "sin":
        y_plot = np.sin(x_plot)
    elif func == "cos":
        y_plot = np.cos(x_plot)
    else:
        y_plot = np.tan(x_plot)

    fig_func, ax_func = plt.subplots(figsize=(8, 4))
    ax_func.plot(x_plot, y_plot, color='blue', linewidth=2)
    if not (func == "tan" and np.isclose(np.cos(angle), 0.0, atol=1e-6)):
        point_y = np.sin(angle) if func == "sin" else np.cos(angle) if func == "cos" else np.tan(angle)
        ax_func.scatter([angle], [point_y], color='red', s=70, zorder=5)
    ax_func.set_xlabel('x')
    ax_func.set_ylabel(f'y = {func}(x)')
    ax_func.set_title(f'기본형: y = {func}(x)')
    ax_func.grid(True)
    ax_func.axhline(0, color='black', linewidth=0.5)
    ax_func.axvline(0, color='black', linewidth=0.5)
    if func in ["sin", "cos"]:
        ax_func.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
        ax_func.set_xticklabels(["0", "π/2", "π", "3π/2", "2π"])
    else:
        ax_func.set_ylim(-5, 5)
        ax_func.set_xticks([-np.pi / 2, 0, np.pi / 2])
        ax_func.set_xticklabels(["-π/2", "0", "π/2"])
    st.pyplot(fig_func)

elif page == "그래프 보기":
    st.sidebar.header("함수 및 파라미터 설정")
    func = st.sidebar.selectbox("삼각함수 선택", ["sin", "cos", "tan"])
    b = st.sidebar.slider("주기 계수 (b)", 0.1, 5.0, 1.0, 0.1)
    d = st.sidebar.slider("수평 이동 (d)", -5.0, 5.0, 0.0, 0.1)
    c = st.sidebar.slider("수직 이동 (c)", -5.0, 5.0, 0.0, 0.1)

    if func == "tan":
        default_min = -np.pi / 2
        default_max = np.pi / 2
    else:
        default_min = -2 * np.pi
        default_max = 2 * np.pi

    x_min = st.sidebar.slider("x 최소값", -10.0, 0.0, default_min)
    x_max = st.sidebar.slider("x 최대값", 0.0, 10.0, default_max)

    x = np.linspace(x_min, x_max, 1000)
    x_shift = x - d
    if func == "sin":
        y = np.sin(b * x_shift) + c
    elif func == "cos":
        y = np.cos(b * x_shift) + c
    elif func == "tan":
        raw_y = np.tan(b * x_shift) + c
        mask = np.abs(np.cos(b * x_shift)) < 0.02
        y = np.ma.array(raw_y, mask=mask)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel("x")
    shift_inner = f"(x - {d:.2f})" if d >= 0 else f"(x + {abs(d):.2f})"
    ax.set_ylabel(f"y = {func}({b} * {shift_inner}) + {c}")
    ax.grid(True)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)

    def format_pi_tick(value):
        frac = Fraction(value / np.pi).limit_denominator(8)
        if frac.numerator == 0:
            return "0"
        sign = "-" if frac.numerator * frac.denominator < 0 else ""
        num = abs(frac.numerator)
        den = frac.denominator
        if den == 1:
            return f"{sign}{'' if num == 1 else num}π"
        return f"{sign}{num}π/{den}"

    if func in ["sin", "cos"]:
        period = 2 * np.pi / b
    else:
        period = np.pi / b

    tick_spacing = np.pi / 2
    xticks = np.arange(np.ceil(x_min / tick_spacing) * tick_spacing, x_max + tick_spacing / 2, tick_spacing)
    ax.set_xticks(xticks)
    ax.set_xticklabels([format_pi_tick(t) for t in xticks])
    for tick in np.arange(np.ceil(x_min / period) * period, x_max + period / 2, period):
        ax.axvline(tick, color='red', linestyle='--', alpha=0.5, linewidth=1)

    if func == "sin":
        k_values = np.arange(np.ceil(b * x_min / np.pi), np.floor(b * x_max / np.pi) + 1)
        x_zeros = k_values * np.pi / b
    elif func == "cos":
        k_values = np.arange(np.ceil((b * x_min - np.pi / 2) / np.pi), np.floor((b * x_max - np.pi / 2) / np.pi) + 1)
        x_zeros = (np.pi / 2 + k_values * np.pi) / b
    else:
        k_values = np.arange(np.ceil(b * x_min / np.pi), np.floor(b * x_max / np.pi) + 1)
        x_zeros = k_values * np.pi / b

    y_zeros = np.zeros_like(x_zeros)
    ax.scatter(x_zeros, y_zeros, color='blue', s=50, zorder=5, label='교점 (y=0)')

    if func == "tan":
        k_values_asymp = np.arange(np.ceil((b * x_min - np.pi / 2) / np.pi), np.floor((b * x_max - np.pi / 2) / np.pi) + 1)
        x_asymp = (np.pi / 2 + k_values_asymp * np.pi) / b
        first_label = True
        for xa in x_asymp:
            ax.axvline(xa, color='green', linestyle='--', alpha=0.8, linewidth=2,
                       label='점근선' if first_label else None)
            first_label = False
        ax.set_ylim(c - 10, c + 10)
        ax.legend(loc='upper left')

    st.pyplot(fig)

    st.write("### 그래프 설명")
    st.write(f"선택된 함수: y = {func}({b} * {shift_inner}) + {c}")
    if func in ["sin", "cos"]:
        st.write("- **주기 계수 (b)**: 주기를 조절")
        st.latex(r"\text{현재 주기} = \frac{2\pi}{b}")
        st.write(f"(현재 b={b:.1f} 이므로 약 {2*np.pi/b:.2f})")
    else:
        st.write("- **주기 계수 (b)**: 주기를 조절")
        st.latex(r"\text{현재 주기} = \frac{\pi}{b}")
        st.write(f"(현재 b={b:.1f} 이므로 약 {np.pi/b:.2f})")
    st.write("- **수평 이동 (d)**: 그래프를 왼쪽/오른쪽으로 이동")
    st.write("- **수직 이동 (c)**: 그래프를 위아래로 이동")
    st.write("- **주기 표시**: 빨간 점선으로 주기 경계를 표시")
    st.write("- **교점 표시**: 파란 점으로 y=0과의 교점을 표시")
    if func == "tan":
        st.write("- **점근선 표시**: 녹색 선으로 점근선을 표시")
