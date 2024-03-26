from libs import extract, store, vectorize

def data(bundles):
    print('Extracting semantic features from JSON...')
    insights = extract.bundles(bundles)
    print('Storing data to file system...')
    insights_stored = store.insights_corpus(insights)
    print('Loading data for indexing...')
    monolith_loaded = vectorize.load_monolith()
    # corpus_loaded = vectorize.load_corpus()
    # insights_loaded = vectorize.load_insights()
    # headlessbi_loaded = False
    # writer_loaded = vectorize.load_writer()
    print('Data upserted to vector index successfully!')
    # return {
    #     'monolith_loaded':  monolith_loaded,
    #     'corpus_loaded':  corpus_loaded,
    #     'insights_loaded':  insights_loaded,
    #     'headlessbi_loaded':  headlessbi_loaded,
    #     'writer_loaded':  writer_loaded
    # }
