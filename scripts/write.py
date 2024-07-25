import os, shutil

from libs import store
from libs.extract import metrics, content


def metric_insights(input):
    insights = metrics.bundles(input)
    if insights:
        print('Storing metric insights data to the file system...')
        delete_contents('data/insights')
        store.insights_corpus(insights)
    else:
        print('No new metric insights data received, skipping write step...')

def catalog(input):
    catalog = content.resources(input)
    if catalog:
        print('Storing catalog data to the file system...')
        delete_contents('data/catalog')
        store.catalog_corpus(catalog)
    else:
        print('No new catalog data received, skipping write step...')


def delete_contents(path):
    try:
        # Check if the directory exists
        if not os.path.exists(path):
            print(f"The directory {path} does not exist.")
            return

        # Iterate over all items in the directory
        for item in os.listdir(path):
            item_path = os.path.join(path, item)

            try:
                if os.path.isfile(item_path):
                    # If it's a file, remove it
                    os.unlink(item_path)
                    print(f"Deleted file: {item_path}")
                elif os.path.isdir(item_path):
                    # If it's a directory, remove it and its contents
                    shutil.rmtree(item_path)
                    print(f"Deleted directory: {item_path}")
            except Exception as e:
                print(f"Error deleting {item_path}: {e}")

        print(f"All contents of {path} have been deleted.")

    except Exception as e:
        print(f"An error occurred: {e}")
