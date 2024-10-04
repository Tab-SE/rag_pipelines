import asyncio, json
from utils import gql

async def query_metadata(params):
    token = params.get('token')
    project_name = params.get('project_name')
    max_retries = params.get('max_retries', 6)
    retry_delay = params.get('retry_delay', 3)
    asset = params['asset']

    if asset == 'workbooks':
        query = project_workbooks_query(project_name)
    elif asset == 'dashboards':
        query = project_dashboards_query(project_name)
    elif asset == 'datasources':
        pass

    for attempt in range(max_retries):
        try:
            workbooks = await gql.query(query=query, token=token)
            workbooks_json = json.loads(workbooks)

            if "errors" in workbooks_json:
                error_message = workbooks_json["errors"][0]["message"]
                if "Execution canceled because timeout of 30000 millis was reached" in error_message:
                    print(f"Attempt {attempt + 1}: Query timed out. Retrying in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                    continue
                elif "One or more of the attributes used in your filter contain sensitive data" in error_message:
                    print(f'Workbooks metadata received')
                    print("Warning: Results filtered due to permissions.")
                    return workbooks_json
                else:
                    print(f"Unhandled error: {error_message}")
                    break
            else:
                print(f'Workbooks metadata received')
                return workbooks_json

        except Exception as e:
            print(f"Attempt {attempt + 1}: An error occurred: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                print("Max retries reached. Unable to fetch workbooks metadata.")
                raise

    return None

def project_workbooks_query(project_name):
    return f"""
query Workbooks {{
    workbooks(filter: {{ projectName: "{project_name}" }}) {{
        name
        description
        createdAt
        projectName
        createdAt
        updatedAt
        tags {{
            name
        }}
        dashboards {{
            name
            path
            createdAt
            updatedAt
            tags {{
                name
            }}
        }}
        sheets {{
            name
            path
            createdAt
            updatedAt
            tags {{
                name
            }}
        }}
        upstreamDatasources {{
            name
            isCertified
            description
            projectName
            hasExtracts
            extractLastRefreshTime
            extractLastIncrementalUpdateTime
            extractLastUpdateTime
            fields(filter: {{ isHidden: false }}) {{
                name
                description
                folderName
            }}
            datasourceFilters {{
                field {{
                    id
                }}
            }}
            parameters {{
                name
            }}
            hasActiveWarning
            labels {{
                value
                category
                message
            }}
            downstreamMetricDefinitions {{
                name
                id
                luid
                fields {{
                    name
                    description
                }}
            }}
        }}
    }}
}}"""

def project_dashboards_query(project_name):
    return f"""
query Workbooks {{
    workbooks(filter: {{ projectName: "{project_name}" }}) {{
        name
        description
        createdAt
        projectName
        createdAt
        updatedAt
        tags {{
            name
        }}
        dashboards {{
            name
            path
            createdAt
            updatedAt
            tags {{
                name
            }}
        }}
        sheets {{
            name
            path
            createdAt
            updatedAt
            tags {{
                name
            }}
        }}
        upstreamDatasources {{
            name
            isCertified
            description
            projectName
            hasExtracts
            extractLastRefreshTime
            extractLastIncrementalUpdateTime
            extractLastUpdateTime
            fields(filter: {{ isHidden: false }}) {{
                name
                description
                folderName
            }}
            datasourceFilters {{
                field {{
                    id
                }}
            }}
            parameters {{
                name
            }}
            hasActiveWarning
            labels {{
                value
                category
                message
            }}
            downstreamMetricDefinitions {{
                name
                id
                luid
                fields {{
                    name
                    description
                }}
            }}
        }}
    }}
}}"""
