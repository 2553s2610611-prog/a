import streamlit as st
import pandas as pd
from datetime import datetime
import time

st.set_page_config(
    page_title="TimeMaster",
    page_icon="⏰",
    layout="wide"
)

# -------------------------
# 세션 상태 초기화
# -------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

# -------------------------
# 제목
# -------------------------
st.title("⏰ TimeMaster")
st.caption("스마트 시간관리 대시보드")

# -------------------------
# 사이드바
# -------------------------
st.sidebar.header("📋 새 업무 추가")

with st.sidebar.form("task_form"):
    task_name = st.text_input("업무명")

    priority = st.selectbox(
        "우선순위",
        ["높음", "중간", "낮음"]
    )

    estimated_time = st.number_input(
        "예상 소요 시간(분)",
        min_value=1,
        value=30
    )

    submit = st.form_submit_button("추가")

    if submit:
        if task_name.strip():
            st.session_state.tasks.append({
                "업무": task_name,
                "우선순위": priority,
                "예상시간": estimated_time,
                "완료": False,
                "생성일": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.success("업무가 추가되었습니다.")
        else:
            st.error("업무명을 입력하세요.")

# -------------------------
# 메인 레이아웃
# -------------------------
col1, col2 = st.columns([2, 1])

# =========================
# 업무 관리
# =========================
with col1:

    st.subheader("✅ 오늘의 업무")

    if not st.session_state.tasks:
        st.info("등록된 업무가 없습니다.")
    else:

        for idx, task in enumerate(st.session_state.tasks):

            cols = st.columns([0.1, 0.5, 0.2, 0.2])

            completed = cols[0].checkbox(
                "",
                value=task["완료"],
                key=f"check_{idx}"
            )

            st.session_state.tasks[idx]["완료"] = completed

            cols[1].write(task["업무"])
            cols[2].write(task["우선순위"])
            cols[3].write(f"{task['예상시간']}분")

        st.divider()

        if st.button("🗑 완료된 업무 삭제"):
            st.session_state.tasks = [
                t for t in st.session_state.tasks
                if not t["완료"]
            ]
            st.rerun()

# =========================
# 통계
# =========================
with col2:

    st.subheader("📊 생산성 분석")

    total_tasks = len(st.session_state.tasks)

    completed_tasks = len([
        t for t in st.session_state.tasks
        if t["완료"]
    ])

    pending_tasks = total_tasks - completed_tasks

    productivity_score = (
        round((completed_tasks / total_tasks) * 100, 1)
        if total_tasks > 0 else 0
    )

    total_time = sum(
        t["예상시간"]
        for t in st.session_state.tasks
    )

    st.metric("전체 업무", total_tasks)
    st.metric("완료 업무", completed_tasks)
    st.metric("남은 업무", pending_tasks)
    st.metric("생산성 점수", f"{productivity_score}%")
    st.metric("예상 총 시간", f"{total_time}분")

# -------------------------
# 업무 분석
# -------------------------
st.divider()
st.subheader("📈 업무 분석")

if st.session_state.tasks:

    df = pd.DataFrame(st.session_state.tasks)

    priority_count = (
        df["우선순위"]
        .value_counts()
        .reset_index()
    )

    priority_count.columns = ["우선순위", "개수"]

    st.bar_chart(
        priority_count.set_index("우선순위")
    )

else:
    st.info("분석할 데이터가 없습니다.")

# -------------------------
# 포모도로 타이머
# -------------------------
st.divider()
st.subheader("🍅 포모도로 타이머")

pomodoro_minutes = st.slider(
    "집중 시간(분)",
    1,
    60,
    25
)

if st.button("타이머 시작"):

    placeholder = st.empty()

    try:
        for remaining in range(
            pomodoro_minutes * 60,
            -1,
            -1
        ):

            mins = remaining // 60
            secs = remaining % 60

            placeholder.metric(
                "남은 시간",
                f"{mins:02d}:{secs:02d}"
            )

            time.sleep(1)

        st.success("🎉 집중 시간이 종료되었습니다!")

    except Exception as e:
        st.error(f"타이머 오류: {e}")

# -------------------------
# 오늘의 조언
# -------------------------
st.divider()

tips = [
    "가장 중요한 업무부터 시작하세요.",
    "25분 집중 + 5분 휴식을 시도해보세요.",
    "멀티태스킹보다 단일 작업이 효율적입니다.",
    "업무를 작은 단위로 나누면 실행하기 쉽습니다.",
    "하루 목표를 3개만 정해보세요."
]

day_index = datetime.now().day % len(tips)

st.subheader("💡 오늘의 시간관리 팁")
st.success(tips[day_index])
