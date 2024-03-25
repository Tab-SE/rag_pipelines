import os

from llama_index.llms.openai import OpenAI
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

from libs import clean

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
