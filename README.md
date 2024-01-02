# LLM Site Chabot

A simple CLI using OpenAI and LlamaIndex to answer questions about your website(s)

## Quick Start

```bash
# Install the CLI
git clone https://github.com/logram-llc/llmsitechatbot
cd llmsitechatbot
pip install -e .

# Copy and then configure config.json
cp config.sample.json config.json

# Build the index
llmchatbot --config config.json build https://logram.io/sitemap.xml https://api.logram.io/sitemap.xml

# Interact with the LLM through a CLI chat
llmchatbot --config config.json chat

# Interact with the LLM through an API 
llmchatbot --config config.json serve
curl -X POST http://localhost:8000 \
    -H "Content-Type: application/json" \
    -d '{"message": "Who is behind this company?"}'
```

## References

- [LLM App Dev Workshop](https://github.com/sroecker/LLM_AppDev-HandsOn/)
- [Build a chatbot with custom data sources, powered by LlamaIndex](https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/)
- [SQL Query Engine with LlamaIndex + DuckDB](https://gpt-index.readthedocs.io/en/latest/examples/index_structs/struct_indices/duckdb_sql_query.html)
- [AI on Openshift - LLMs, Chatbots, Talk with your Documentation](https://ai-on-openshift.io/demos/llm-chat-doc/llm-chat-doc/)
- [Open Sourcerers - A personal AI assistant for developers that doesn't phone home](https://www.opensourcerers.org/2023/11/06/a-personal-ai-assistant-for-developers-that-doesnt-phone-home/)

