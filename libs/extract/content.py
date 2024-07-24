def resources(catalog):
    print('Catalog areas received: ', list(catalog.keys()))
    extract_workbooks(catalog['workbooks'])
    extract_views(catalog['views'])
    extract_datasources(catalog['datasources'])


def extract_workbooks(workbooks):
    pass

def extract_views(views):
    pass

def extract_datasources(datasources):
    pass
