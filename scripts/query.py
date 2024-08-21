import os
from libs import bundles, session, subscriptions, metadata

# returns a session with metadata about the user and site
async def get_user_session():
    credentials = await session.authenticate()
    # high level user and site metadata for the RAG system
    user_session = {
        'credentials': credentials,
        'user_data': '',
        'site_data': '',
        'projects': ''
    }

    return user_session

# returns data on user metrics and their Pulse insights
async def get_insights(credentials):
    metrics = await subscriptions.metrics(credentials)
    print(f'{len(metrics)} Metrics received')

    insights = await bundles.insights(credentials=credentials, metrics=metrics)

    print(f'{len(insights)} Insight bundles received')
    return insights

# returns metadata on Tableau files relevant to users
async def get_catalog(credentials):
    token = credentials['credentials']['token']
    project_name = os.environ['CATALOG_PROJECT']
    workbooks = await metadata.query_metadata({
        'token': token,
        'project_name': project_name,
        'max_retries': 6,
        'retry_delay': 1,
        'asset': 'workbooks'
    })

    catalog = {
        'workbooks': workbooks
    }

    print(f'Full data catalog metadata received')
    return catalog
