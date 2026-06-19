import streamlit as st
import time

st.set_page_config(
    page_title="Tomato Focus Timer",
    page_icon="🍅",
    layout="centered"
)

# ------------------
# 세션 상태
# ------------------
if "running" not in st.session_state:
    st.session_state.running = False

if "paused" not in st.session_state:
    st.session_state.paused = False

if "mode" not in st.session_state:
    st.session_state.mode = "집중"

if "remaining_seconds" not in st.session_state:
    st.session_state.remaining_seconds = 25 * 60

if "total_seconds" not in st.session_state:
    st.session_state.total_seconds = 25 * 60

if "completed_sessions" not in st.session_state:
    st.session_state.completed_sessions = 0

# ------------------
# 제목
# ------------------
st.title("🍅 Tomato Focus Timer")
st.caption("집중과 휴식을 반복하는 포모도로 타이머")

# ------------------
# 설정
# ------------------
st.subheader("⚙️ 타이머 설정")

focus_minutes = st.number_input(
    "집중 시간 (분)",
    min_value=1,
    max_value=180,
    value=25
)

break_minutes = st.number_input(
    "휴식 시간 (분)",
    min_value=1,
    max_value=60,
    value=5
)

# ------------------
# 버튼
# ------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶ 시작"):
        if not st.session_state.running:
            st.session_state.running = True
            st.session_state.paused = False

            if st.session_state.remaining_seconds <= 0:
                st.session_state.mode = "집중"
                st.session_state.total_seconds = focus_minutes * 60
                st.session_state.remaining_seconds = focus_minutes * 60

with col2:
    if st.button("⏸ 일시정지"):
        st.session_state.paused = True

with col3:
    if st.button("🔄 초기화"):
        st.session_state.running = False
        st.session_state.paused = False
        st.session_state.mode = "집중"
        st.session_state.total_seconds = focus_minutes * 60
        st.session_state.remaining_seconds = focus_minutes * 60

# ------------------
# 타이머 표시
# ------------------
minutes = st.session_state.remaining_seconds // 60
seconds = st.session_state.remaining_seconds % 60

st.markdown(
    f"""
    <div style='text-align:center'>
        <div style='font-size:120px;'>🍅</div>
        <div style='font-size:60px;font-weight:bold;'>
            {minutes:02d}:{seconds:02d}
        </div>
        <div style='font-size:30px;color:#ff4b4b'>
            {st.session_state.mode} 모드
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------
# 진행률
# ------------------
progress = 1 - (
    st.session_state.remaining_seconds /
    st.session_state.total_seconds
)

progress = max(0, min(progress, 1))

st.progress(progress)

# ------------------
# 통계
# ------------------
st.subheader("🏆 오늘의 기록")

st.metric(
    "완료한 포모도로",
    st.session_state.completed_sessions
)

# ------------------
# 타이머 동작
# ------------------
if (
    st.session_state.running
    and not st.session_state.paused
):

    time.sleep(1)

    st.session_state.remaining_seconds -= 1

    if st.session_state.remaining_seconds <= 0:

        if st.session_state.mode == "집중":

            st.session_state.completed_sessions += 1

            st.session_state.mode = "휴식"

            st.session_state.total_seconds = break_minutes * 60
            st.session_state.remaining_seconds = break_minutes * 60

        else:

            st.session_state.mode = "집중"

            st.session_state.total_seconds = focus_minutes * 60
            st.session_state.remaining_seconds = focus_minutes * 60

    st.rerun()
