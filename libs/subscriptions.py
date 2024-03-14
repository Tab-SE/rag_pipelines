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

    return definitions

def getSubscriptions(path, headers, user):
    endpoint =  path + f"/subscriptions?user_id={user}"
    response = httpGet(endpoint=endpoint, headers=headers)
    body = response['body']
    return body

def getMetrics(path, headers, subscriptions):
    # JSONPath expressions
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
    # JSONPath expression for query parameter values
    definition_ids_expression = parse("$.metrics.[*].definition_id")
    # apply JSONPATH expression to JSON
    definition_ids_array = [match.value for match in definition_ids_expression.find(metrics)]
    # convert to string without brackets and spaces
    definition_ids = ','.join(definition_ids_array)

    # use as query parameter values
    endpoint =  path + f"/definitions:batchGet?definition_ids={definition_ids}"
    response = httpGet(endpoint=endpoint, headers=headers)
    body = response['body']

    # JSONPath expressions to extract data for requesting Pulse insights and semantic embedding
    metric_ids_expression = parse("$.metrics.[*].id")
    specifications_expression = parse("$.metrics.[*].specification")
    names_expression = parse("$.definitions.[*].metadata.name")
    descriptions_expression = parse("$.definitions.[*].metadata.description")
    definitions_expression = parse("$.definitions.[*].specification")
    extentions_expression = parse("$.definitions.[*].extension_options")
    representations_expression = parse("$.definitions.[*].representation_options")
    insights_options_expression = parse("$.definitions.[*].insights_options")

    # apply JSONPATH expression to JSON
    metric_ids_array = [match.value for match in metric_ids_expression.find(metrics)]
    specifications_array = [match.value for match in specifications_expression.find(metrics)]
    names_array = [match.value for match in names_expression.find(body)]
    descriptions_array = [match.value for match in descriptions_expression.find(body)]
    definitions_array = [match.value for match in definitions_expression.find(body)]
    extentions_array = [match.value for match in extentions_expression.find(body)]
    representations_array = [match.value for match in representations_expression.find(body)]
    insights_options_array = [match.value for match in insights_options_expression.find(body)]

    definitions = {}

    # iterate through arrays and create leaves in the return dictionary
    # conditionals ensure that if index is out of bounds, the value will be None
    # preventing index out-of-range errors.
    for index, name in enumerate(metric_ids_array):
        definitions[index] = {
            'id': name,
            'name': names_array[index] if index < len(names_array) else None,
            'description': descriptions_array[index] if index < len(descriptions_array) else None,
            'specification': specifications_array[index] if index < len(specifications_array) else None,
            'definition_id': definition_ids_array[index] if index < len(definition_ids_array) else None,
            'definition': definitions_array[index] if index < len(definitions_array) else None,
            'extension_options': extentions_array[index] if index < len(extentions_array) else None,
            'representation_options': representations_array[index] if index < len(representations_array) else None,
            'insights_options': insights_options_array[index] if index < len(insights_options_array) else None,
        }

    return definitions


