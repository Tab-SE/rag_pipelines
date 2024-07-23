import asyncio
from dotenv import load_dotenv

from scripts import query, load

async def main():
    print('Initializing RAG Pipeline...')
    # 1. Obtain data to update the corpus of the RAG system
    print('Securing user session with Tableau site...')
    user_session = await query.get_user_session()
    credentials = user_session['credentials']

    print('Querying for Pulse Metric Insights...')
    insights = await query.get_insights(credentials)

    print('Querying the Data Catalog...')
    catalog = await query.get_catalog(credentials)
    # 2. Write natural language summaries
    print('Processing remote data...')

    print('Natural language summaries written to file system...')
    # 3. Load corpus to vector store and s3 bucket
    load.data({
        'bundles': insights,
        'catalog': catalog,
        'options': { 'vector': True, 's3': True },
    })
    print('Data uploaded to targets...')

    print('Terminating RAG Pipeline...')
    return

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
