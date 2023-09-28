from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORGANIZATION_IDS = os.getenv("OPENAI_ORGANIZATION_IDS").split(',')
USE_TEST_SET = os.getenv("USE_TEST_SET", "false") == "true"
N_EPOCHS = int(os.getenv("N_EPOCHS", "5"))
MODEL = os.getenv("MODEL", "gpt-3.5-turbo")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "3800"))
