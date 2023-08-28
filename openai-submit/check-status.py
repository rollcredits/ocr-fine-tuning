import openai
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        
if __name__ == '__main__':
  openai.api_key = OPENAI_API_KEY
  jobs = openai.FineTuningJob.list(limit=10)
  print(jobs)