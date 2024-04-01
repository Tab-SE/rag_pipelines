from datetime import datetime

from tzlocal import get_localzone

from utils import http

async def insights(domain, credentials, metrics):
    insights_bundles = {}
    # REST API authentication token
    token = credentials['credentials']['token']
    # generates full set of insights from Pulse
    endpoint = f"{domain}/api/-/pulse/insights/detail"
    # carries authentication token and sets response format
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-Tableau-Auth': token
    }

    # provide common time definitions for all insights requests
    current_datetime = datetime.now()
    # formatted as "YYYY-MM-DD HH:mm:ss"
    formatted_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # Get the local timezone object
    local_timezone = get_localzone()
    # Get the IANA timezone name
    timezone_name = current_datetime.astimezone(local_timezone).tzinfo.zone
    time_options = {
        'formatted_time': formatted_time,
        'timezone_name': timezone_name
    }

    for key, metric in metrics.items():
        insights = await queryInsights(endpoint=endpoint, headers=headers, metric=metric, time_options=time_options)
        insights_bundles[key] = {
            "metric": metric,
            "insights": insights,
            "time_options": time_options,
        }

    return insights_bundles

async def queryInsights(endpoint, headers, metric, time_options):
    # request body needed to generate insights
    payload = {
        "bundle_request": {
            "version": "1",
            "options": {
                "output_format": "OUTPUT_FORMAT_TEXT",
                "now": time_options['formatted_time'],
                "time_zone": time_options['timezone_name']
            },
            "input": {
                "metadata": {
                    "name": metric['name'],
                    "metric_id": metric['id'],
                    "definition_id": metric['definition_id']
                },
                "metric": {
                    "definition": metric['definition'],
                    "metric_specification": metric['specification'],
                    "extension_options": metric['extension_options'],
                    "representation_options": metric['representation_options'],
                    "insights_options": metric['insights_options']
                }
            }
        }
    }
    # generate /detail insights from Tableau Pulse
    # https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_pulse.htm#PulseInsightsService_GenerateInsightBundleDetail
    response = await http.post(endpoint=endpoint, headers=headers, payload=payload)
    bundles = response['body']
    return bundles
