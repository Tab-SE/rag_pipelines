import os

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from libs import clean

def load_index(directory_path, index_name):
    try:
        documents = gather_documents(directory_path)
        # construct pinecone client for target index
        index = initialize_index(index_name)
        # build vector store, index and upsert to Pinecone
        vectorize(index=index, documents=documents)
        return True
    except Exception as e:
        print(f"Error loading data from {directory_path}:", e)
        return False

def gather_documents(path):
    print(f'Gathering documents from {path}')
    exclude = ''
    # monolith must exclude literature data used to generate the corpus
    if path == 'data/':
        exclude='data/literature/'
    # Create an instance of SimpleDirectoryReader
    reader = SimpleDirectoryReader(
        input_dir=path,
        recursive=True,
        exclude_hidden=True
    )
    # Load the documents from the directory
    documents = reader.load_data()
    # remove emaining \n characters and broken, hyphenated words
    cleaned_docs = clean_docs(documents)
    return cleaned_docs

def clean_docs(documents):
    # remove emaining \n characters and broken, hyphenated words
    cleaned_docs = []
    for d in documents:
        cleaned_text = clean.clean_up_text(d.text)
        d.text = cleaned_text
        cleaned_docs.append(d)
    return cleaned_docs

def initialize_index(pinecone_index):
    pinecone_api = os.environ['PINECONE_API_KEY']
    pinecone_environment = os.environ['PINECONE_ENVIRONMENT']
    index_name = os.environ[pinecone_index]
    # initialize pinecone client
    pc = Pinecone(api_key=pinecone_api, environment=pinecone_environment)

    # check if index exists
    existing_indexes = pc.list_indexes()
    if existing_indexes:
        for index in existing_indexes:
            if index.get('name') == index_name:
                # Remove index to be replaced with updated data
                pc.delete_index(index_name)
                print(f"Previous vector state found! Deleting state data at: {index_name}")
    # create a new index to store updated data
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-west-2"
        )
    )
    # client instance targets newly created index
    index = pc.Index(index_name)
    return index

def vectorize(index, documents):
    # construct vector store
    vector_store = PineconeVectorStore(pinecone_index=index)
    # specifies location, environment and index for storage
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    # build index
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )
