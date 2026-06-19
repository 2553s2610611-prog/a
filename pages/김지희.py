import streamlit as st
import google.generativeai as genai
from datetime import date

st.set_page_config(
    page_title="시험기간 플래너 AI",
    page_icon="📚",
    layout="wide"
)

st.title("📚 시험기간 플래너 AI")
st.write("시험 과목과 범위를 입력하면 AI가 공부 시간표를 만들어줍니다.")

# API 설정
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# 시험 날짜
exam_date = st.date_input(
    "시험 시작 날짜",
    min_value=date.today()
)

days_left = (exam_date - date.today()).days

st.info(f"📅 시험까지 D-{days_left}")

st.subheader("과목 입력")

subject_count = st.number_input(
    "과목 수",
    min_value=1,
    max_value=10,
    value=3
)

subjects = []

for i in range(subject_count):
    st.markdown(f"### 과목 {i+1}")

    name = st.text_input(
        f"과목명 {i+1}",
        key=f"name{i}"
    )

    scope = st.text_area(
        f"시험 범위 {i+1}",
        key=f"scope{i}"
    )

    importance = st.slider(
        f"중요도 {i+1}",
        1,
        5,
        3,
        key=f"importance{i}"
    )

    subjects.append({
        "name": name,
        "scope": scope,
        "importance": importance
    })

st.subheader("📷 시험 자료 사진")

uploaded_files = st.file_uploader(
    "교과서, 프린트, 범위표 업로드",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    cols = st.columns(min(len(uploaded_files), 3))

    for idx, file in enumerate(uploaded_files):
        with cols[idx % len(cols)]:
            st.image(file, caption=file.name)

if st.button("📝 공부 계획 생성"):

    valid_subjects = [
        s for s in subjects
        if s["name"].strip() and s["scope"].strip()
    ]

    if not valid_subjects:
        st.warning("과목 정보를 입력해주세요.")
        st.stop()

    try:
        model = genai.GenerativeModel(
            "gemini-2.5-flash-lite"
        )

        subject_text = ""

        for s in valid_subjects:
            subject_text += (
                f"\n과목: {s['name']}"
                f"\n범위: {s['scope']}"
                f"\n중요도: {s['importance']}\n"
            )

        prompt = f"""
너는 학습 플래너 전문가다.

시험까지 {days_left}일 남았다.

다음 과목 정보를 바탕으로
현실적이고 실천 가능한 공부 계획을 작성해라.

{subject_text}

조건:
1. 날짜별 공부 계획 작성
2. 과목별 시간 배분 이유 설명
3. 복습 일정 포함
4. 보기 쉽게 표 형식 사용
5. 한국어로 작성
"""

        with st.spinner("AI가 시간표를 만드는 중..."):

            response = model.generate_content(prompt)

            st.success("공부 계획 생성 완료!")

            st.markdown(response.text)

    except Exception as e:
        st.error(f"AI 생성 중 오류 발생: {e}")

st.divider()

st.caption("Made with Streamlit + Gemini")
