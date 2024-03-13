import pandas as pd

from scripts.libs import session, subscriptions, bundles

def query(params):
  credentials = session.authenticate(params)
  print('credentials', credentials)

  # metrics = subscriptions(credentials)
  # print('metrics', metrics)

  # insights = bundles(credentials, metrics)
  # print('insights', insights)

  insights = credentials

  return insights
