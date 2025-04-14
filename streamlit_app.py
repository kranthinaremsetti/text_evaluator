import streamlit as st
from PIL import Image
from langdetect import detect
import random

# Only import and use language_tool_python if running locally
try:
    import language_tool_python
    tool = language_tool_python.LanguageTool('en-US')
    
    def evaluate_text(text):
        matches = tool.check(text)
        issues = [match for match in matches]
        score = 100 - (len(issues) * 2)
        return score, issues
except ModuleNotFoundError:
    tool = None  # If not available, set to None

# Quiz generation
def generate_quiz(text):
    sentences = text.split('.')
    questions = []
    for sentence in sentences:
        words = sentence.split()
        if len(words) > 4:
            blank_word = random.choice(words)
            question = f"Fill in the blank: {sentence.replace(blank_word, '______')}"
            correct_answer = blank_word
            incorrect_answers = random.sample([w for w in words if w != correct_answer], min(3, len(words)-1))
            options = [correct_answer] + incorrect_answers
            random.shuffle(options)
            questions.append({"question": question, "options": options, "answer": correct_answer})
    return questions

# Streamlit UI
st.set_page_config(page_title="Text Understanding App", layout="wide")
st.title("🧠 Text Understanding & Quiz Generator")

tab1, tab2 = st.tabs(["📜 Text Input", "🖼️ Image Upload"])

with tab1:
    st.header("Text Understanding & Quiz")
    user_text = st.text_area("Enter text for quiz generation:", height=200)

    if user_text.strip():
        st.subheader("🔍 Language Detection")
        lang = detect(user_text) if len(user_text.split()) >= 2 else "en"
        st.success(f"Language: {lang}")

        if tool:
            st.subheader("📊 Text Evaluation")
            score, issues = evaluate_text(user_text)
            st.metric(label="Grammar Score", value=f"{score}/100")

            st.subheader("📋 Grammar Issues")
            if issues:
                for issue in issues[:5]:
                    st.write(f"• {issue.message} (suggestion: {issue.replacements})")
        else:
            st.warning("Grammar checking is disabled on Streamlit Cloud due to missing dependencies.")

        st.subheader("❓ Quiz Generator")
        quiz_questions = generate_quiz(user_text)
        for i, q in enumerate(quiz_questions, 1):
            st.markdown(f"**Q{i}:** {q['question']}")
            st.write(f"Options: {', '.join(q['options'])}")
            st.write(f"Answer: {q['answer']}")

with tab2:
    st.header("Upload an Image with Text")
    uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        st.subheader("📝 Extracted Text")
        # No OCR here, keep it as is or modify based on your OCR choice
        st.text_area("OCR Result", "Text extraction here", height=200)
