from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
import streamlit as st
from langchain.llms import VertexAI
from google.cloud import aiplatform
from google.oauth2 import service_account
from io import StringIO
import json
import os
from multiprocessing import Process
import sys


st.set_page_config(
    page_title="Multi Model Chat", page_icon="https://cdn-icons-png.flaticon.com/64/2232/2232241.png?filename=database_2232241.png&fd=1",layout="wide",
    menu_items={        
        'About': "# LLM App Demos!"
    }
)

st.image('app/logo.png')
st.markdown(
            """# **<img src="https://cdn-icons-png.flaticon.com/64/2232/2232241.png?filename=database_2232241.png&fd=1" alt="drawing" width="50"/> Database Chat with Multiple Models.**
""",unsafe_allow_html=True,
)

with st.expander(label="Sample database connection"):
    st.code("""snowflake://{user}:{password}@{account_name}/{database_name}/{schema_name}?warehouse={warehouse} \noracle+cx_oracle://{user}:{password}@{host}:{port}/?service_name={service}""")
    
with st.expander(label="Sample questions:"):
    st.markdown("""
                - Show number of order per year in table format. Also show difference with previous year.
                - Describe Cusomer table.
                - Show total orders placed by each customer with customer name.
                """,unsafe_allow_html=True)

with st.sidebar:
    st.session_state['db_string'] = st.text_input("Database String")
    with st.expander(label="Open AI Details:"):
        st.session_state['api_key'] = st.text_input("OpenAI API Key",type="password")
        os.environ["OPENAI_API_KEY"] = st.session_state['api_key']
    with st.expander(label="Google Cloud Details:"):
        google_sa = st.file_uploader('Google Service Account',  type="json")
        if google_sa is not None:
            client_credentials = json.loads(StringIO(google_sa.getvalue().decode("utf-8")).read())
            credentials = service_account.Credentials.from_service_account_info(client_credentials)
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/abhijeetnazar)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/abhijeetnazar)"

st.sidebar.markdown("""<small>It's always good practice to verify that a website is safe before giving it your API key. 
                        This site is open source, so you can check the code yourself, or run the streamlit app locally.</small>""", unsafe_allow_html=True)

@st.cache_resource(ttl=100)
def connect_database():
    db = SQLDatabase.from_uri(st.session_state.db_string)
    return db
    

# st.session_state['api_key']

try:
    if st.session_state.db_string:
        db = connect_database()
        st.write("Database connected...")
        if st.session_state['api_key']:
            llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
            toolkit = SQLDatabaseToolkit(db=db, llm=llm)
            openai_agent = create_sql_agent(llm=llm,toolkit=toolkit,agent_type=AgentType.OPENAI_FUNCTIONS)
        if google_sa:            
            aiplatform.init(project='bespin-us-demo',credentials=credentials)
            llm = VertexAI(model_name="text-bison")
            toolkit = SQLDatabaseToolkit(db=db, llm=llm)
            google_agent = create_sql_agent(llm=llm,toolkit=toolkit,agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
        if not(st.session_state['api_key'] and google_sa):
            st.stop()
        question = st.text_input("Ask something about the data:",on_change=None)    
        if question:
            with st.spinner('Hangon. Generating output...'):
                # p1 = Process(target = google_agent.run(question))
                # ga_response = p1.start()
                # p2 = Process(target = openai_agent.run(question))
                # openai_response = p2.start()
                ga_response = google_agent.run(question)
                openai_response = openai_agent.run(question)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown( """# **<img src="https://techcrunch.com/wp-content/uploads/2021/05/VertexAI-512-color.png" alt="drawing" width="50"/> Vertex AI.**""",unsafe_allow_html=True,)
                # st.write("### Answer")
                st.write(ga_response)
            with col2:
                st.markdown( """# **<img src="https://static-00.iconduck.com/assets.00/openai-icon-505x512-pr6amibw.png" alt="drawing" width="50"/> Open AI.**""",unsafe_allow_html=True,)
                # st.write("### Answer")
                st.write(openai_response)
        else:
            st.info("Please enter your question above:")
    else:
        st.info("Please input Open AI API key and database details.")
except Exception as e:
    st.error("Please check your details." + str(e))
    st.cache_resource.clear()
