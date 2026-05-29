import streamlit as st
import random
import time

st.set_page_config(page_title="Snake Game")

st.title("🐍 뱀 게임")

SIZE = 10

# 초기 설정
if "snake" not in st.session_state:
    st.session_state.snake = [(5, 5)]

if "food" not in st.session_state:
    st.session_state.food = (
        random.randint(0, SIZE-1),
        random.randint(0, SIZE-1)
    )

if "direction" not in st.session_state:
    st.session_state.direction = "RIGHT"

if "game_over" not in st.session_state:
    st.session_state.game_over = False

# 방향 버튼
col1, col2, col3 = st.columns(3)

with col2:
    if st.button("⬆️"):
        st.session_state.direction = "UP"

with col1:
    if st.button("⬅️"):
        st.session_state.direction = "LEFT"

with col3:
    if st.button("➡️"):
        st.session_state.direction = "RIGHT"

if st.button("⬇️"):
    st.session_state.direction = "DOWN"

# 게임 실행
if not st.session_state.game_over:

    head_x, head_y = st.session_state.snake[0]

    if st.session_state.direction == "UP":
        head_y -= 1

    elif st.session_state.direction == "DOWN":
        head_y += 1

    elif st.session_state.direction == "LEFT":
        head_x -= 1

    elif st.session_state.direction == "RIGHT":
        head_x += 1

    new_head = (head_x, head_y)

    # 벽 충돌
    if (
        head_x < 0 or head_x >= SIZE or
        head_y < 0 or head_y >= SIZE
    ):
        st.session_state.game_over = True

    # 자기 몸 충돌
    elif new_head in st.session_state.snake:
        st.session_state.game_over = True

    else:
        st.session_state.snake.insert(0, new_head)

        # 음식 먹기
        if new_head == st.session_state.food:
            st.session_state.food = (
                random.randint(0, SIZE-1),
                random.randint(0, SIZE-1)
            )
        else:
            st.session_state.snake.pop()

# 보드 그리기
board = []

for y in range(SIZE):

    row = ""

    for x in range(SIZE):

        if (x, y) == st.session_state.food:
            row += "🍎"

        elif (x, y) in st.session_state.snake:
            row += "🟩"

        else:
            row += "⬛"

    board.append(row)

for row in board:
    st.text(row)

# 점수
score = len(st.session_state.snake) - 1
st.write(f"점수: {score}")

# 게임 오버
if st.session_state.game_over:
    st.error("💥 게임 오버!")

    if st.button("다시 시작"):
        st.session_state.snake = [(5, 5)]
        st.session_state.food = (
            random.randint(0, SIZE-1),
            random.randint(0, SIZE-1)
        )
        st.session_state.direction = "RIGHT"
        st.session_state.game_over = False

# 게임 속도
time.sleep(0.3)
st.rerun()
