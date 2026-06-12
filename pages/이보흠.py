import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Sleep & Study Planner",
    page_icon="📚",
    layout="centered"
)

st.title("📚 Sleep & Study Planner")
st.markdown("숙면과 공부시간을 균형 있게 관리하는 시간표 생성기")

st.divider()

try:
    st.subheader("😴 수면 시간 설정")

    sleep_time = st.time_input(
        "취침 시간",
        value=datetime.strptime("23:00", "%H:%M").time()
    )

    wake_time = st.time_input(
        "기상 시간",
        value=datetime.strptime("07:00", "%H:%M").time()
    )

    sleep_start = datetime.combine(datetime.today(), sleep_time)
    wake_start = datetime.combine(datetime.today(), wake_time)

    if wake_start <= sleep_start:
        wake_start += timedelta(days=1)

    sleep_hours = round(
        (wake_start - sleep_start).total_seconds() / 3600,
        1
    )

    st.success(f"예상 수면 시간: {sleep_hours}시간")

    st.divider()

    st.subheader("📖 공부 목표 설정")

    total_study = st.slider(
        "하루 공부 목표 시간",
        min_value=1,
        max_value=15,
        value=6
    )

    subject_count = st.number_input(
        "과목 수",
        min_value=1,
        max_value=10,
        value=3
    )

    subjects = []
    ratios = []

    for i in range(subject_count):
        col1, col2 = st.columns([2, 1])

        with col1:
            subject = st.text_input(
                f"과목 {i+1}",
                value=f"과목{i+1}",
                key=f"sub{i}"
            )

        with col2:
            ratio = st.number_input(
                f"비율 {i+1}",
                min_value=1,
                max_value=100,
                value=int(100 / subject_count),
                key=f"ratio{i}"
            )

        subjects.append(subject)
        ratios.append(ratio)

    total_ratio = sum(ratios)

    if total_ratio != 100:
        st.warning(
            f"과목 비율의 합이 현재 {total_ratio}% 입니다. 100%로 맞춰주세요."
        )

    st.divider()

    if st.button("📅 시간표 생성", use_container_width=True):

        if total_ratio != 100:
            st.error("과목 비율 합계를 100%로 맞춰주세요.")
            st.stop()

        available_time = 24 - sleep_hours

        if total_study > available_time:
            st.error("공부 시간이 하루 사용 가능한 시간을 초과했습니다.")
            st.stop()

        schedule = []

        current_time = wake_start

        for subject, ratio in zip(subjects, ratios):
            study_hours = round(total_study * ratio / 100, 2)

            start_time = current_time
            end_time = current_time + timedelta(hours=study_hours)

            schedule.append([
                subject,
                start_time.strftime("%H:%M"),
                end_time.strftime("%H:%M"),
                round(study_hours, 2)
            ])

            current_time = end_time

        df = pd.DataFrame(
            schedule,
            columns=[
                "과목",
                "시작",
                "종료",
                "공부시간(시간)"
            ]
        )

        st.subheader("🗓 생성된 시간표")
        st.dataframe(df, use_container_width=True)

        st.subheader("📊 하루 시간 분석")

        other_time = round(
            24 - sleep_hours - total_study,
            1
        )

        labels = [
            "수면",
            "공부",
            "기타"
        ]

        values = [
            sleep_hours,
            total_study,
            other_time
        ]

        fig, ax = plt.subplots(figsize=(5, 5))

        ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%"
        )

        ax.axis("equal")

        st.pyplot(fig)

        st.subheader("💡 건강도 분석")

        if sleep_hours < 7:
            st.warning(
                "수면 시간이 부족합니다. 최소 7시간 이상 수면을 권장합니다."
            )
        else:
            st.success(
                "적절한 수면 시간을 확보하고 있습니다."
            )

        if total_study > 10:
            st.warning(
                "공부 시간이 매우 많습니다. 휴식 시간을 충분히 확보하세요."
            )
        else:
            st.info(
                "공부 시간이 적절한 수준입니다."
            )

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
