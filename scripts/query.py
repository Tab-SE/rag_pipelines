import pandas as pd

from libs import session, subscriptions, bundles

def query(env_vars):
  domain = env_vars['DOMAIN']
  credentials = session.authenticate(env_vars)
  print('credentials', credentials)

  metrics = subscriptions.metrics(domain=domain, credentials=credentials)
  print('metrics', metrics)

  # insights = bundles(credentials, metrics)
  # print('insights', insights)

  insights = credentials

  return insights
