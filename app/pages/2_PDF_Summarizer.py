import os
import streamlit as st

from utils import (
    doc_loader, summary_prompt_creator, doc_to_final_summary,
)
from my_prompts import file_map, file_combine
from streamlit_app_utils import check_key_validity, create_temp_file, create_chat_model, token_limit, token_minimum

st.set_page_config(
    page_title="PDF Summarizer", page_icon="https://www.svgrepo.com/download/484943/pdf-file.svg",layout="wide",
    menu_items={        
        'About': "# LLM App Demos!"
    }
)

with st.sidebar:
    api_key = st.text_input("OpenAI API Key",type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/abhijeetnazar)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/abhijeetnazar)"

st.sidebar.markdown("""<small>It's always good practice to verify that a website is safe before giving it your API key. 
                        This site is open source, so you can check the code yourself, or run the streamlit app locally.</small>""", unsafe_allow_html=True)

st.image('app/logo.png')
st.markdown(
            """# **<img src="https://www.svgrepo.com/download/484943/pdf-file.svg" alt="drawing" width="50"/> PDF Summarizer using Langchain**
""",unsafe_allow_html=True,
)

def main():
    """
    The main function for the Streamlit app.
    :return: None.
    """
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("Upload a document to summarize, 10k to 100k tokens works best!", type=['txt', 'pdf'])

        # api_key = st.text_input("Enter API key here, or contact the author if you don't have one.")
    
        if st.button('Summarize'):
            process_summarize_button(uploaded_file, api_key)


def process_summarize_button(file_or_transcript, api_key, file=True):
    """
    Processes the summarize button, and displays the summary if input and doc size are valid
    :param file_or_transcript: The file uploaded by the user or the transcript from the YouTube URL
    :param api_key: The API key entered by the user
    :return: None
    """
    if not validate_input(file_or_transcript, api_key):
        return

    with st.spinner("Summarizing... please wait..."):
        
        temp_file_path = create_temp_file(file_or_transcript)
        doc = doc_loader(temp_file_path)
        map_prompt = file_map
        combine_prompt = file_combine
        
        llm = create_chat_model(api_key)
        initial_prompt_list = summary_prompt_creator(map_prompt, 'text', llm)
        final_prompt_list = summary_prompt_creator(combine_prompt, 'text', llm)

        if not validate_doc_size(doc):
            if file:
                os.unlink(temp_file_path)
            return

        summary = doc_to_final_summary(doc, 10, initial_prompt_list, final_prompt_list, api_key)
            
        st.markdown(summary, unsafe_allow_html=True)
        if file:
            os.unlink(temp_file_path)


def validate_doc_size(doc):
    """
    Validates the size of the document
    :param doc: doc to validate
    :return: True if the doc is valid, False otherwise
    """
    if not token_limit(doc, 800000):
        st.warning('File or transcript too big!')
        return False

    if not token_minimum(doc, 2000):
        st.warning('File or transcript too small!')
        return False
    return True


def validate_input(file_or_transcript, api_key):
    """
    Validates the user input, and displays warnings if the input is invalid
    :param file_or_transcript: The file uploaded by the user or the YouTube URL entered by the user
    :param api_key: The API key entered by the user
    :return: True if the input is valid, False otherwise
    """
    if file_or_transcript == None:
        st.info("Please upload a file.")
        return False

    if not check_key_validity(api_key):
        st.info("Please input Open AI API key.")
        return False

    return True


if __name__ == '__main__':
    main()
