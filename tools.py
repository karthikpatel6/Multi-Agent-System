from langchain.tools import tool
from dotenv import load_dotenv
load_dotenv()
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
import requests
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str:
    """Search the web for recent and realiable information on a topic. Returns Titles,URLs and snippets"""
    results = tavily.search(query=query,max_results=3)
    out = []
    for r in results['results']:
        out.append(
            f"Title {r['title']}\n URL {r['url']}\n Snippets: {r['content'][:300]}\n"
        )
    
    return "\n---------\n".join(out)

@tool 
def scrape_url(url : str) -> str:
    """Scrape and return clean text content from the given URL for deeper reading"""
    try:
        resp = requests.get(url,timeout=8,headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text,"html.parser")
        for tag in soup(["script","style","nav","footer"]):
            tag.decompose()
        return soup.get_text(separator=" ",strip=True)[:3000]
    except Exception as e:
        return f"Could not able to scrap the URL: {str(e)}"
