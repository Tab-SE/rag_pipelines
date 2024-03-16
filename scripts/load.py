import os
import json
from llama_index.llms.openai import OpenAI
from llama_index.readers.json import JSONReader
from llama_index.core.indices.struct_store import JSONQueryEngine

def data(insights):
    store_response(insights)

    read_data()

    return insights

def store_response(insights):
    # create 'data/insights' folder if it doesn't exist
    os.makedirs('data/insights', exist_ok=True)

    # loop through key-value pairs in insights dict
    for key, value in insights.items():
        try:
            # create file path with key as file name
            file_path = os.path.join('data', 'insights', f'{key}.json')

            # Write JSON to file
            with open(file_path, 'w') as f:
                json.dump(value, f)
        except Exception as e:
            print(f"An error occurred while processing key '{key}': {e}")

    return insights


def read_data():
    # https://llamahub.ai/l/readers/llama-index-readers-json?from=readers
    # reader = JSONReader(levels_back=1, collapse_length=100, ensure_ascii=False)
    # documents = reader.load_data('path_to_your_json_file.json')
    pass
