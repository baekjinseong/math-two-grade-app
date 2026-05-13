# 삼각함수 그래프 시각화 앱

2022개정 교육과정 수학 수업용 삼각함수 그래프 도구입니다. sin, cos, tan 함수의 파라미터(a, b, c)를 조절하여 그래프의 변화를 실시간으로 확인할 수 있습니다.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### 기능
- 삼각함수 선택: sin, cos, tan
- 파라미터 조절:
  - **a**: 진폭 (그래프의 높이)
  - **b**: 주기 계수 (주기 조절)
  - **d**: 수평 이동 (그래프를 왼쪽/오른쪽으로 이동)
  - **c**: 수직 이동 (그래프 위치 조절)
- 실시간 그래프 업데이트
- x 범위 조절 가능

### 실행 방법

1. 요구사항 설치

   ```
   $ pip install -r requirements.txt
   ```

2. 앱 실행

   ```
   $ streamlit run streamlit_app.py
   ```

3. 브라우저에서 http://localhost:8502 접속
