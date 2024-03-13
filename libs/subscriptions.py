import json
from jsonpath_ng import jsonpath, parse

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
    metrics = getMetrics(path=path, headers=headers, subscriptions=subscriptions)
    definitions = getMetricDefinitions(path=path, headers=headers, metrics=metrics)

    return metrics

def getSubscriptions(path, headers, user):
    endpoint =  path + f"/subscriptions?user_id={user}"
    response = httpGet(endpoint=endpoint, headers=headers)
    body = response['body']
    return body

def getMetrics(path, headers, subscriptions):
    # JSONPath expression
    expression = parse("$.subscriptions.[*].metric_id")
    # apply JSONPATH expression to JSON
    metrics_array = [match.value for match in expression.find(subscriptions)]
    # convert to string without brackets and spaces
    metric_ids = ','.join(metrics_array)
    # query parameter is a string of comma separated values with no spaces
    endpoint =  path + f"/metrics:batchGet?metric_ids={metric_ids}"

    response = httpGet(endpoint=endpoint, headers=headers)
    body = response['body']
    return body

def getMetricDefinitions(path, headers, metrics):
    definition_id = ""
    endpoint =  path + f"/definitions:batchGet?definition_ids={definition_id}"
    response = httpGet(endpoint=endpoint, headers=headers)
    body = json.loads(response.text)
    return body
