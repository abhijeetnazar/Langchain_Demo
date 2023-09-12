from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
import streamlit as st
import os

st.set_page_config(
    page_title="Database Chat", page_icon="https://cdn-icons-png.flaticon.com/64/2232/2232241.png?filename=database_2232241.png&fd=1",layout="wide",
    menu_items={        
        'About': "# LLM App Demos!"
    }
)

st.image('app/logo.png')
st.markdown(
            """# **<img src="https://cdn-icons-png.flaticon.com/64/2232/2232241.png?filename=database_2232241.png&fd=1" alt="drawing" width="50"/> Database Chat using Langchain**
The app demonstrates the use of OpenAI to support getting insights from database by just asking questions. The assistant can also generate SQL code for the Questions.
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
    st.session_state['api_key'] = st.text_input("OpenAI API Key",type="password")
    os.environ["OPENAI_API_KEY"] = st.session_state['api_key']
    st.session_state['db_string'] = st.text_input("Database String")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/abhijeetnazar)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/abhijeetnazar)"

st.sidebar.markdown("""<small>It's always good practice to verify that a website is safe before giving it your API key. 
                        This site is open source, so you can check the code yourself, or run the streamlit app locally.</small>""", unsafe_allow_html=True)

@st.cache_resource(ttl=100)
def connect_database():
    db = SQLDatabase.from_uri(st.session_state.db_string)
    toolkit = SQLDatabaseToolkit(db=db, llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"))
    agent_executor = create_sql_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )
    return agent_executor

try:
    if st.session_state['api_key'] and st.session_state.db_string:
        agent_executor = connect_database()
        st.write("Database connected...")
        question = st.text_input("Ask something about the data:",on_change=None)
        if question:
            with st.spinner('Hangon. Generating output...'):
                    response = agent_executor.run(question)
            st.write("### Answer")
            st.write(response)
        else:
            st.info("Please enter your question above:")
    else:
        st.info("Please input Open AI API key and database details.")
except Exception as e:
    st.error("Please check your details." + str(e))
    st.cache_resource.clear()
