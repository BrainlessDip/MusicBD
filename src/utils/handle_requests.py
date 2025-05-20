import aiohttp
from bs4 import BeautifulSoup

async def fetch_content(url: str) -> BeautifulSoup:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; MusicScraperBot/1.0)"
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
         html = await response.text()
         return BeautifulSoup(html, "html.parser")