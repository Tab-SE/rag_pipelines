from libs import bundles, session, subscriptions

def query(env_vars):
    domain = env_vars['DOMAIN']

    credentials = session.authenticate(env_vars)
    print(f'Tableau authentication successful: {credentials['credentials']['token']}')

    metrics = subscriptions.metrics(domain=domain, credentials=credentials)
    print(f'{len(metrics)} Metrics received!')

    insights = bundles.insights(domain=domain, credentials=credentials, metrics=metrics)
    print(f'{len(insights)} Insight bundles received!')

    for key, value in insights.items():
        # print(f"Key: {key}, Value: {value}")
        pass

    return insights
