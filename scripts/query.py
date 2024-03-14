from libs import bundles, session, subscriptions

def query(env_vars):
    domain = env_vars['DOMAIN']

    credentials = session.authenticate(env_vars)

    metrics = subscriptions.metrics(domain=domain, credentials=credentials)

    insights = bundles.insights(domain=domain, credentials=credentials, metrics=metrics)

    for key, value in insights.items():
        # print(f"Key: {key}, Value: {value}")
        pass

    return insights
