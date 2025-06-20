import streamlit as st
import openai
import os
import re

# Set the OpenAI API key (replace with your actual key for testing)
# For production, use environment variables or Streamlit secrets
OPENAI_API_KEY = "add-your-own-api-key"  # Replace with your valid key or comment out to use env variable

# Try to fetch from environment variables or Streamlit secrets
if not OPENAI_API_KEY:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate API key
if not OPENAI_API_KEY or OPENAI_API_KEY == "your-actual-key-here":
    st.error("API key is missing. Please set a valid OpenAI API key in the code (OPENAI_API_KEY variable) or as an environment variable (OPENAI_API_KEY).")
    st.stop()

# Initialize OpenAI client
try:
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    st.error(f"Invalid API key or OpenAI configuration error: {e}")
    st.stop()

# Function to generate MCQs using OpenAI
def generate_mcqs(text_content):
    prompt = f"""
    Generate 10 unique multiple-choice questions (MCQs) based on the following content:

    Content:
    \"\"\"{text_content}\"\"

    Each question must have 4 options and clearly mention the correct answer separately like:
    Q1: <question text>
    Options:
    a) option 1
    b) option 2
    c) option 3
    d) option 4
    Answer: b

    Return in the exact same format. Only output the questions, options, and answers.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        generated_text = response.choices[0].message.content
        return parse_mcqs(generated_text)
    
    except Exception as e:
        st.error(f"Error generating quiz: {e}")
        return []

# Function to parse the LLM output into questions
def parse_mcqs(text):
    questions = []
    lines = text.strip().split('\n')
    q = None
    for line in lines:
        line = line.strip()
        if line.startswith("Q"):
            if q:
                questions.append(q)
            q = {'question': line.split(": ", 1)[1], 'options': {}, 'answer': None}
        elif line.startswith(("a)", "b)", "c)", "d)")):
            option_letter = line[0]
            option_text = line[3:].strip()
            q['options'][option_letter] = option_text
        elif line.startswith("Answer:"):
            q['answer'] = line.split(":")[1].strip()
    if q:
        questions.append(q)
    return questions

# Streamlit app
def app():
    st.title("🧠 Quiz Generator")

    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "quiz_generated" not in st.session_state:
        st.session_state.quiz_generated = False

    # Text area to enter content
    text_content = st.text_area("Paste the content here to generate a quiz:", height=200)

    if st.button("Create Quiz"):
        if text_content.strip():
            with st.spinner('Generating quiz...'):
                st.session_state.questions = generate_mcqs(text_content)
                st.session_state.user_answers = {}
                st.session_state.quiz_generated = True
            if st.session_state.questions:
                st.success("Quiz Generated! 🎯")
            else:
                st.error("Failed to generate quiz. Please try again.")
        else:
            st.warning("Please paste some content first!")

    # Display the questions if quiz has been generated
    if st.session_state.quiz_generated and st.session_state.questions:
        st.subheader("📚 Answer the Questions")
        
        for idx, q in enumerate(st.session_state.questions):
            st.write(f"**Q{idx+1}. {q['question']}**")
            options = [f"{k}) {v}" for k, v in q['options'].items()]
            choice = st.radio(f"Select an option for Question {idx+1}", options, key=f"q_{idx}")
            st.session_state.user_answers[idx] = choice

        if st.button("Submit"):
            score = 0
            result = []
            
            for idx, q in enumerate(st.session_state.questions):
                selected_answer = st.session_state.user_answers.get(idx, "")
                # Extract the option letter from the selected answer (e.g., "a) text" -> "a")
                selected_letter = selected_answer[0] if selected_answer and selected_answer[1] == ")" else None
                correct_answer = q['answer'].lower()

                if selected_letter and selected_letter.lower() == correct_answer:
                    score += 1
                    result.append(f"Q{idx+1}: Correct! Your answer: {q['options'][selected_letter]}")
                else:
                    correct_text = q['options'].get(correct_answer, "Unknown")
                    result.append(f"Q{idx+1}: Incorrect! Your answer: {selected_answer} | Correct answer: {correct_text}")

            st.success(f"✅ You scored {score}/{len(st.session_state.questions)}!")
            st.write("### Results Summary:")
            for res in result:
                st.write(res)

# Only run if this file is executed directly
if __name__ == "__main__":
    app()
