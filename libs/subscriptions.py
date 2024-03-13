import json

from utils.http import httpGet

def metrics(domain, credentials):
    token = credentials['credentials']['token']
    user = credentials['credentials']['user']['id']

    # shared by all Pulse endpoints
    path = f"{domain}/api/-/pulse" 
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-Tableau-Auth': token
    }

    subscriptions = getSubscriptions(path=path, headers=headers, user=user)
    
    return subscriptions

def getSubscriptions(path, headers, user):
    endpoint =  path + f"/subscriptions?user_id={user}"
    response = httpGet(endpoint=endpoint, headers=headers)
    body = json.loads(response.text)
    return body
