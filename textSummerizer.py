from summa import summarizer
import streamlit as st

# Set page title and icon
st.set_page_config(page_title="Text Summarization", page_icon="✅")

# Add a colorful title
st.title("📚 Text Summarization")

# Sidebar with file uploader and ratio slider
st.sidebar.title("Options")
uploaded_file = st.sidebar.file_uploader("Upload a Text File (.txt)", type=["txt"])
ratio = st.sidebar.slider("Summarization Fraction", min_value=0.1, max_value=1.0, value=0.5, step=0.05)

# Main content area
st.markdown("---")  # Horizontal line for separation

if uploaded_file:
    # Read the uploaded text file and decode it to a Unicode (str) object
    input_text = uploaded_file.read().decode('utf-8')

    # Generate a summary using Summa
    summarized_text = summarizer.summarize(input_text, ratio=ratio, language="english", split=True, scores=True)

    # Post-process the summary for better structure and context
    summary_sentences = []
    for sentence, score in summarized_text:
        if len(sentence) > 30:  # Filter out very short sentences
            summary_sentences.append(sentence)

    # Display the improved summary
    st.markdown("### Summary:")
    for i, sentence in enumerate(summary_sentences):
        st.write(f"{i + 1}. {sentence}")

# Footer
st.markdown("---")  # Horizontal line for separation
st.markdown("Created with ❤️ by Your Name")
