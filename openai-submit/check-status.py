import openai
from constants import OPENAI_API_KEY, OPENAI_ORGANIZATION_IDS
        
if __name__ == '__main__':
  openai.api_key = OPENAI_API_KEY
  jobs = []
  for organization_id in OPENAI_ORGANIZATION_IDS:
    jobs += openai.FineTuningJob.list(
      organization=organization_id,
      limit=10
    )["data"]
  print(jobs)