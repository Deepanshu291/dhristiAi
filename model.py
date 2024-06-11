from typing import  Any
import requests as rq

class NewsArticle:
    def __init__(self, article_dict):
        self.article_dict = article_dict
        self.titles = list(article_dict.keys())
        self.urls = list(article_dict.values())

    def get_titles(self):
        """Returns a list of all article titles."""
        return self.titles

    def get_urls(self):
        """Returns a list of all article URLs."""
        return self.urls

    def ProcessSearch(input_string: str) -> dict[Any,Any]:
        result = []
        start_index = input_string.find("title: ")  # Find the first occurrence of "title: "
        while start_index != -1:
            end_index = input_string.find("],", start_index)  # Find the end of the snippet
            if end_index == -1:
                break
            snippet = input_string[start_index:end_index]
            snippet_text = snippet.split("title: ")[1].strip()  # Extract the snippet text
            result.append(snippet_text)
            start_index = input_string.find("title: ", end_index)  # Move to the next snippet
        dictxt = dict()
        for itm in result:
            # print(f"{itm} \n")
            title, link = itm.split(", link: ")
            dictxt[title] = link
        return dictxt

class Scraper:
        def __init__(self, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"):
            self.session = rq.Session()
            self.session.headers.update({"User-Agent": user_agent})

        def fetch_data(self, url):
            try:
                response = self.session.get(url, timeout=2)
                if response.status_code == 200:
                    return response.text
            except rq.exceptions.RequestException as e:
                print(f"Error {url}:{e}")
            return None