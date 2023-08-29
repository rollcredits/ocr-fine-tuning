import argparse
import os
import json
import random
import openai
import time
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_TEST_SET=False
N_EPOCHS=5

def read_file(folder, filename):
    with open(os.path.join(folder, filename), 'r') as f:
        return f.read()

def write_to_file_jsonl(filename, data):
    with open(filename, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')

def poll_finetuning_job(job_id, interval=60):
    while True:
        job_status = openai.FineTuningJob.retrieve(job_id)
        status = job_status['status']
        if status == 'succeeded':
            print(f"Fine-tuning job {job_id} completed.")
            print(job_status)
            return
        elif status == 'running':
            print(f"Fine-tuning job {job_id} still in progress. Checking again in {interval} seconds.")
            time.sleep(interval)
        else:
            print(f"Fine-tuning job {job_id} failed.")
            return

def main(prompt_folder, label_folder):
    prompt_files = [f for f in os.listdir(prompt_folder) if f.endswith('.txt')]
    label_files = [f for f in os.listdir(label_folder) if f.endswith('.json')]

    training_data = []
    test_data = []

    for prompt_file in prompt_files:
        prompt_content = read_file(prompt_folder, prompt_file)
        label_file = prompt_file.replace('.txt', '.json')
        if label_file in label_files:
            label_content = read_file(label_folder, label_file)
            training_example = {
                "messages": [
                    {"role": "user", "content": prompt_content},
                    {"role": "assistant", "content": label_content}
                ]
            }
            if random.uniform(0, 1) > 0.8 and USE_TEST_SET:
                test_data.append(training_example)
            else:
                training_data.append(training_example)

    write_to_file_jsonl('training_data.jsonl', training_data)
    write_to_file_jsonl('test_data.jsonl', test_data)

    user_input = input("Check the training and test data. Type 'y' to proceed: ")
    if user_input != 'y':
        print("Operation cancelled.")
        return

    openai.api_key = OPENAI_API_KEY

    training_data_file = openai.File.create(
        file=open("training_data.jsonl", "rb"),
        purpose='fine-tune'
    )
    if USE_TEST_SET:
        test_data_file = openai.File.create(
            file=open("test_data.jsonl", "rb"),
            purpose='fine-tune'
        )

    attempts = 0
    while True:
        try:
            attempts += 1
            if USE_TEST_SET:
                    training_job = openai.FineTuningJob.create(
                        training_file=training_data_file["id"],
                        validation_file=test_data_file["id"],
                        model="gpt-3.5-turbo",
                        hyperparameters={
                            "n_epochs": N_EPOCHS,
                        }
                    )            
            else:
                training_job = openai.FineTuningJob.create(
                    training_file=training_data_file["id"],
                    model="gpt-3.5-turbo",
                    hyperparameters={
                        "n_epochs": N_EPOCHS,
                    }
                )
            break
        except Exception as e:
            print(e)
            if attempts > 5:
                raise e
            time.sleep(10) # file is generally not ready immediately on OpenAI's end
    
    job_id = training_job['id']
    print(f"Fine-tuning job started with ID: {job_id}")
    poll_finetuning_job(job_id)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare data for GPT-3.5-turbo fine-tuning.')
    parser.add_argument('label_folder', help='Folder containing label .json files')
    parser.add_argument('prompt_folder', help='Folder containing prompt .txt files')
    args = parser.parse_args()
    main(args.prompt_folder, args.label_folder)
