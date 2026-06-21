from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHROMA_PATH = os.getenv("CHROMA_PATH")
TEXT_DIR = os.getenv("TEXT_DIR")
PDF_DIR = os.getenv("PDF_DIR")
