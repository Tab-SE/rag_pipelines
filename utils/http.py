import requests
import json

def httpGet(endpoint, headers):
  response = requests.request("GET", endpoint, headers=headers)
  return response

def httpPost(endpoint, headers, payload):
  formattedPayload = json.dumps(payload)
  response = requests.request("POST", endpoint, headers=headers, data=formattedPayload)
  return response

