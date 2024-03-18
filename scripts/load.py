import os
import json

from llama_index.llms.openai import OpenAI
from llama_index.readers.json import JSONReader
from llama_index.core.indices.struct_store import JSONQueryEngine

from libs import extract

def data(bundles):
    print('Extracting semantic features from JSON...')
    insights = extract.bundles(bundles)
    print('Storing data to file system...')
    store_response(insights)
    print('Loading data for indexing...')
    # load_data()
    return insights

def store_response(insights):
    os.makedirs('data/insights', exist_ok=True)

    # loop through key-value pairs in insights dict
    for key, metric in insights.items():
        try:
            print('metadata', type(metric['metadata']))
            print('ban', type(metric['insights']['ban']))
            print('anchor', type(metric['insights']['anchor']))
            print('breakdown', type(metric['insights']['breakdown']))
            print('followup', type(metric['insights']['followup']))
            # create 'data/insights/{key}' folder if it doesn't exist
            folder_path = os.path.join('data', 'insights', key)
            os.makedirs(folder_path, exist_ok=True)
            # write metadata file to parent folder
            metadata_path = os.path.join(folder_path, f'{key}.txt')
            with open(metadata_path, 'w') as f:
                f.write(metric['metadata'])

             # create 'data/insights/{key}/insights' child folder if it doesn't exist
            insights_folder_path = os.path.join('data', 'insights', key, 'insights')
            os.makedirs(insights_folder_path, exist_ok=True)

            # write insight summary files
            metric_insights = metric['insights']
            for key in metric_insights['ban']:
                print(key)
                # ban_path = os.path.join(insights_folder_path, f'{key}.txt')
                # with open(ban_path, 'w') as f:
                #     f.write(insight)

        except Exception as e:
            print(f"An error occurred while processing key '{key}': {e}")
    return True


def load_data():
    # directory path
    directory_path = 'data/insights/'
    # loop through all files
    for filename in os.listdir(directory_path):
        # construct file path
        file_path = os.path.join(directory_path, filename)
        # initialize a LlamaIndex reader for JSON and load target file
        # https://llamahub.ai/l/readers/llama-index-readers-json?from=readers
        reader = JSONReader(levels_back=1, collapse_length=100, ensure_ascii=False)
        documents = reader.load_data(file_path)
        if filename == '0.json':
            print(documents[0].get_text())
    return True
