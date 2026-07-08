import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 AI Study Buddy")
st.write("Learn any topic with simple explanations, real-life examples, quizzes, and feedback.")

st.sidebar.title("About This Project")
st.sidebar.write(
    """
    AI Study Buddy is a beginner-friendly AI tutor built using Streamlit and Google Gemini API.
    It explains concepts, gives examples, creates quizzes, and provides feedback on learner answers.
    """
)

# Gemini API key is NOT stored in GitHub.
# It will be added privately in Streamlit Cloud Secrets.
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key is missing. Please add GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

topic = st.text_input("Enter a Topic")

option = st.selectbox(
    "Choose Activity",
    [
        "Explain Concept",
        "Real-Life Example",
        "Generate Quiz",
        "Evaluate My Answer",
        "Ask Anything"
    ]
)

learner_answer = ""

if option == "Evaluate My Answer":
    learner_answer = st.text_area("Write your answer here")

if st.button("Generate"):
    if topic.strip() == "":
        st.warning("Please enter a topic.")

    elif option == "Evaluate My Answer" and learner_answer.strip() == "":
        st.warning("Please write your answer for feedback.")

    else:
        if option == "Explain Concept":
            prompt = f"""
            You are an AI Study Buddy for beginner students.
            Explain the topic "{topic}" in simple language.

            Include:
            1. Simple definition
            2. Step-by-step explanation
            3. Important points
            4. Small summary
            """

        elif option == "Real-Life Example":
            prompt = f"""
            You are an AI Study Buddy.
            Give one simple real-life example of the topic "{topic}".
            Make it easy for a beginner student to understand.
            Explain how the example connects to the concept.
            """

        elif option == "Generate Quiz":
            prompt = f"""
            You are an AI quiz tutor.
            Create 5 multiple-choice questions on "{topic}".
            Give 4 options for each question.
            Also provide the correct answer and a short explanation.
            """

        elif option == "Evaluate My Answer":
            prompt = f"""
            You are an AI Study Buddy.
            Evaluate the learner's answer for the topic "{topic}".

            Learner answer:
            "{learner_answer}"

            Give:
            1. Whether the answer is correct, partially correct, or incorrect
            2. What is good in the answer
            3. What is missing
            4. Improved answer
            5. Encouraging feedback
            """

        else:
            prompt = f"""
            You are an AI Study Buddy.
            Answer this student question in simple language:
            {topic}
            """

        try:
            with st.spinner("Generating your learning response..."):
                response = model.generate_content(prompt)

            st.markdown("### AI Study Buddy Response")
            st.markdown(response.text)
            st.info("Note: This response is AI-generated. Please verify important academic information.")

        except Exception as e:
            st.error("Something went wrong while generating the response.")
            st.write(e)