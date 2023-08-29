from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORGANIZATION_IDS = os.getenv("OPENAI_ORGANIZATION_IDS").split(',')