import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Heart Potion Progress Tracker",
    page_icon="❤️",
    layout="centered"
)

# --------------------------
# 세션 상태
# --------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --------------------------
# 스타일
# --------------------------
st.markdown("""
<style>
.potion {
    font-size: 40px;
}
.task-card {
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #dddddd;
    margin-bottom: 10px;
}
.complete {
    color: green;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# 제목
# --------------------------
st.title("❤️ Heart Potion Progress Tracker")
st.caption("하트 물약병으로 과제 완성도를 관리하세요")

# --------------------------
# 하트 물약병 생성 함수
# --------------------------
def make_potion_bar(level):
    filled = "❤️🧪" * level
    empty = "🤍🧪" * (5 - level)
    return filled + empty

# --------------------------
# 입력
# --------------------------
with st.form("task_form"):

    task_name = st.text_input(
        "과제 또는 업무 이름"
    )

    progress = st.slider(
        "완성도",
        min_value=1,
        max_value=5,
        value=3
    )

    submitted = st.form_submit_button("추가")

    if submitted:

        try:

            if not task_name.strip():
                st.error("과제명을 입력하세요.")
            else:

                st.session_state.tasks.append({
                    "과제": task_name,
                    "레벨": progress
                })

                st.success("과제가 추가되었습니다.")

        except Exception as e:
            st.error(f"오류 발생: {e}")

# --------------------------
# 목록 표시
# --------------------------
st.divider()

st.subheader("📋 과제 목록")

if not st.session_state.tasks:

    st.info("등록된 과제가 없습니다.")

else:

    for idx, task in enumerate(st.session_state.tasks):

        level = task["레벨"]
        percent = level * 20

        st.markdown('<div class="task-card">', unsafe_allow_html=True)

        st.write(f"### {task['과제']}")

        st.markdown(
            f'<div class="potion">{make_potion_bar(level)}</div>',
            unsafe_allow_html=True
        )

        st.write(f"완성도: {percent}%")

        if level == 5:
            st.success("🏆 완료!")

        st.markdown("</div>", unsafe_allow_html=True)

# --------------------------
# 전체 평균
# --------------------------
if st.session_state.tasks:

    avg = sum(
        task["레벨"]
        for task in st.session_state.tasks
    ) / len(st.session_state.tasks)

    avg_percent = round(avg * 20)

    st.divider()

    st.subheader("📊 전체 진행률")

    st.metric(
        "평균 완성도",
        f"{avg_percent}%"
    )

    if avg_percent >= 80:
        st.success("매우 좋은 진행 상태입니다!")
    elif avg_percent >= 60:
        st.info("순조롭게 진행 중입니다.")
    else:
        st.warning("조금 더 집중이 필요합니다.")

# --------------------------
# 전체 삭제
# --------------------------
st.divider()

if st.button("🗑 전체 과제 삭제"):

    try:
        st.session_state.tasks = []
        st.rerun()
    except Exception as e:
        st.error(f"삭제 오류: {e}")
