import requests
import jwt
import json
from datetime import datetime, timedelta, timezone
from uuid import uuid4

def authenticate(params):
    DOMAIN, API, SITE, CLIENT_ID, SECRET, SECRET_ID, USER = params.values()
    # Encode the payload and secret key to generate the JWT
    token = jwt.encode(
      {
        "iss": CLIENT_ID,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
        "jti": str(uuid4()),
        "aud": "tableau",
        "sub": USER,
        "scp": [
          "tableau:datasources:read",
          "tableau:workbooks:read",
          "tableau:projects:read",
          "tableau:insight_definitions_metrics:read", 
          "tableau:insight_metrics:read",
          "tableau:metric_subscriptions:read",
        ]
      },
        SECRET,
        algorithm = "HS256",
        headers = {
        'kid': SECRET_ID,
        'iss': CLIENT_ID
      }
    )

    # authentication endpoint + request headers & payload
    url = f"{DOMAIN}/api/{API}/auth/signin" 

    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    
    payload = json.dumps({
      "credentials": {
        "jwt": token,
        "site": {
          "contentUrl": SITE,
        }
      }
    })

    response = requests.request("POST", url, headers=headers, data=payload)
    print('body', json.dumps(response.text, indent=4))
    return response
