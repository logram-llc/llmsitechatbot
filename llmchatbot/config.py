from dataclasses import dataclass
from json import loads as json_loads
from os import environ
from pathlib import Path


@dataclass(kw_only=True, frozen=True)
class Config:
    """App config"""

    llm_system_prompt: str
    llm_vector_store_path: str | None

    openai_api_url: str | None
    openai_api_key: str
    openai_model: str


def get_config_from_env() -> Config:
    """Get app config from environment variables"""
    return Config(
        llm_system_prompt=environ["LLMCHATBOT__LLM_SYSTEM_PROMPT"],
        llm_vector_store_path=environ["LLMCHATBOT__LLM_VECTOR_STORE_PATH"],
        openai_api_url=environ.get("LLMCHATBOT__OPENAI_API_URL"),
        openai_api_key=environ["LLMCHATBOT__OPENAI_API_KEY"],
        openai_model=environ.get("LLMCHATBOT__OPENAI_API_MODEL", "gpt-3.5-turbo"),
    )


def get_config_from_file(path: str) -> Config:
    """Get app config from a file"""
    config = json_loads(Path(path).read_text(encoding="utf-8"))

    return Config(
        llm_system_prompt=config.get("llm_system_prompt", "You are a helpful assistant."),
        llm_vector_store_path=config["llm_vector_store_path"],
        openai_api_url=config.get("openai_api_url"),
        openai_api_key=config["openai_api_key"],
        openai_model=config.get("openai_model", "gpt-3.5-turbo"),
    )
