import streamlit as st

st.set_page_config(
    page_title="Heart Completion Tracker",
    page_icon="❤️",
    layout="centered"
)

# ------------------------
# 세션 상태
# ------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ------------------------
# 함수
# ------------------------
def heart_display(level):
    return "❤️" * level + "🤍" * (5 - level)

# ------------------------
# 제목
# ------------------------
st.title("❤️ Heart Completion Tracker")
st.caption("하트를 클릭하여 과제의 완성도를 관리하세요")

# ------------------------
# 과제 추가
# ------------------------
st.subheader("➕ 새 과제 추가")

with st.form("add_task"):

    task_name = st.text_input("과제 이름")

    submitted = st.form_submit_button("추가")

    if submitted:

        try:
            if not task_name.strip():
                st.error("과제 이름을 입력하세요.")
            else:
                st.session_state.tasks.append({
                    "name": task_name,
                    "progress": 0
                })
                st.success("과제가 추가되었습니다.")
                st.rerun()

        except Exception as e:
            st.error(f"오류 발생: {e}")

# ------------------------
# 과제 목록
# ------------------------
st.divider()

st.subheader("📋 과제 목록")

if not st.session_state.tasks:

    st.info("등록된 과제가 없습니다.")

else:

    completed_count = 0

    for idx, task in enumerate(st.session_state.tasks):

        st.markdown("---")

        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown(f"### {task['name']}")

        with col2:
            if st.button("🗑", key=f"delete_{idx}"):
                st.session_state.tasks.pop(idx)
                st.rerun()

        # 하트 표시
        st.markdown(
            f"## {heart_display(task['progress'])}"
        )

        # 하트 클릭 영역
        heart_cols = st.columns(5)

        for heart_idx in range(5):

            if heart_cols[heart_idx].button(
                "❤️",
                key=f"heart_{idx}_{heart_idx}"
            ):
                st.session_state.tasks[idx]["progress"] = heart_idx + 1
                st.rerun()

        progress_percent = task["progress"] * 20

        st.write(f"완성도: {progress_percent}%")

        if task["progress"] == 5:
            completed_count += 1
            st.success("🏆 완료!")

# ------------------------
# 통계
# ------------------------
if st.session_state.tasks:

    st.divider()

    st.subheader("📊 진행 현황")

    total_tasks = len(st.session_state.tasks)

    completed_tasks = len(
        [
            t for t in st.session_state.tasks
            if t["progress"] == 5
        ]
    )

    average_progress = round(
        sum(
            t["progress"]
            for t in st.session_state.tasks
        ) / total_tasks * 20
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "전체 과제",
        total_tasks
    )

    col2.metric(
        "완료 과제",
        completed_tasks
    )

    col3.metric(
        "평균 완성도",
        f"{average_progress}%"
    )

# ------------------------
# 전체 삭제
# ------------------------
st.divider()

if st.button("🗑 전체 과제 삭제"):

    try:
        st.session_state.tasks = []
        st.rerun()

    except Exception as e:
        st.error(f"삭제 오류: {e}")
