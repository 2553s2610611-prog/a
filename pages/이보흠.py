
import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(
    page_title="시험기간 공부 도우미",
    page_icon="📚"
)

st.title("📚 시험기간 공부 & 숙면 시간표 챗봇")

# API 키 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# 모델 생성
try:
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
except Exception as e:
    st.error(f"모델 로딩 오류: {e}")
    st.stop()

# 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요! 😊\n\n"
                "시험 날짜, 과목, 기상 시간 등을 알려주시면\n"
                "공부 계획표와 숙면 시간표를 만들어 드립니다."
            )
        }
    ]

# 이전 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
user_input = st.chat_input("질문을 입력하세요")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        # 대화 기록 문자열 생성
        history = ""

        for msg in st.session_state.messages:
            role = "사용자" if msg["role"] == "user" else "챗봇"
            history += f"{role}: {msg['content']}\n"

        prompt = f"""
너는 고등학생 시험기간 공부 코치이다.

역할:
1. 공부 계획표 작성
2. 과목별 공부 우선순위 추천
3. 숙면을 고려한 시간표 작성
4. 무리한 밤샘 공부는 추천하지 말 것
5. 표 형태로 보기 쉽게 작성

대화 기록:
{history}
"""

        response = model.generate_content(prompt)

        answer = response.text

    except Exception as e:
        answer = f"오류가 발생했습니다.\n\n{e}"

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

# 초기화 버튼
if st.button("대화 초기화"):
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "대화가 초기화되었습니다. 다시 시작해 주세요!"
        }
    ]
    st.rerun()
