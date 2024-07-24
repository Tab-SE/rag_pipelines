from utils import gql

async def query_workbooks(token):
    print(f'Workbooks metadata received')
    workbooks = await gql.query(query=workbooks_query, token=token)
    return workbooks

async def query_views(token):
    print(f'Views metadata received')
    views = await gql.query(query=views_query, token=token)
    return views

async def query_datasources(token):
    print(f'Datasources metadata received')
    datasources = await gql.query(query=datasources_query, token=token)
    return datasources

workbooks_query = """query Workbooks {
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
}"""

views_query = """query Views {
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
}"""

datasources_query = """query datasources {
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
}"""
