from utils import gql

async def query_workbooks(token):
    print(f'Workbooks metadata received')
    workbooks = await gql.query(query=workbooks_filter_query, token=token)
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

workbooks_filter_query = """query Workbooks {
    workbooks(filter: { projectName: ["Comcast","ebikes","superstore"] }) {
        name
        description
        createdAt
        projectName
        tags {
            name
        }
        dashboards {
            name
            path
            createdAt
            updatedAt
            tags {
                name
            }
        }
        sheets {
            name
            path
            createdAt
            updatedAt
            tags {
                name
            }
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
    name
    description
    hasExtracts
    extractLastRefreshTime
    extractLastIncrementalUpdateTime
    extractLastUpdateTime
    projectName
    isCertified
    certificationNote
    certifierDisplayName
    fields {
      name
      description
      isHidden
      folderName
    }
    datasourceFilters {
      field {
        id
        name
        fullyQualifiedName
        description
        descriptionInherited {
          assetId
        }
        folderName
      }
    }
    parameters {
      name
      parentName
    }
    hasActiveWarning
    dataQualityWarnings {
      isActive
      isElevated
      value
      category
      message
      createdAt
      updatedAt
      asset {
        name
        labels {
          author {
            id
          }
          authorDisplayName
          value
          category
          isActive
          isElevated
        }
      }
    }
    dataQualityCertifications {
      isActive
      isElevated
      value
      category
      message
      createdAt
      updatedAt
      asset {
        name
        labels {
          author {
            id
          }
          authorDisplayName
          value
          category
          isActive
          isElevated
        }
      }
    }
    labels {
      isActive
      isElevated
      value
      category
      message
      createdAt
      updatedAt
      asset {
        name
      }
    }
    tags {
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

datasources_filter_query = """query datasources {
  publishedDatasources (filter: { projectName: ["Comcast","ebikes","superstore"] }) {
    name
    description
    hasExtracts
    extractLastRefreshTime
    extractLastIncrementalUpdateTime
    extractLastUpdateTime
    projectName
    isCertified
    certificationNote
    certifierDisplayName
    fields {
      name
      description
      isHidden
      folderName
    }
    datasourceFilters {
      field {
        id
        name
        fullyQualifiedName
        description
        descriptionInherited {
          assetId
        }
        folderName
      }
    }
    parameters {
      name
      parentName
    }
    hasActiveWarning
    dataQualityWarnings {
      isActive
      isElevated
      value
      category
      message
      createdAt
      updatedAt
      asset {
        name
        labels {
          author {
            id
          }
          authorDisplayName
          value
          category
          isActive
          isElevated
        }
      }
    }
    dataQualityCertifications {
      isActive
      isElevated
      value
      category
      message
      createdAt
      updatedAt
      asset {
        name
        labels {
          author {
            id
          }
          authorDisplayName
          value
          category
          isActive
          isElevated
        }
      }
    }
    labels {
      isActive
      isElevated
      value
      category
      message
      createdAt
      updatedAt
      asset {
        name
      }
    }
    tags {
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
