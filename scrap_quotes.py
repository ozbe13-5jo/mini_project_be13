import requests
import asyncio
from bs4 import BeautifulSoup
from app.models.models import Quote
from app.db import init_db, close_db

URL = "http://quotes.toscrape.com/"

def fetch_quotes():
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = []
    for div in soup.select(".quote"):
        text = div.select_one(".text").get_text(strip=True)
        author = div.select_one(".author").get_text(strip=True)
        quotes.append({"quote_content": text, "author": author})
    return quotes

async def save_quotes(quotes):
    for q in quotes:
        exists = await Quote.exists(
            quote_content=q["quote_content"],
            author=q["author"]
        )
        if not exists:
            await Quote.create(**q)

async def main():
    await init_db()
    try:
        quotes = fetch_quotes()
        await save_quotes(quotes)
        print(f"{len(quotes)}개 명언 저장 완료 (중복 제외)")
    finally:
        await close_db()  # 연결 종료

if __name__ == "__main__":
    asyncio.run(main())
