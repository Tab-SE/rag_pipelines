import pandas as pd

from libs import bundles, session, subscriptions

def query(env_vars):
    domain = env_vars['DOMAIN']
    credentials = session.authenticate(env_vars)
    # print('credentials', credentials)

    metrics = subscriptions.metrics(domain=domain, credentials=credentials)
    # print('metrics', metrics)

    insights = bundles.insights(domain=domain, credentials=credentials, metrics=metrics)
    # print('insights', insights)

    for key, value in insights.items():
        print(f"Key: {key}, Value: {value}")
        pass

    return insights

