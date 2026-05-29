import streamlit as st
import random
import time

st.set_page_config(page_title="피하기 게임", layout="centered")

st.title("🎮 피하기 게임")

# 게임 상태 저장
if "player" not in st.session_state:
    st.session_state.player = 2

if "enemy_x" not in st.session_state:
    st.session_state.enemy_x = random.randint(0, 4)

if "enemy_y" not in st.session_state:
    st.session_state.enemy_y = 0

if "score" not in st.session_state:
    st.session_state.score = 0

# 버튼으로 이동
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬅️ 왼쪽"):
        if st.session_state.player > 0:
            st.session_state.player -= 1

with col3:
    if st.button("오른쪽 ➡️"):
        if st.session_state.player < 4:
            st.session_state.player += 1

# 적 이동
st.session_state.enemy_y += 1

# 충돌 체크
game_over = False

if (
    st.session_state.enemy_y == 4
    and st.session_state.enemy_x == st.session_state.player
):
    game_over = True

# 적이 바닥 도착하면 새로 생성
if st.session_state.enemy_y > 4:
    st.session_state.enemy_y = 0
    st.session_state.enemy_x = random.randint(0, 4)
    st.session_state.score += 1

# 게임판 그리기
board = []

for y in range(5):
    row = ""
    for x in range(5):

        if (
            x == st.session_state.enemy_x
            and y == st.session_state.enemy_y
        ):
            row += "🟥"

        elif (
            x == st.session_state.player
            and y == 4
        ):
            row += "🟦"

        else:
            row += "⬜"

    board.append(row)

for row in board:
    st.text(row)

# 점수 출력
st.write(f"점수: {st.session_state.score}")

# 게임 오버
if game_over:
    st.error("💥 게임 오버!")
    
    if st.button("다시 시작"):
        st.session_state.player = 2
        st.session_state.enemy_x = random.randint(0, 4)
        st.session_state.enemy_y = 0
        st.session_state.score = 0

# 자동 새로고침
time.sleep(0.5)
st.rerun()
