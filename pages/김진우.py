# app.py

```python
import streamlit as st
import random

st.set_page_config(
    page_title="시험범위 예상문제 생성기",
    page_icon="📚",
    layout="centered"
)

st.title("📚 시험범위 예상문제 생성기")
st.write("시험범위를 입력하면 예상문제를 만들어줍니다.")

exam_range = st.text_area(
    "시험 범위를 입력하세요",
    placeholder="""
예시:
경우의 수
순열
조합
"""
)

if st.button("📝 예상문제 만들기"):
    if exam_range.strip() == "":
        st.warning("시험 범위를 입력해주세요.")
    else:
        topics = [x.strip() for x in exam_range.split("\n") if x.strip()]

        st.subheader("예상문제")

        for i, topic in enumerate(topics, 1):
            question_type = random.choice(["단답형", "서술형", "개념 설명"])

            if question_type == "단답형":
                st.markdown(f"""
### 문제 {i}
**[{topic}]의 정의를 쓰시오.**
""")

            elif question_type == "서술형":
                st.markdown(f"""
### 문제 {i}
**[{topic}]의 특징과 활용 예시를 서술하시오.**
""")

            else:
                st.markdown(f"""
### 문제 {i}
**[{topic}]에 대해 설명하시오.**
""")

            st.divider()
```

# requirements.txt

```txt
streamlit
```

# GitHub 업로드 방법

1. 새 저장소 생성
2. app.py 업로드
3. requirements.txt 업로드
4. Streamlit Community Cloud 연결
5. app.py 선택 후 Deploy
