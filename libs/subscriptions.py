import json

from utils.http import httpGet

def metrics(domain, credentials):
    token = credentials['credentials']['token']
    user = credentials['credentials']['user']['id']
    endpoint = f"{domain}/api/-/pulse/subscriptions?user_id={user}" 

    print('endpoint', endpoint)

    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-Tableau-Auth': token
    }

    response = httpGet(endpoint=endpoint, headers=headers)
    body = json.loads(response.text)
    
    return body
