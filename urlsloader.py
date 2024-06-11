from langchain.document_loaders import NewsURLLoader


urls = ['https://www.nytimes.com/2024/03/23/world/asia/india-election-federalism.html',
        'https://www.britannica.com/biography/Narendra-Modi',
        'https://www.abc.net.au/news/2024-03-12/narendra-modi-india-election-secret-past/103442558']

loder = NewsURLLoader(urls=urls)
data = loder.load()
print(data)

#AIzaSyAFL2r9kxHmL6oBiXTawkUWXM_RZlW7jOE