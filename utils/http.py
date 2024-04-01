import requests
import aiohttp
import asyncio
import json

# def get(endpoint, headers):
# 	response = requests.request("GET", endpoint, headers=headers)

# 	responseHeaders = dict(response.headers)
# 	responseBody = response.json()

# 	responseObject = {
# 		"headers": responseHeaders,
# 		"body": responseBody
# 	}
# 	return responseObject

async def get(endpoint, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint, headers=headers) as response:
            responseHeaders = dict(response.headers)
            responseBody = await response.json()

            responseObject = {
                "headers": responseHeaders,
                "body": responseBody
            }
            return responseObject

def post(endpoint, headers, payload):
	formattedPayload = json.dumps(payload)
	response = requests.request("POST", endpoint, headers=headers, data=formattedPayload)

	responseHeaders = dict(response.headers)
	responseBody = response.json()

	responseObject = {
		"headers": responseHeaders,
		"body": responseBody
	}

	return responseObject

