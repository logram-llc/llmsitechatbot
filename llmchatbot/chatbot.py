from llmchatbot.config import Config
from os import getcwd
from pathlib import Path
from subprocess import run as subprocess_run
from llama_index import ServiceContext, StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.llms import OpenAI
from llama_index.schema import MetadataMode
from llmchatbot.scraper import PlaywrightWebScraper
from llmchatbot.sitemap import SitemapParser


class Chatbot:
    def __init__(self, config: Config, verbose: bool = False) -> None:
        self.config = config
        self.verbose = verbose

        self.llm = OpenAI(
            model=config.openai_model, api_key=config.openai_api_key, api_base=config.openai_api_url
        )
        self.service_context = ServiceContext.from_defaults(llm=self.llm, embed_model="local")
        self.index: VectorStoreIndex | None = None

    def build_index(self, urls: list[str]) -> None:
        subprocess_run(["playwright", "install"], capture_output=True, text=True, check=True)

        scraper = PlaywrightWebScraper(sitemap_parser=SitemapParser())
        documents = scraper.scrape(urls)

        if self.verbose:
            (Path(getcwd()) / "processed-docs.txt").write_text(
                "\n---\n".join([doc.get_content(metadata_mode=MetadataMode.ALL) for doc in documents]),
                encoding="utf-8",
            )

        index = VectorStoreIndex.from_documents(
            documents,
            service_context=self.service_context,
            show_progress=self.verbose,
        )
        index.storage_context.persist(persist_dir=self.config.llm_vector_store_path)

    def load_index(self) -> VectorStoreIndex:
        storage_context = StorageContext.from_defaults(persist_dir=self.config.llm_vector_store_path)
        self.index = load_index_from_storage(
            storage_context=storage_context, service_context=self.service_context
        )

    def chat(self) -> None:
        if not self.index:
            raise ValueError("Must call `load_index`")
        query_engine = self.index.as_query_engine(
            chat_mode="context",
            verbose=self.verbose,
            streaming=True,
            system_prompt=self.config.llm_system_prompt,
        )
        while True:
            streaming_response = query_engine.query(input("\n> "))
            streaming_response.print_response_stream()

    def query(self, message: str) -> str | None:
        if not self.index:
            raise ValueError("Must call `load_index`")
        query_engine = self.index.as_query_engine(
            chat_mode="context",
            verbose=self.verbose,
            streaming=False,
            system_prompt=self.config.llm_system_prompt,
        )
        response = query_engine.query(message)
        return response.response
