from libs import store
from libs.extract import metrics, content

def metric_insights(input):
    print('Storing metric insights data to the file system...')
    insights = metrics.bundles(input)
    store.insights_corpus(insights)

def catalog(input):
    print('Storing catalog data to the file system...')
    catalog = content.resources(input)
    store.catalog_corpus(catalog)

