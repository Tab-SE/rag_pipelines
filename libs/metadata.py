from utils import gql

async def query_workbooks(token, project_name):
    project_workbook_query = f"""
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
            fields {{
                name
                description
                isHidden
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
            owner {{
                username
                name
                email
            }}
            hasActiveWarning
            labels {{
                author {{
                    id
                }}
                authorDisplayName
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
    workbooks = await gql.query(query=project_workbook_query, token=token)
    # Errors:
    # {"errors":[{"message":"Execution canceled because timeout of 30000 millis was reached","locations":[]}],"data":null}
    # {"errors":[{"message":"One or more of the attributes used in your filter contain sensitive data so your results have been automatically filtered to contain only the results you have permissions to see","extensions":{"severity":"WARNING","code":"PERMISSIONS_MODE_SWITCHED","properties":{"workbooks":["projectName"]}}}],"data":{"workbooks":[]}}
    print(f'Workbooks metadata received')
    return workbooks
