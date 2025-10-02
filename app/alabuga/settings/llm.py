from alabuga.settings import config

LLM_PROVIDER = config("LLM_PROVIDER", default="server.apps.llm.providers.GPTProvider")
OPENAI_ASSISTANT_ID = config("OPENAI_ASSISTANT_ID", "")
OLLAMA_HOST = config("OLLAMA_HOST", default="http://localhost:11434")
OPENAI_API_KEY = config("OPENAI_API_KEY", default="", cast=str)
OPENAI_PROXY_URL = config("OPENAI_PROXY_URL", default="", cast=str)
