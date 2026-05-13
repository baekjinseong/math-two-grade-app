import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("삼각함수 그래프 시각화")
st.write("2022개정 교육과정 수학 수업용 삼각함수 그래프 도구")

# 사이드바에 옵션들
st.sidebar.header("함수 및 파라미터 설정")

func = st.sidebar.selectbox("삼각함수 선택", ["sin", "cos", "tan"])

a = st.sidebar.slider("진폭 (a)", -5.0, 5.0, 1.0, 0.1)
b = st.sidebar.slider("주기 계수 (b)", 0.1, 5.0, 1.0, 0.1)
d = st.sidebar.slider("수평 이동 (d)", -5.0, 5.0, 0.0, 0.1)
c = st.sidebar.slider("수직 이동 (c)", -5.0, 5.0, 0.0, 0.1)

# x 범위 (tan의 경우 기본 범위를 조절)
if func == "tan":
    default_min = -np.pi / 2
    default_max = np.pi / 2
else:
    default_min = -2 * np.pi
    default_max = 2 * np.pi

x_min = st.sidebar.slider("x 최소값", -10.0, 0.0, default_min)
x_max = st.sidebar.slider("x 최대값", 0.0, 10.0, default_max)

# x 값 생성
x = np.linspace(x_min, x_max, 1000)

# 함수 계산
x_shift = x - d
if func == "sin":
    y = a * np.sin(b * x_shift) + c
elif func == "cos":
    y = a * np.cos(b * x_shift) + c
elif func == "tan":
    raw_y = a * np.tan(b * x_shift) + c
    mask = np.abs(np.cos(b * x_shift)) < 0.02
    y = np.ma.array(raw_y, mask=mask)

# 그래프 그리기
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel("x")
shift_inner = f"(x - {d:.2f})" if d >= 0 else f"(x + {abs(d):.2f})"
ax.set_ylabel(f"y = {a} * {func}({b} * {shift_inner}) + {c}")
ax.grid(True)
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)

# 주기 표시 (수직선과 눈금)
if func in ["sin", "cos"]:
    period = 2 * np.pi / b
else:  # tan
    period = np.pi / b

xticks = np.arange(np.ceil(x_min / period) * period, x_max + period, period)
ax.set_xticks(xticks)
ax.set_xticklabels([f"{tick/period:.1f}T" for tick in xticks])  # T는 주기 단위
for tick in xticks:
    ax.axvline(tick, color='red', linestyle='--', alpha=0.5, linewidth=1)

# y=0과의 교점 표시
if func == "sin":
    # sin(bx) = 0 => bx = kπ, x = kπ / b
    k_values = np.arange(np.ceil(b * x_min / np.pi), np.floor(b * x_max / np.pi) + 1)
    x_zeros = k_values * np.pi / b
elif func == "cos":
    # cos(bx) = 0 => bx = π/2 + kπ, x = (π/2 + kπ)/b
    k_values = np.arange(np.ceil((b * x_min - np.pi/2) / np.pi), np.floor((b * x_max - np.pi/2) / np.pi) + 1)
    x_zeros = (np.pi / 2 + k_values * np.pi) / b
elif func == "tan":
    # tan(bx) = 0 => bx = kπ, x = kπ / b
    k_values = np.arange(np.ceil(b * x_min / np.pi), np.floor(b * x_max / np.pi) + 1)
    x_zeros = k_values * np.pi / b

y_zeros = np.zeros_like(x_zeros)
ax.scatter(x_zeros, y_zeros, color='blue', s=50, zorder=5, label='교점 (y=0)')

# tan의 점근선 표시
if func == "tan":
    # tan(bx) = ∞ => bx = π/2 + kπ, x = (π/2 + kπ)/b
    k_values_asymp = np.arange(np.ceil((b * x_min - np.pi/2) / np.pi), np.floor((b * x_max - np.pi/2) / np.pi) + 1)
    x_asymp = (np.pi / 2 + k_values_asymp * np.pi) / b
    first_label = True
    for xa in x_asymp:
        ax.axvline(xa, color='green', linestyle='-', alpha=0.7, linewidth=2,
                   label='점근선' if first_label else None)
        first_label = False
    ax.set_ylim(c - 10, c + 10)
    ax.legend(loc='upper left')

st.pyplot(fig)

# 설명
st.write("### 그래프 설명")
st.write(f"선택된 함수: y = {a} * {func}({b} * {shift_inner}) + {c}")
st.write("- **진폭 (a)**: 그래프의 높이 (최댓값 - 최솟값)/2")
if func in ["sin", "cos"]:
    st.write(f"- **주기 계수 (b)**: 주기를 조절 (현재 주기: {2*np.pi/b:.2f})")
else:
    st.write(f"- **주기 계수 (b)**: 주기를 조절 (현재 주기: {np.pi/b:.2f})")
st.write("- **수평 이동 (d)**: 그래프를 왼쪽/오른쪽으로 이동")
st.write("- **수직 이동 (c)**: 그래프를 위아래로 이동")
st.write("- **주기 표시**: 빨간 점선으로 주기 경계를 표시")
st.write("- **교점 표시**: 파란 점으로 y=0과의 교점을 표시")
if func == "tan":
    st.write("- **점근선 표시**: 녹색 선으로 점근선을 표시")
