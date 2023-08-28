import openai

OPENAI_API_KEY="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"
        
if __name__ == '__main__':
  openai.api_key = OPENAI_API_KEY
  jobs = openai.FineTuningJob.list(limit=10)
  print(jobs)