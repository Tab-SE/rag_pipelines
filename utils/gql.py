import aiohttp
import json

async def query():
    url = "https://prod-useast-b.online.tableau.com/api/metadata/graphql"

    payload = json.dumps({
        "query": """query Content {
  workbooks {
    id
    luid
    name
    description
    createdAt
    projectName
    projectVizportalUrlId
    projectLuid
    uri
    tags {
      id
      name
    }
    dashboards {
      id
      luid
    }
    sheets {
      id
      luid
    }
  }

  dashboards {
    id
    luid
    name
    path
    createdAt
    updatedAt
    index
    tags {
      id
      name
    }
    sheets {
      id
      luid
    }
  }

  sheets {
    id
    luid
    documentViewId
    name
    path
    createdAt
    updatedAt
    index
    tags {
      id
      name
    }
    containedInDashboards {
      id
      luid
    }
    upstreamDatasources {
      id
      name
    }
  }

  publishedDatasources {
    id
    luid
    name
    description
    hasUserReference
    hasExtracts
    extractLastRefreshTime
    extractLastIncrementalUpdateTime
    extractLastUpdateTime
    projectName
    projectVizportalUrlId
    isCertified
    certificationNote
    certifierDisplayName
    containsUnsupportedCustomSql
    datasourceFilters {
      id
      field {
        id
      }
    }
    parameters {
      id
      name
    }
    hasActiveWarning
    dataQualityWarnings {
      id
      luid
      isActive
      isElevated
      value
      category
      message
      createdAt
      updatedAt
      asset {
        id
        luid
        name
      }
    }
    dataQualityCertifications {
      id
      luid
      isActive
      isElevated
      value
      category
      message
      createdAt
      updatedAt
      asset {
        id
        luid
        name
      }
    }
    labels {
      id
      luid
      isActive
      isElevated
      value
      category
      message
      createdAt
      updatedAt
      asset {
        id
        luid
        name
      }
    }
    tags {
      id
      name
    }
    createdAt
    updatedAt
    downstreamWorkbooks {
      id
      luid
    }
  }
}""",
        "variables": {}
    })

    headers = {
        'Content-Type': 'application/json',
        'X-Tableau-Auth': 'WI9l0DTRTh2aumfGuZW8SQ|apfva4G3v5AOqiL99x1k7HK8NUciNrSD|87db4137-fce1-4392-ac84-a289b96e3373'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as response:
            return await response.text()
