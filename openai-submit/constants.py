from dotenv import load_dotenv
import os

load_dotenv()

USE_TEST_SET = os.getenv("USE_TEST_SET", "false") == "true"
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "3800"))
