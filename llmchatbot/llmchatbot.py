from argparse import ArgumentParser
from llmchatbot.config import get_config_from_env, get_config_from_file
from llmchatbot.chatbot import Chatbot
from llmchatbot import api
import uvicorn


def main():
    parser = ArgumentParser(description="Chat with your website")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--config", help="JSON config path")

    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    parser_build = subparsers.add_parser("build", help="Build the LLM index")
    parser_build.add_argument("urls", nargs="+", help="List of URLs to scrape")

    subparsers.add_parser("chat", help="Chat with the LLM")

    parser_serve = subparsers.add_parser("serve", help="Serve an API for the LLM")
    parser_serve.add_argument("--host", type=str, default="127.0.0.1", help="Host to run the server on")
    parser_serve.add_argument("--port", type=int, default=8000, help="Port to run the server on")

    args = parser.parse_args()
    config = get_config_from_file(args.config) if args.config else get_config_from_env()

    chatbot = Chatbot(config=config, verbose=args.verbose)

    if args.command == "build":
        chatbot.build_index(urls=args.urls)
    elif args.command in ("chat", "serve"):
        chatbot.load_index()

        if args.command == "chat":
            chatbot.chat()
        elif args.command == "serve":
            api.chatbot = chatbot
            uvicorn.run(api.app, host=args.host, port=args.port, reload=False)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
