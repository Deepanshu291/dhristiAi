from langchain.prompts import PromptTemplate

template = """You are a text retriever and summarizer,ignore everything you know, 
return only the summarized text for the query: {query} into a maximum of 500 words. 
Output should be concise chunks of paragraphs, ignore links, 
using the scraped context:{content}
....
"""
prompt = PromptTemplate(template=template,input_variables=['query','content'])