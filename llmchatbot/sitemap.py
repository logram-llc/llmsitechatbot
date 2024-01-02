from collections.abc import Generator
from lxml import etree
from requests import RequestException, Session
from llmchatbot.__version__ import __version__


class SitemapParser:
    def __init__(self):
        self.session = Session()
        self.session.headers.update({"User-Agent": f"llmchatbot Scraper v{__version__}"})

    def _fetch_sitemap(self, url: str) -> bytes | None:
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.content
        except RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def _parse_sitemap(self, xml_content: bytes | None) -> Generator[str, None, None]:
        root = etree.fromstring(xml_content)
        namespace = {"sitemap": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        if root.tag == "{http://www.sitemaps.org/schemas/sitemap/0.9}sitemapindex":
            # Sitemap index file
            for sitemap in root.findall("sitemap:sitemap", namespace):
                loc = sitemap.find("sitemap:loc", namespace).text
                yield from self._parse_sitemap(self._fetch_sitemap(loc))
        else:
            for url in root.findall("sitemap:url", namespace):
                loc = url.find("sitemap:loc", namespace).text
                yield loc

    def get_all_urls(self, sitemap_url: str) -> list[str]:
        """Recursively fetch all URLs in a sitemap"""
        xml_content = self._fetch_sitemap(sitemap_url)
        if xml_content:
            return list(self._parse_sitemap(xml_content))
        else:
            return []
