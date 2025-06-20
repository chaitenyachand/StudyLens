# StudyLens

**StudyLens** is an educational productivity tool built using Python and Streamlit. It enables students to upload their study notes and generate learning aids such as summaries, mind maps, flashcards, and quizzes — all within a user-friendly web interface.

## Features

- **Upload Notes**: Supports `.pdf` and `.txt` files. Extracts text content for processing.
- **Summary Generator**: Implements frequency-based summarization using NLTK to condense text.
- **Mind Map**: Dynamically creates mind maps from input text using Graphviz.
- **Flashcards**: Generates keyword-based question-answer flashcards for active recall.
- **Quiz Generator**: Forms simple multiple-choice questions based on extracted terms and context.

## Project Structure

StudyLens/
│
├── main.py # Entry point with navigation and page loading
├── menu.py # Alternate file for rendering navigation
├── pages/
│ ├── upload.py # Handles file uploads and text extraction
│ ├── summary.py # Contains logic for summarization
│ ├── mindmap.py # Generates and renders mind maps
│ ├── flashcards.py # Builds flashcards from text
│ └── quiz.py # Constructs quizzes from extracted content

## Technologies Used

- **Python**
- **Streamlit** – Web UI framework
- **NLTK** – Natural Language Processing for text analysis and summarization
- **Graphviz** – For visual mind map generation
- **PyPDF2** – To read and extract text from PDF files
- **nest_asyncio** – To patch event loops in Streamlit for async support
- **Regular Expressions** – For basic keyword and pattern detection

## How It Works

1. User uploads study material (PDF or text).
2. The app extracts content and lets the user choose between:
   - Generating a summary
   - Creating a mind map
   - Generating flashcards
   - Taking a quiz
3. Each module is loaded dynamically using Python's importlib and displayed via the sidebar navigation.

## Limitations

- Summary and quiz logic are rule-based and may not cover deep semantic understanding.
- Flashcard generation may miss nuanced Q&A if input text lacks clear definitions.

## Future Scope

- Integrate large language models (e.g., GPT) for smarter content generation.
- Enable user account login and save study sessions.
- Add diagram/image-based support for mind maps.
