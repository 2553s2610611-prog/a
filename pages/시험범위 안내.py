import streamlit as st

st.set_page_config(
    page_title="📚 시험범위 정리 도우미",
    page_icon="📚",
    layout="wide"
)

# CSS
st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}
.title {
    text-align:center;
    font-size:45px;
    font-weight:bold;
    color:#2563eb;
}
.subtitle {
    text-align:center;
    color:gray;
}
.result-box {
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 0px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>📚 시험범위 정리 도우미</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>시험범위를 입력하면 보기 쉽게 정리해드립니다.</div>", unsafe_allow_html=True)

st.divider()

subject = st.selectbox(
    "과목 선택",
    ["국어", "수학", "영어", "과학", "사회", "기타"]
)

exam_range = st.text_area(
    "시험 범위를 입력하세요",
    placeholder="""
예시)
1. 경우의 수
2. 순열
3. 조합
4. 확률의 기본 성질
"""
)

if st.button("✨ 정리하기", use_container_width=True):

    if exam_range.strip() == "":
        st.warning("시험 범위를 입력해주세요.")
    else:
        topics = [x.strip() for x in exam_range.split("\n") if x.strip()]

        st.success("정리가 완료되었습니다!")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📌 핵심 개념")

            for i, topic in enumerate(topics, 1):
                st.markdown(f"""
                <div class='result-box'>
                <b>{i}. {topic}</b><br>
                중요 개념을 반드시 이해하기
                </div><br>
                """, unsafe_allow_html=True)

        with col2:
            st.subheader("🔥 암기 포인트")

            for topic in topics:
                st.info(f"✔ {topic} 관련 공식 및 정의 암기")

        st.divider()

        st.subheader("📝 예상 문제")

        for topic in topics:
            st.markdown(f"""
            **Q. {topic}에 대해 설명하시오.**

            - 핵심 개념 작성
            - 예시 제시
            - 활용 방법 설명
            """)

        st.divider()

        progress = min(len(topics) * 20, 100)

        st.subheader("🎯 시험 준비도")
        st.progress(progress)

        if progress >= 80:
            st.success("시험 준비가 거의 완료되었습니다!")
        else:
            st.warning("조금 더 학습이 필요합니다.")
