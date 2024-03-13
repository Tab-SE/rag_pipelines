import requests
import json

def httpGet(endpoint, headers):
  response = requests.request("GET", endpoint, headers=headers)

  responseHeaders = dict(response.headers)
  responseBody = response.json()

  responseObject = {
    "headers": responseHeaders,
    "body": responseBody
  }
  return responseObject

def httpPost(endpoint, headers, payload):
  formattedPayload = json.dumps(payload)
  response = requests.request("POST", endpoint, headers=headers, data=formattedPayload)

  responseHeaders = dict(response.headers)
  responseBody = response.json()

  responseObject = {
    "headers": responseHeaders,
    "body": responseBody
  }

  return responseObject

