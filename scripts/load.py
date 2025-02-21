import os
from libs import bucket, vectorize

def data(config):
    if config.get('vector') == True:
        vector_index()
    if config.get('s3') == True:
        push_s3()

def vector_index():
    print('Loading data for indexing...')
    # monolith_loaded = vectorize.load_index(directory_path='data/', index_name=os.environ['PINECONE_INDEX_NAME'])
    metrics_loaded = vectorize.load_index(directory_path='data/analytics/metrics/', index_name=os.environ['METRICS_INDEX'])
    workbooks_loaded = vectorize.load_index(directory_path='data/analytics/workbooks/', index_name=os.environ['WORKBOOKS_INDEX'])
    datasources_loaded = vectorize.load_index(directory_path='data/analytics/datasources/', index_name=os.environ['DATASOURCES_INDEX'])
    # literature_loaded = vectorize.load_index(directory_path='data/literature/', index_name=os.environ['LITERATURE_INDEX'])

    # monolith_loaded = vectorize.langchain_vectorize(directory_path='data/', index_name=os.environ['PINECONE_INDEX_NAME'], chunk_size=2000, chunk_overlap=200)
    # metrics_loaded = vectorize.langchain_vectorize(directory_path='data/analytics/metrics/', index_name=os.environ['METRICS_INDEX'], chunk_size=2000, chunk_overlap=200)
    # workbooks_loaded = vectorize.langchain_vectorize(directory_path='data/analytics/workbooks/', index_name=os.environ['WORKBOOKS_INDEX'], chunk_size=2000, chunk_overlap=200)
    # datasources_loaded = vectorize.langchain_vectorize(directory_path='data/analytics/datasources/', index_name=os.environ['DATASOURCES_INDEX'], chunk_size=2000, chunk_overlap=200)
    # literature_loaded = vectorize.langchain_vectorize(directory_path='data/literature/', index_name=os.environ['LITERATURE_INDEX'], chunk_size=2000, chunk_overlap=200)

    print('Data upserted to vector index successfully!')
    return {
        # 'monolith_loaded':  monolith_loaded,
        'metrics_loaded':  metrics_loaded,
        'workbooks_loaded': workbooks_loaded,
        'datasources_loaded':  datasources_loaded,
        # 'literature_loaded':  literature_loaded
    }

def push_s3():
    print('Pushing data to S3 bucket...')
    bucket.load_bucket()
