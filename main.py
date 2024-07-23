import asyncio
from dotenv import load_dotenv

from scripts import query, load

async def main():
    print('Initializing RAG Pipeline...')
    print('Querying Insights...')
    insights = await query.get()

    print('Processing Insights...')
    load.data({
        'bundles': insights,
        'options': { 'vector': True, 's3': True },
    })

    print('Terminating RAG Pipeline...')
    return


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
