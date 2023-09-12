import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import os


st.set_page_config(
    page_title="PDF Chat", page_icon="https://www.svgrepo.com/download/484943/pdf-file.svg",layout="wide",
    menu_items={        
        'About': "# LLM App Demos!"
    }
)

st.image('app/logo.png')
st.markdown("""# **<img src="https://www.svgrepo.com/download/484943/pdf-file.svg" alt="drawing" width="50"/> PDF Chat using Langchain.** """,unsafe_allow_html=True)

#sidebar contents

with st.sidebar:
    st.session_state['api_key'] = st.text_input("OpenAI API Key",type="password")
    os.environ["OPENAI_API_KEY"] = st.session_state['api_key']
    api_key = st.session_state['api_key']
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/abhijeetnazar)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/abhijeetnazar)"

st.sidebar.markdown("""<small>It's always good practice to verify that a website is safe before giving it your API key. 
                        This site is open source, so you can check the code yourself, or run the streamlit app locally.</small>""", unsafe_allow_html=True)

@st.cache_resource()
def generate_embeddings(pdf):
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text+= page.extract_text()

    #langchain_textspliter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
    chunks = text_splitter.split_text(text=text)
    embeddings = OpenAIEmbeddings()
    #Store the chunks part in db (vector)
    vectorstore = FAISS.from_texts(chunks,embedding=embeddings)
    return vectorstore
    

def main():
    col1, col2 = st.columns(2)
    
    with col1:
        #upload a your pdf file
        pdf = st.file_uploader("Upload your PDF", type='pdf')

        if not api_key:
            st.info("Please enter OpenAI key.")
            st.stop()
            
        if pdf is not None:
            vectorstore = generate_embeddings(pdf)
            
            #Accept user questions/query
            query = st.text_input("Ask questions about related your upload pdf file")
            with st.spinner("Thinking..."):
                if query:
                    docs = vectorstore.similarity_search(query=query,k=3)
                    
                    #openai rank lnv process
                    llm = ChatOpenAI(model="gpt-3.5-turbo-0613",temperature=0)
                    chain = load_qa_chain(llm=llm, chain_type= "stuff")
                    
                    with get_openai_callback() as cb:
                        response = chain.run(input_documents = docs, question = query)
                        print(cb)
                    st.write(response)

if __name__=="__main__":
    main()