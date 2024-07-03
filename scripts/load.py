from libs import extract, store, vectorize

def data(bundles):
    semantics = get_semantics(bundles)
    corpus(semantics)
    vector_index()

def get_semantics(bundles):
    print('Extracting semantic features from external HTTP data sources...')
    insights = extract.bundles(bundles)
    return insights

def corpus(insights):
    print('Storing data to file system...')
    insights_stored = store.insights_corpus(insights)

def vector_index():
    print('Loading data for indexing...')
    monolith_loaded = vectorize.load_index(directory_path='data/', index_name='PINECONE_INDEX_NAME')
    # corpus_loaded = vectorize.load_index(directory_path='data/corpus/', index_name='CORPUS_INDEX')
    # insights_loaded = vectorize.load_index(directory_path='data/insights/', index_name='INSIGHTS_INDEX')
    # headlessbi_loaded = vectorize.load_index(directory_path='data/headlessbi/', index_name='HEADLESS_BI_INDEX')
    # catalog_loaded = vectorize.load_index(directory_path='data/catalog/', index_name='CATALOG_INDEX')
    # writer_loaded = vectorize.load_index(directory_path='data/literature/', index_name='WRITING_INDEX')

    print('Data upserted to vector index successfully!')
    return {
        'monolith_loaded':  monolith_loaded,
        # 'corpus_loaded':  corpus_loaded,
        # 'insights_loaded':  insights_loaded,
        # 'catalog_loaded': catalog_loaded,
        # 'writer_loaded':  writer_loaded
    }
