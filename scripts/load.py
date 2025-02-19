import os
from libs import bucket, vectorize

def data(config):
    if config.get('vector') == True:
        vector_index()
    if config.get('s3') == True:
        push_s3()

def vector_index():
    print('Loading data for indexing...')
    monolith_loaded = vectorize.langchain_vectorize(directory_path='data/', index_name=os.environ['PINECONE_INDEX_NAME'], chunk_size=1024, chunk_overlap=20)
    metrics_loaded = vectorize.langchain_vectorize(directory_path='data/analytics/metrics/', index_name=os.environ['METRICS_INDEX'], chunk_size=1024, chunk_overlap=20)
    workbooks_loaded = vectorize.langchain_vectorize(directory_path='data/analytics/workbooks/', index_name=os.environ['WORKBOOKS_INDEX'], chunk_size=1024, chunk_overlap=20)
    datasources_loaded = vectorize.langchain_vectorize(directory_path='data/analytics/datasources/', index_name=os.environ['DATASOURCES_INDEX'], chunk_size=1024, chunk_overlap=20)
    literature_loaded = vectorize.langchain_vectorize(directory_path='data/literature/', index_name=os.environ['LITERATURE_INDEX'], chunk_size=1024, chunk_overlap=20)

    print('Data upserted to vector index successfully!')
    return {
        'monolith_loaded':  monolith_loaded,
        'metrics_loaded':  metrics_loaded,
        'workbooks_loaded': workbooks_loaded,
        'datasources_loaded':  datasources_loaded,
        'literature_loaded':  literature_loaded
    }

def push_s3():
    print('Pushing data to S3 bucket...')
    bucket.load_bucket()
