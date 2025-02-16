from libs import bucket, vectorize

def data(config):
    if config.get('vector') == True:
        vector_index()
    if config.get('s3') == True:
        push_s3()

def vector_index():
    print('Loading data for indexing...')
    monolith_loaded = vectorize.load_index(directory_path='data/', index_name='PINECONE_INDEX_NAME')
    metrics_loaded = vectorize.load_index(directory_path='data/analytics/metrics/', index_name='METRICS_INDEX')
    workbooks_loaded = vectorize.load_index(directory_path='data/analytics/workbooks/', index_name='WORKBOOKS_INDEX')
    datasources_loaded = vectorize.load_index(directory_path='data/analytics/datasources/', index_name='DATASOURCES_INDEX')
    literature_loaded = vectorize.load_index(directory_path='data/literature/', index_name='LITERATURE_INDEX')

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
