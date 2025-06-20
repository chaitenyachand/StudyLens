import streamlit as st
import PyPDF2
import openai
import base64
from openai import OpenAI  # NEW

# Initialize OpenAI client
client = OpenAI(
    api_key="add-your-own-api-key"
)

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    extracted_text = " ".join([page.extract_text() or "" for page in pdf_reader.pages])
    return extracted_text.strip()

def split_text_into_chunks(text, chunk_size):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def generate_anki_flashcards(text, chunk_size, model_choice):
    text_chunks = split_text_into_chunks(text, chunk_size)
    flashcards = []

    for i, chunk in enumerate(text_chunks):
        message_prompt = [
            {"role": "system", "content": "You are a helpful assistant and specialist in creating flashcards."},
            {"role": "user", "content": f"Create 5 flashcards from this text. Format: 'Question: ... Answer: ...'. Keep it short and simple.\n\nText:\n{chunk}"}
        ]

        response = client.chat.completions.create(
            model=model_choice,
            messages=message_prompt,
            temperature=0.2,
            max_tokens=2048
        )

        generated_text = response.choices[0].message.content.strip()

        # Split into individual flashcards
        cards = []
        current_question = ""
        current_answer = ""

        for line in generated_text.splitlines():
            line = line.strip()
            if line.lower().startswith("question:"):
                if current_question and current_answer:
                    cards.append((current_question, current_answer))
                    current_answer = ""
                current_question = line[len("question:"):].strip()

            elif line.lower().startswith("answer:"):
                current_answer = line[len("answer:"):].strip()

        if current_question and current_answer:
            cards.append((current_question, current_answer))

        flashcards.extend(cards)

        break  # Process only first chunk

    return flashcards

def get_file_download_link(cards, filename):
    flashcards_text = '\n'.join([f"{q};{a}" for q, a in cards])
    b64 = base64.b64encode(flashcards_text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download Flashcards</a>'

def app():
    st.title('🃏Flashcard Generator')

    uploaded_file = st.file_uploader('Please upload your PDF file', type='pdf')

    chunk_size = st.number_input('Enter the chunk size (default 1000)', min_value=100, value=1000, step=100)

    model_choice = st.selectbox('Select AI model', ['gpt-3.5-turbo', 'gpt-4'])

    if uploaded_file is None:
        st.error('Please upload a PDF file.')
    elif st.button('Generate Flashcards'):
        pdf_text = extract_text_from_pdf(uploaded_file)

        if not pdf_text:
            st.warning('No extractable text found in the PDF.')
            st.stop()

        flashcards = generate_anki_flashcards(pdf_text, chunk_size, model_choice)

        if not flashcards:
            st.warning('No flashcards generated. Try a different PDF or smaller chunk size.')
            st.stop()

        st.success('Flashcards created!')

        # Display Flashcards
        st.subheader("📚 Flashcards Preview")
        for idx, (front, back) in enumerate(flashcards, 1):
            with st.expander(f"Flashcard {idx}: {front}"):
                st.write(f"**Answer:** {back}")

        # Download Link
        download_link = get_file_download_link(flashcards, 'flashcards.txt')
        st.markdown(download_link, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
