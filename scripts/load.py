from libs import extract, store, vectorize

def data(bundles):
    print('Extracting semantic features from JSON...')
    insights = extract.bundles(bundles)
    print('Storing data to file system...')
    insights_stored = store.insights_corpus(insights)
    print('Loading data for indexing...')
    is_loaded = vectorize.load_insights()
    print('Data upserted to vector index successfully!')
    return insights
