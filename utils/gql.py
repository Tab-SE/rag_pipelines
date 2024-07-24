import os, json, aiohttp

async def query(query, token):
    domain = os.environ['TABLEAU_DOMAIN']
    url = f"{domain}/api/metadata/graphql"

    payload = json.dumps({
        "query": query,
        "variables": {}
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Tableau-Auth': token
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as response:
            return await response.text()
