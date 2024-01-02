from typing import Protocol
import html2text
from bs4 import BeautifulSoup
from llama_index import Document
from playwright.sync_api import sync_playwright


class ISitemapParser(Protocol):
    def get_all_urls(self, sitemap_url: str) -> list[str]:
        ...


class IWebScraper(Protocol):
    def scrape(self, urls: list[str]) -> list[Document]:
        ...


class PlaywrightWebScraper(IWebScraper):
    def __init__(self, sitemap_parser: ISitemapParser) -> None:
        self.sitemap_parser = sitemap_parser

    def _expand_sitemap_urls(self, urls: list[str]) -> list[str]:
        processed_urls: list[str] = []
        for url in urls:
            if "sitemap" not in url:
                processed_urls += url
                continue

            processed_urls += self.sitemap_parser.get_all_urls(url)
        return processed_urls

    def scrape(self, urls: list[str]) -> list[Document]:
        documents: list[Document] = []
        all_urls = self._expand_sitemap_urls(urls)

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()

            for url in all_urls:
                page.goto(url, wait_until="networkidle")
                page.wait_for_timeout(3000)
                html_content = page.content()

                soup = BeautifulSoup(html_content, "html.parser")

                h2t = html2text.HTML2Text()
                h2t.ignore_links = False
                h2t.ignore_images = True
                markdown_content = h2t.handle((soup.select_one("main") or soup.select_one("body")).prettify())

                metadata = {}

                title_tag = soup.select_one('meta[property="og:title"]')
                if title_tag and title_tag.has_attr("content"):
                    metadata["og:title"] = title_tag["content"]

                url_tag = soup.select_one('meta[property="og:url"]')
                if url_tag and url_tag.has_attr("content"):
                    metadata["og:url"] = url_tag["content"]

                description_tag = soup.select_one('meta[property="og:description"]')
                if description_tag and description_tag.has_attr("content"):
                    metadata["og:description"] = description_tag["content"]

                documents.append(Document(text=markdown_content, metadata=metadata))

        return documents
