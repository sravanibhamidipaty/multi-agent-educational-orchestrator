from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
CHROMA_PATH: str | None = os.getenv("CHROMA_PATH")
TEXT_DIR: str | None = os.getenv("TEXT_DIR")
PDF_DIR: str | None = os.getenv("PDF_DIR")
REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
LOG_PATH: str = os.getenv("LOG_PATH", "./logs/conversation.jsonl")