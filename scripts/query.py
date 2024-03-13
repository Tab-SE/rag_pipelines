import pandas as pd

from libs import session, subscriptions, bundles

def query(params):
  credentials = session.authenticate(params)
  print('credentials', credentials)

  metrics = subscriptions.metrics(credentials)
  print('metrics', metrics)

  # insights = bundles(credentials, metrics)
  # print('insights', insights)

  insights = credentials

  return insights
