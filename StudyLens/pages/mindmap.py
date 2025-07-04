import streamlit as st
import openai
from PyPDF2 import PdfReader
import streamlit.components.v1 as components

# Replace with your OpenAI API key
OPENAI_API_KEY = "add-your-own-api-key"

def configure_openai():
    """Configure OpenAI with the API key."""
    if not OPENAI_API_KEY:
        st.error("API Key is missing. Please provide a valid OpenAI API key.")
        return False
    openai.api_key = OPENAI_API_KEY
    return True

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file."""
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if not text.strip():
            st.warning("No text could be extracted from the PDF.")
            return None
        return text.strip()
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def create_mindmap_markdown(text):
    """Generate mindmap markdown using OpenAI."""
    try:
        max_chars = 30000
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
            st.warning(f"Text was truncated to {max_chars} characters.")

        prompt = f"""
Create a hierarchical markdown mindmap from the following text. 
Use proper markdown heading syntax (# for main topics, ## for subtopics, ### for details).
Focus on the main concepts and their relationships.
Include relevant details and connections between ideas.
Keep the structure clean and organized.

Format the output exactly like this example:
# Main Topic
## Subtopic 1
### Detail 1
- Key point 1
- Key point 2
### Detail 2
## Subtopic 2
### Detail 3
### Detail 4

Text to analyze: {text}

Respond only with the markdown mindmap, no additional explanation.
"""

        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2048
        )
        markdown = response.choices[0].message.content
        return markdown.strip()
    except Exception as e:
        st.error(f"Error generating mindmap: {str(e)}")
        return None

def create_markmap_html(markdown_content):
    markdown_content = markdown_content.replace('`', '\\`').replace('${', '\\${')
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            #mindmap {{
                width: 100%;
                height: 600px;
                margin: 0;
                padding: 0;
            }}
        </style>
        <script src="https://cdn.jsdelivr.net/npm/d3@6"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-view"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-lib@0.14.3/dist/browser/index.min.js"></script>
    </head>
    <body>
        <svg id="mindmap"></svg>
        <script>
            window.onload = async () => {{
                try {{
                    const markdown = `{markdown_content}`;
                    const transformer = new markmap.Transformer();
                    const {{root}} = transformer.transform(markdown);
                    const mm = new markmap.Markmap(document.querySelector('#mindmap'), {{
                        maxWidth: 300,
                        color: (node) => {{
                            const level = node.depth;
                            return ['#2196f3', '#4caf50', '#ff9800', '#f44336'][level % 4];
                        }},
                        paddingX: 16,
                        autoFit: true,
                        initialExpandLevel: 2,
                        duration: 500,
                    }});
                    mm.setData(root);
                    mm.fit();
                }} catch (error) {{
                    console.error('Error rendering mindmap:', error);
                    document.body.innerHTML = '<p style="color: red;">Error rendering mindmap. Please check the console for details.</p>';
                }}
            }};
        </script>
    </body>
    </html>
    """
    return html_content

def main():
    st.title("🧠 Mind Map Generator")
    if not configure_openai():
        return

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        with st.spinner("🔄 Processing PDF and generating mindmap..."):
            text = extract_text_from_pdf(uploaded_file)
            if text:
                st.info(f"Successfully extracted {len(text)} characters from PDF")
                markdown_content = create_mindmap_markdown(text)
                if markdown_content:
                    tab1, tab2 = st.tabs(["📊 Mindmap", "📝 Markdown"])
                    with tab1:
                        st.subheader("Interactive Mindmap")
                        html_content = create_markmap_html(markdown_content)
                        components.html(html_content, height=700, scrolling=True)
                    with tab2:
                        st.subheader("Generated Markdown")
                        st.text_area("Markdown Content", markdown_content, height=400)
                        st.download_button(
                            label="⬇️ Download Markdown",
                            data=markdown_content,
                            file_name="mindmap.md",
                            mime="text/markdown"
                        )

if __name__ == "__main__":
    main()

app = main
