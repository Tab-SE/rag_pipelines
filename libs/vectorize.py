import os

from llama_index.core import Document, SimpleDirectoryReader, VectorStoreIndex, StorageContext, Settings
from llama_index.embeddings.langchain import LangchainEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore

from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import Pinecone as LangchainPinecone

from pinecone import Pinecone as PineconeClient, ServerlessSpec

from libs import clean


def load_index(directory_path, index_name):
    try:
        documents = gather_documents(directory_path)
        # construct pinecone client for target index
        index = initialize_index(index_name)
        # build vector store, index and upsert to Pinecone
        vectorize(index=index, documents=documents, chunk_size=2048, chunk_overlap=50)

        return True
    except Exception as e:
        print(f"Error loading data from {directory_path}:", e)
        return False

def gather_documents(path):
    print(f'Gathering documents from {path}...')
    # Create an instance of SimpleDirectoryReader
    reader = SimpleDirectoryReader(
        input_dir=path,
        recursive=True,
        exclude_hidden=True,
    )
    # Load the documents from the directory
    documents = reader.load_data()
    # remove emaining \n characters and broken, hyphenated words
    cleaned_docs = clean_docs(documents)
    return cleaned_docs

def clean_docs(documents):
    # remove remaining \n characters and broken, hyphenated words
    cleaned_docs = []
    for d in documents:
        cleaned_text = clean.clean_up_text(d.text)
        # Create a new Document object with the cleaned text
        cleaned_doc = Document(text=cleaned_text, metadata=d.metadata)
        cleaned_docs.append(cleaned_doc)
    return cleaned_docs

def initialize_index(pinecone_index):
    pinecone_api = os.environ['PINECONE_API_KEY']
    pinecone_environment = os.environ['PINECONE_ENVIRONMENT']
    index_name = os.environ[pinecone_index]
    # initialize pinecone client
    pc = PineconeClient(api_key=pinecone_api)

    # check if index exists
    existing_indexes = pc.list_indexes()
    if existing_indexes:
        for index in existing_indexes:
            if index.get('name') == index_name:
                # Remove index to be replaced with updated data
                pc.delete_index(index_name)
                print(f"Previous vector state found! Deleting stale index: {index_name}")
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

def vectorize(index, documents, chunk_size=1024, chunk_overlap=20):
    lc_embed_model = OpenAIEmbeddings(
        model=os.environ['EMBEDDING_MODEL']
    )

    embed_model = LangchainEmbedding(lc_embed_model)

    # configure global settings
    Settings.embed_model = embed_model
    Settings.chunk_size = chunk_size
    Settings.chunk_overlap = chunk_overlap

    # construct vector store
    vector_store = PineconeVectorStore(
        pinecone_index=index,
        api_key=os.environ['PINECONE_API_KEY'],
        environment=os.environ['PINECONE_ENVIRONMENT']
    )

    # specifies location, environment and index for storage
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    # build index
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, show_progress=True,
    )


def langchain_vectorize(directory_path, index_name, chunk_size=1024, chunk_overlap=20):
    # Initialize Pinecone
    pc = PineconeClient(api_key=os.environ['PINECONE_API_KEY'])

    # Ensure the index exists
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric='cosine',
            spec=ServerlessSpec(
                cloud="aws",
                region=os.environ['PINECONE_ENVIRONMENT']
            )
        )

    # Load documents from the directory
    loader = DirectoryLoader(directory_path, glob="**/*")
    documents = loader.load()

    # Split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    texts = text_splitter.split_documents(documents)

    # Initialize the OpenAI embeddings
    embeddings = OpenAIEmbeddings(
        model=os.environ['EMBEDDING_MODEL']
    )

    # Create and populate the Pinecone index
    vectorstore = LangchainPinecone.from_documents(
        texts,
        embeddings,
        index_name=index_name
    )

    return vectorstore
