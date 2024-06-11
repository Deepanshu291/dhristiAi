import time
import streamlit as st
from langchain.embeddings import GooglePalmEmbeddings
from langchain_google_genai import GoogleGenerativeAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.document_loaders import PyMuPDFLoader, PyPDFLoader, UnstructuredURLLoader
from langchain.vectorstores.chroma import Chroma
from langchain.text_splitter import  CharacterTextSplitter
from utils import *

searchai = DuckDuckGoSearchRun()

if __name__ == '__main__':
    st.title("Dhristi AI")
    st.subheader("This AI help for Research and Development")
    infoC = st.empty()
    infoC.info("Please Enter Your Gemini API key...😊😊 ")
    # api = ""
    stb = st.sidebar
    with stb:
        st.header("Dhristi AI")
        st.subheader("")
        GeminiApi = st.text_input("Gemini Api Key",placeholder="Enter your Gemini API Key",type="password")
        st.divider()

        if GeminiApi:
            llm = GoogleGenerativeAI(google_api_key=GeminiApi,temperature=0.5,model="gemini-pro")

        st.title("Search History")
        if "search" not in st.session_state:
            st.session_state.search = []

        for i,search in enumerate(st.session_state.search):
            st.write(f"{i}. {search}")

        btn = st.button("Clear Search History")
        if btn:
            st.session_state.search.clear()


    if GeminiApi :
        infoC.empty()

    user_input = st.text_input("Enter your Query",disabled= not GeminiApi)
    if user_input:
        stsContainer = st.sidebar.empty()
        with stsContainer.status("Searching.....",expanded=True) as sts:
            st.info("Search Query from DuckDuckGo search Engine...")
            res = searchWithDuckDuckGo(user_input)
            st.info("Extracting Urls....")
            urls = NewsArticle(res).urls
            st.info("Loading News Articles....")
            docs = load_WebData(urls=urls)
            sts.update(label="Loading Web Data...", state="running")
            st.info("Text Spliting....")
            splitdocs = TextSplitter(_docs=docs)
            sts.update(label="Load Knowledge Base", state='running')
            st.info("Loading Google Embedding...")
            # embedding = GooglePalmEmbeddings(google_api_key=GeminiApi, show_progress_bar=True)
            st.info("Create VectoreStore....")
            # vectoreStore = CreateKnowledgeBase(texts=text, _embeddings=embedding)
            sts.update(label="All Done...", state='complete', expanded=False)

        stsContainer.empty()

        st.subheader("AI ReSearch:")
        with st.spinner(text="AI Thinking about Research..."):
            # result = Summarization(llm=llm, docs=docs)
            print(type(docs))
            search = searchai.run(user_input)
            result = docs[0]
            # result = Summarization(llm=llm,docs=docs[0])
             # result = vectoreStore
        st.markdown(f"### AI Response \n {result} \n \n ### Search context \n {urls}", unsafe_allow_html=True)




