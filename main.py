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
    load.data({
        'bundles': insights, 
        'options': { 'vector': True, 's3': True },
        'env_vars': {
            'AWS_ACCESS_KEY_ID': AWS_ACCESS_KEY_ID,
            'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY,
            'AWS_DEFAULT_REGION': AWS_DEFAULT_REGION,
        }
    })

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
    # AWS S3 env vars
    AWS_ACCESS_KEY_ID = env_vars['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = env_vars['AWS_SECRET_ACCESS_KEY']
    AWS_DEFAULT_REGION = env_vars['AWS_DEFAULT_REGION']

    asyncio.run(main())
