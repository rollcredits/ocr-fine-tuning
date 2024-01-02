import argparse
import os
import json
import random
import tiktoken
from constants import USE_TEST_SET, MAX_TOKENS

TIKTOKEN_ENCODING = "cl100k_base"


def read_file(folder, filename):
    with open(os.path.join(folder, filename), 'r') as f:
        return f.read()


def write_to_file_jsonl(filename, data):
    with open(filename, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')


def main(prompt_folder, label_folder):
    prompt_files = [f for f in os.listdir(prompt_folder) if f.endswith('.txt')]
    label_files = [f for f in os.listdir(label_folder) if f.endswith('.json')]

    training_data = []
    test_data = []

    encoding = tiktoken.get_encoding(TIKTOKEN_ENCODING)
    for prompt_file in prompt_files:
        prompt_content = read_file(prompt_folder, prompt_file)
        label_file = prompt_file.replace('.txt', '.json')
        if label_file in label_files:
            label_content = read_file(label_folder, label_file)
            encoded = encoding.encode(prompt_content + label_content)
            if len(encoded) > MAX_TOKENS:
                print(
                    f"Skipping {prompt_file} because it has {len(encoded)} tokens.")
                continue

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

    print("Wrote out data files! You can submit them through the OpenAI fine tuning UI: https://platform.openai.com/finetune")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Prepare data for GPT-3.5-turbo fine-tuning.')
    parser.add_argument(
        'label_folder', help='Folder containing label .json files')
    parser.add_argument(
        'prompt_folder', help='Folder containing prompt .txt files')
    args = parser.parse_args()
    main(args.prompt_folder, args.label_folder)
