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
    workbooks = await metadata.query_workbooks(token)
    views = await metadata.query_views(token)
    datasources = await metadata.query_datasources(token)

    catalog = {
        'workbooks': workbooks,
        'views': views,
        'datasources': datasources
    }

    print(f'Full data catalog metadata received')
    return catalog
