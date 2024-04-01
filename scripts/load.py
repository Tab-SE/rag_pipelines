from libs import extract, store, vectorize

def data(bundles):
    semantics = get_semantics(bundles)
    corpus(semantics)
    vector_index()

def get_semantics(bundles):
    print('Extracting semantic features from JSON...')
    insights = extract.bundles(bundles)
    return insights

def corpus(insights):
    print('Storing data to file system...')
    insights_stored = store.insights_corpus(insights)

def vector_index():
    print('Loading data for indexing...')
    monolith_loaded = vectorize.load_monolith()
    # corpus_loaded = vectorize.load_corpus()
    # insights_loaded = vectorize.load_insights()
    # headlessbi_loaded = vectorize.load_headlessbi()
    # writer_loaded = vectorize.load_writer()
    print('Data upserted to vector index successfully!')
    return {
        'monolith_loaded':  monolith_loaded,
        'corpus_loaded':  False,
        'insights_loaded':  False,
        'headlessbi_loaded':  False,
        'writer_loaded':  False
    }
