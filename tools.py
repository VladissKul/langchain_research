import requests
from pydantic import BaseModel, Field
from langchain.tools import tool
from langchain_community.llms import Ollama

llm = Ollama(model="llama3.2")


class WikipediaArticleExporter(BaseModel):
    article: str = Field(description="The canonical name of the Wikipedia article")


class SummarizeTextInput(BaseModel):
    text: str = Field(description="The text that needs to be summarized")


@tool("wikipedia_text_exporter", args_schema=WikipediaArticleExporter, return_direct=False)
def wikipedia_text_exporter(article: str) -> str:
    """Fetches the most recent revision for a Wikipedia article in WikiText format"""
    url = f"https://en.wikipedia.org/w/api.php?action=parse&page={article}&prop=wikitext&formatversion=2"
    result = requests.get(url).text

    start = result.find('"wikitext": "\{\{')
    end = result.find('\}</pre></div></div><!--esi')

    return {"text": str(result[start + 12: end - 30])}


@tool("summarize_text", args_schema=SummarizeTextInput, return_direct=False)
def summarize_text(text: str) -> str:
    """Creates a summary of the given text using the Ollama model"""
    prompt = f"Please summarize the following text:\n\n{text}\n\nSummarize in a concise manner."

    summary = llm.invoke(prompt)

    return summary


response = wikipedia_text_exporter.invoke({"article": "NASA"})

article_text = response["text"]

summary_response = summarize_text.invoke({"text": article_text})

print("Summary of the article:")
print(summary_response)
