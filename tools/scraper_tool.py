# tools/scraper_tool.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from crewai.tools.base_tool import BaseTool

class WebsiteScraperTool(BaseTool):
    # Pydantic v2 requires annotated overrides of model fields
    name: str = "website_scraper"
    description: str = "Scrapes a website and returns its text content and main image URL."

    def _run(self, url: str) -> dict:
        """
        Sync implementation of the tool.
        """
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            for s in soup(["script", "style"]):
                s.extract()

            text = " ".join(soup.stripped_strings)[:8000]
            images = [urljoin(url, img.get('src')) for img in soup.find_all('img') if img.get('src')]
            hero_image = images[0] if images else None

            return {"text_content": text, "hero_image_url": hero_image}
        except Exception as e:
            return {"error": str(e)}

    async def _arun(self, url: str) -> dict:
        """
        Async version of the tool.
        """
        return self._run(url)
