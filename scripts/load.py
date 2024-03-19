import os

from llama_index.llms.openai import OpenAI
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone


from libs import extract, clean

def data(bundles):
    print('Extracting semantic features from JSON...')
    insights = extract.bundles(bundles)
    print('Storing data to file system...')
    is_stored = store_response(insights)
    print('Loading data for indexing...')
    load_insights()
    is_loaded = print('Data upserted to vector index successfully!')
    return insights

def store_response(insights):
    # create 'data/insights/' folder if it doesn't exist
    corpus_path = os.path.join('data', 'insights')
    os.makedirs(corpus_path, exist_ok=True)
    #
    corpus_metadata_path = os.path.join('data', 'insights', 'insights_metadata.md')
    # metadata file in root of insights/
    with open(corpus_metadata_path, 'w') as f:
        f.write(insights['corpus_metadata'])

    # loop through key-value pairs in insights dict
    for key, metric in insights['corpus'].items():
        try:
            folder_path = os.path.join('data', 'insights', key)
            os.makedirs(folder_path, exist_ok=True)
            # write metadata file to parent folder
            metadata_path = os.path.join(folder_path, f'{key}.md')
            with open(metadata_path, 'w') as f:
                f.write(metric['metadata'])

             # create 'data/insights/{key}/insights' child folder if it doesn't exist
            insights_folder_path = os.path.join('data', 'insights', key, 'insights')
            os.makedirs(insights_folder_path, exist_ok=True)

            # write insight summary files
            metric_insights = metric['insights']
            for index, insight in enumerate(metric_insights['ban']):
                ban_path = os.path.join(insights_folder_path, f'ban_{index}.md')
                with open(ban_path, 'w') as f:
                    f.write(insight)

            for index, insight in enumerate(metric_insights['anchor']):
                anchor_path = os.path.join(insights_folder_path, f'anchor_{index}.md')
                with open(anchor_path, 'w') as f:
                    f.write(insight)

            for index, insight in enumerate(metric_insights['breakdown']):
                breakdown_path = os.path.join(insights_folder_path, f'breakdown_{index}.md')
                with open(breakdown_path, 'w') as f:
                    f.write(insight)

            for index, insight in enumerate(metric_insights['followup']):
                followup_path = os.path.join(insights_folder_path, f'followup_{index}.md')
                with open(followup_path, 'w') as f:
                    f.write(insight)

        except Exception as e:
            print(f"An error occurred while processing key '{key}': {e}")
    return True


def load_insights():
    # directory path
    directory_path = 'data/insights/'
    # Create an instance of SimpleDirectoryReader
    reader = SimpleDirectoryReader(
        input_dir=directory_path,
        recursive=True
    )
    # Load the documents from the directory
    documents = reader.load_data()
    # remove emaining \n characters and broken, hyphenated words
    cleaned_docs = []
    for d in documents:
        cleaned_text = clean.clean_up_text(d.text)
        d.text = cleaned_text
        cleaned_docs.append(d)

    pinecone_api = os.environ['PINECONE_API_KEY']
    pinecone_environment = os.environ['PINECONE_ENVIRONMENT']
    pinecone_index = os.environ['PINECONE_INDEX_NAME']

    # initialize pinecone client
    pc = Pinecone(api_key=pinecone_api, environment=pinecone_environment)
    # client instance targets declared index
    index = pc.Index(pinecone_index)

    # construct vector store
    vector_store = PineconeVectorStore(pinecone_index=index)
    # specifies location, environment and index for storage
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    # build index
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )

    return True
