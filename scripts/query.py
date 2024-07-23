import os

from libs import bundles, session, subscriptions

async def get():
    domain = os.environ['TABLEAU_DOMAIN']

    credentials = await session.authenticate()
    print(f'Tableau authentication successful: {credentials['credentials']['token']}')

    metrics = await subscriptions.metrics(domain=domain, credentials=credentials)
    print(f'{len(metrics)} Metrics received')

    insights = await bundles.insights(domain=domain, credentials=credentials, metrics=metrics)
    print(f'{len(insights)} Insight bundles received')

    return insights
