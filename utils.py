from model import  NewsArticle
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults
from langchain.text_splitter import RecursiveCharacterTextSplitter,CharacterTextSplitter
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain.document_loaders import NewsURLLoader,WebBaseLoader
from langchain.chains.summarize import  load_summarize_chain
from langchain.prompts import  PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from duckduckgo_search import DDGS
from prompt import  prompt as fprompt
import requests as rq
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


prompt_template = """Write a concise summary of the following:
"{text}"
CONCISE SUMMARY:"""
prompt = PromptTemplate.from_template(prompt_template)


@st.cache_resource
def load_WebData(urls):
    loader = NewsURLLoader(urls)
    data = loader.load()
    return data



@st.cache_data
def TextSplitter(_docs):
    # text_splitter = CharacterTextSplitter(chunk_size=1000,chunk_overlap=20,separator=[' ','\n'])
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50,
                                                   separators=['\n\n', '\n', '.', ','], )
    # context = "\n".join(str(p.page_content) for p in _docs)
    data = text_splitter.split_text(_docs)
    # data = text_splitter.split_documents(documents=_docs)
    return data

# @st.cache_resource
# def CreateKnowledgeBase(texts,_embeddings):
#     kb = FAISS.from_texts(texts=texts, embedding=_embeddings)
#     return kb.as_retriever(k=3, search_type='similarity')

def Summarization(llm,docs):
    chain = load_summarize_chain(llm=llm,prompt=prompt,chain_type="stuff",verbose=True)
    result = chain.run(docs)
    return result

def FinalAnswer(llm,docs,query):
    chain = LLMChain(llm=llm,prompt=fprompt,output_key="output")
    result = chain({'query':query,'content':docs})['output']
    return result

def searchWithDuckDuckGo(query: str):
    search = DDGS()
    news = search.news(query, max_results=5, region='in-en')
    # wrappers = DuckDuckGoSearchAPIWrapper(max_results=5, time='y', region="in-in")
    # search = DuckDuckGoSearchResults(api_wrapper=wrappers, source="news")
    # results = NewsArticle.ProcessSearch(search.run(query))
    # print(results.values())
    # NewsArticle(results)
    urls = []
    for i in range(len(news)):
        urls.append(news[i]['url'])
    return urls

def Extract_data(html):
    if html:
        soup = BeautifulSoup(html,'lxml')
#         titles = soup.find('h1')
#         if titles:
#             title = [t.get_text() for t in titles]
#         else:
#             title = []
        paragraghs = soup.find_all('p')
        text = [p.get_text() for p in paragraghs]
#         return [title,text]
        return text
    return []

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered_text = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_text)


# res = searchWithDuckDuckGo("who is modi")
# news = NewsArticle(res)
# data = load_WebData(news.urls)
# print(data)
# print(news.urls)
# print(res.values())
# print(NewsArticle(res).urls)
