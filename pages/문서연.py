import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="TimeMaster",
    page_icon="⏰",
    layout="wide"
)

# -----------------------
# 세션 상태 초기화
# -----------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# -----------------------
# 함수
# -----------------------
def add_task(title, priority):
    st.session_state.tasks.append({
        "업무": title,
        "우선순위": priority,
        "완료": False,
        "생성시간": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

def calculate_score(total, completed):
    if total == 0:
        return 0

    score = int((completed / total) * 100)
    return score

# -----------------------
# 제목
# -----------------------
st.title("⏰ TimeMaster")
st.caption("업무 관리 + 포모도로 + 생산성 분석")

# -----------------------
# 사이드바
# -----------------------
with st.sidebar:
    st.header("➕ 업무 추가")

    task_name = st.text_input("업무명")

    priority = st.selectbox(
        "우선순위",
        ["높음", "보통", "낮음"]
    )

    if st.button("업무 추가"):
        if task_name.strip():
            add_task(task_name.strip(), priority)
            st.success("업무가 추가되었습니다.")
            st.rerun()
        else:
            st.warning("업무명을 입력하세요.")

    st.divider()

    st.header("🍅 포모도로 타이머")

    pomodoro_minutes = st.number_input(
        "집중 시간(분)",
        min_value=1,
        max_value=120,
        value=25
    )

    st.info(f"권장 집중시간: {pomodoro_minutes}분")

# -----------------------
# 업무 데이터
# -----------------------
tasks = st.session_state.tasks

total_tasks = len(tasks)
completed_tasks = sum(task["완료"] for task in tasks)

progress = (
    completed_tasks / total_tasks * 100
    if total_tasks > 0 else 0
)

score = calculate_score(
    total_tasks,
    completed_tasks
)

# -----------------------
# KPI
# -----------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("전체 업무", total_tasks)
col2.metric("완료 업무", completed_tasks)
col3.metric("진행률", f"{progress:.1f}%")
col4.metric("생산성 점수", score)

st.progress(progress / 100 if progress > 0 else 0)

# -----------------------
# 생산성 평가
# -----------------------
if score >= 90:
    st.success("🏆 매우 우수")
elif score >= 70:
    st.info("🚀 우수")
elif score >= 50:
    st.warning("🙂 보통")
else:
    st.error("📈 개선 필요")

st.divider()

# -----------------------
# 업무 목록
# -----------------------
st.subheader("📋 오늘의 업무")

if not tasks:
    st.info("등록된 업무가 없습니다.")
else:
    delete_index = None

    for idx, task in enumerate(tasks):

        col1, col2, col3, col4 = st.columns(
            [5, 2, 2, 1]
        )

        with col1:
            st.write(task["업무"])

        with col2:
            st.write(task["우선순위"])

        with col3:
            checked = st.checkbox(
                "완료",
                value=task["완료"],
                key=f"check_{idx}"
            )

            st.session_state.tasks[idx]["완료"] = checked

        with col4:
            if st.button(
                "❌",
                key=f"delete_{idx}"
            ):
                delete_index = idx

    if delete_index is not None:
        st.session_state.tasks.pop(delete_index)
        st.rerun()

# -----------------------
# 분석 영역
# -----------------------
st.divider()

st.subheader("📊 우선순위 분석")

if tasks:

    df = pd.DataFrame(tasks)

    priority_count = (
        df["우선순위"]
        .value_counts()
        .reset_index()
    )

    priority_count.columns = [
        "우선순위",
        "개수"
    ]

    fig = px.bar(
        priority_count,
        x="우선순위",
        y="개수",
        color="우선순위",
        title="우선순위별 업무 분포"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.info("분석할 데이터가 없습니다.")

# -----------------------
# 업무 데이터 보기
# -----------------------
st.divider()

st.subheader("🗂 업무 데이터")

if tasks:
    st.dataframe(
        pd.DataFrame(tasks),
        use_container_width=True
    )

    csv = pd.DataFrame(tasks).to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "CSV 다운로드",
        csv,
        file_name="timemaster_tasks.csv",
        mime="text/csv"
    )

else:
    st.info("저장된 업무가 없습니다.")
