async def main():
    print('Initializing RAG Pipeline...')
    print('Querying Insights...')
    insights = await query.get({
        'DOMAIN': DOMAIN,
        'API': API,
        'SITE': SITE,
        'CLIENT_ID': CLIENT_ID,
        'SECRET': SECRET,
        'SECRET_ID': SECRET_ID,
        'USER': USER
    })

    print('Processing Insights...')
    load.data(insights, { 'vector': True, 's3': True })

    print('Terminating RAG Pipeline...')
    return


if __name__ == "__main__":
    import os

    import asyncio
    from dotenv import load_dotenv

    from scripts import query, load

    load_dotenv()
    env_vars = os.environ
    # Tableau Pulse env vars
    DOMAIN = env_vars['TABLEAU_DOMAIN']
    API = env_vars['TABLEAU_API']
    SITE = env_vars['TABLEAU_SITE']
    CLIENT_ID = env_vars['TABLEAU_JWT_CLIENT_ID']
    SECRET = env_vars['TABLEAU_REST_JWT_SECRET']
    SECRET_ID = env_vars['TABLEAU_REST_JWT_SECRET_ID']
    USER = env_vars['TABLEAU_USER']
    # Vectorization env vars
    OPENAI_API_KEY = env_vars['OPENAI_API_KEY']
    MODEL = env_vars['MODEL']
    PINECONE_API_KEY = env_vars['PINECONE_API_KEY']
    PINECONE_ENVIRONMENT = env_vars['PINECONE_ENVIRONMENT']
    PINECONE_INDEX_NAME = env_vars['PINECONE_INDEX_NAME']

    asyncio.run(main())
