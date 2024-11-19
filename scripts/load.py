from libs import bucket, vectorize

def data(config):
    if config.get('vector') == True:
        vector_index()
    if config.get('s3') == True:
        push_s3()

def vector_index():
    print('Loading data for indexing...')
    monolith_loaded = vectorize.load_index(directory_path='data/', index_name='PINECONE_INDEX_NAME')
    # agent_loaded = vectorize.load_index(directory_path='data/agent/', index_name='AGENT_INDEX')
    # metrics_loaded = vectorize.load_index(directory_path='data/analytics/insights/', index_name='METRICS_INDEX')
    # catalog_loaded = vectorize.load_index(directory_path='data/analytics/catalog/', index_name='DATA_CATALOG_INDEX')
    # literature_loaded = vectorize.load_index(directory_path='data/literature/', index_name='LITERATURE_INDEX')

    print('Data upserted to vector index successfully!')
    return {
        'monolith_loaded':  monolith_loaded,
        # 'agent_loaded':  agent_loaded,
        # 'metrics_loaded':  metrics_loaded,
        # 'catalog_loaded': catalog_loaded,
        # 'literature_loaded':  literature_loaded
    }

def push_s3():
    print('Pushing data to S3 bucket...')
    bucket.load_bucket()
