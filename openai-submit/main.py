import argparse
import os
import json
import random
import openai
import time

OPENAI_API_KEY="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"
USE_TEST_SET=False

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
        if job_status['status'] == 'completed':
            print(f"Fine-tuning job {job_id} completed.")
            print(job_status)
            return
        elif job_status['status'] == 'failed':
            print(f"Fine-tuning job {job_id} failed.")
            return
        else:
            print(f"Fine-tuning job {job_id} still in progress. Checking again in {interval} seconds.")
            time.sleep(interval)

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

    time.sleep(10) # wait for file to be ready on OpenAI's end

    if USE_TEST_SET:
        training_job = openai.FineTuningJob.create(
            training_file=training_data_file["id"],
            validation_file=test_data_file["id"],
            model="gpt-3.5-turbo"
        )
    else:
        training_job = openai.FineTuningJob.create(
            training_file=training_data_file["id"],
            model="gpt-3.5-turbo"
        )
    
    job_id = training_job['id']
    print(f"Fine-tuning job started with ID: {job_id}")
    poll_finetuning_job(job_id)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare data for GPT-3.5-turbo fine-tuning.')
    parser.add_argument('label_folder', help='Folder containing label .json files')
    parser.add_argument('prompt_folder', help='Folder containing prompt .txt files')
    args = parser.parse_args()
    main(args.prompt_folder, args.label_folder)
