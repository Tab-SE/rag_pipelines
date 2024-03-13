import pandas as pd

from libs import session, subscriptions, bundles

def query(env_vars):
  DOMAIN, API, SITE, CLIENT_ID, SECRET, SECRET_ID, USER = env_vars.values()
  credentials = session.authenticate(env_vars)
  print('credentials', credentials)

  metrics = subscriptions.metrics(domain=DOMAIN, credentials=credentials)
  print('metrics', metrics)

  # insights = bundles(credentials, metrics)
  # print('insights', insights)

  insights = credentials

  return insights
