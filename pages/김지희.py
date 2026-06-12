```python
import streamlit as st
import pandas as pd
from math import ceil

st.set_page_config(
    page_title="StudySprint",
    page_icon="📚",
    layout="centered"
)

st.title("📚 StudySprint")
st.subheader("시험기간 시간관리 도우미")

st.write("시험 과목과 범위를 입력하면 공부 시간표를 자동으로 만들어줍니다!")

# -----------------------------
# 이미지 업로드
# -----------------------------
st.header("🖼️ 공부 참고 이미지 업로드")

uploaded_file = st.file_uploader(
    "필기, 교과서, 시간표 사진 등을 업로드하세요",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:
    st.image(uploaded_file, caption="업로드한 이미지", use_container_width=True)

# -----------------------------
# 입력 영역
# -----------------------------
st.header("✏️ 시험 정보 입력")

num_subjects = st.number_input(
    "과목 개수",
    min_value=1,
    max_value=10,
    value=3
)

subjects = []

for i in range(num_subjects):
    st.markdown(f"### 과목 {i+1}")

    name = st.text_input(
        f"과목명 {i+1}",
        key=f"name_{i}"
    )

    scope = st.text_area(
        f"시험 범위 {i+1}",
        key=f"scope_{i}"
    )

    difficulty = st.slider(
        f"난이도 {i+1}",
        min_value=1,
        max_value=5,
        value=3,
        key=f"diff_{i}"
    )

    subjects.append({
        "name": name,
        "scope": scope,
        "difficulty": difficulty
    })

days_left = st.number_input(
    "시험까지 남은 일수",
    min_value=1,
    max_value=60,
    value=7
)

daily_hours = st.number_input(
    "하루 공부 가능 시간",
    min_value=1,
    max_value=24,
    value=4
)

# -----------------------------
# 시간표 생성
# -----------------------------
if st.button("📅 공부 시간표 만들기"):

    try:
        valid_subjects = [
            s for s in subjects
            if s["name"].strip() != ""
        ]

        if not valid_subjects:
            st.error("과목명을 최소 1개 이상 입력해주세요.")
        else:

            total_weight = sum(s["difficulty"] for s in valid_subjects)
            total_hours = days_left * daily_hours

            result = []

            for s in valid_subjects:
                allocated_hours = round(
                    (s["difficulty"] / total_weight) * total_hours,
                    1
                )

                per_day = round(allocated_hours / days_left, 1)

                result.append({
                    "과목": s["name"],
                    "시험 범위": s["scope"],
                    "총 공부 시간": f"{allocated_hours}시간",
                    "하루 권장 시간": f"{per_day}시간"
                })

            df = pd.DataFrame(result)

            st.success("시간표 생성 완료!")

            st.subheader("📋 추천 공부 계획")
            st.dataframe(df, use_container_width=True)

            st.subheader("🔥 공부 팁")

            st.info(
                """
                ✔ 어려운 과목은 오전에 공부하기  
                ✔ 50분 공부 + 10분 휴식 추천  
                ✔ 자기 전 암기과목 복습 추천  
                ✔ 하루 최소 6시간 수면 유지하기
                """
            )

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
```

