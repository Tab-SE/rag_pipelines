import json

def resources(catalog):
    print('Catalog areas received: ', list(catalog.keys()))
    extract_workbooks(catalog['workbooks'])

def extract_workbooks(input):
    formatted_input = json.loads(input)
    workbooks = formatted_input['data']['workbooks']
    print('******* WORKBOOK METADATA *********', [list(workbook.keys()) for workbook in workbooks])

    for workbook in workbooks:
        details = f"""
# WORKBOOK NAME: {workbook.get('name')}
### DESCRIPTION: {workbook.get('description')}
### CREATED_AT: {workbook.get('createdAt')}
### UPDATED_AT: {workbook.get('updatedAt')}
### PROJECT: {workbook.get('projectName')}

## TAGS:
"""
        if workbook.get('tags'):
            details += "| Tag |\n| --- |\n"
            for tag in workbook['tags']:
                details += f"| {tag} |\n"
        else:
            details += "No tags\n"

        details += "\n## DASHBOARDS:\n"
        if workbook.get('dashboards'):
            details += "| Name | Path | Created At | Updated At | Tags |\n| --- | --- | --- | --- | --- |\n"
            for dashboard in workbook['dashboards']:
                details += f"| {dashboard.get('name')} | {dashboard.get('path')} | {dashboard.get('createdAt')} | {dashboard.get('updatedAt')} | {', '.join(dashboard.get('tags')) if dashboard.get('tags') else 'No tags'} |\n"
        else:
            details += "No dashboards\n"

        details += "\n## SHEETS:\n"
        if workbook.get('sheets'):
            details += "| Name | Path | Created At | Updated At | Tags |\n| --- | --- | --- | --- | --- |\n"
            for sheet in workbook['sheets']:
                details += f"| {sheet.get('name')} | {sheet.get('path')} | {sheet.get('createdAt')} | {sheet.get('updatedAt')} | {', '.join(sheet.get('tags')) if sheet.get('tags') else 'No tags'} |\n"
        else:
            details += "No sheets\n"

        details += "\n## UPSTREAM DATASOURCES:\n"
        if workbook.get('upstreamDatasources'):
            for datasource in workbook['upstreamDatasources']:
                details += f"""
# DATASOURCE NAME: {datasource.get('name')}
### DESCRIPTION: {datasource.get('description')}
### PROJECT: {datasource.get('projectName')}
### IS CERTIFIED: {datasource.get('isCertified')}
### HAS EXTRACTS: {datasource.get('hasExtracts')}
### OWNER: {datasource.get('owner', {}).get('name')} ({datasource.get('owner', {}).get('email')})

## FIELDS:
| Name | Description | Is Hidden | Folder Name |
| --- | --- | --- | --- |
"""
            for field in datasource.get('fields', []):
                details += f"| {field.get('name')} | {field.get('description') or 'N/A'} | {field.get('isHidden')} | {field.get('folderName') or 'N/A'} |\n"

            details += "\n## DOWNSTREAM METRIC DEFINITIONS:\n"
            if datasource.get('downstreamMetricDefinitions'):
                details += "| Name | ID | LUID | Fields |\n| --- | --- | --- | --- |\n"
                for metric in datasource['downstreamMetricDefinitions']:
                    fields = ', '.join([f"{field['name']}" for field in metric.get('fields', [])])
                    details += f"| {metric.get('name')} | {metric.get('id')} | {metric.get('luid')} | {fields} |\n"
            else:
                details += "No downstream metric definitions\n"
        else:
            details += "No upstream datasources\n"

        print('***** WORKBOOK DETAILS ******')
        print(details)
        print('***** END DETAILS ******')

def extract_datasources(input):
    formatted_input = json.loads(input)
    datasources = formatted_input['data']['datasources']
    print('******* DATASOURCE METADATA *********', [list(datasource.keys()) for datasource in datasources])

    for datasource in datasources:
        details = f"""
# DATASOURCE NAME: {datasource.get('name')}
### DESCRIPTION: {datasource.get('description')}
### PROJECT: {datasource.get('projectName')}
### IS CERTIFIED: {datasource.get('isCertified')}
### HAS EXTRACTS: {datasource.get('hasExtracts')}
### OWNER: {datasource.get('owner', {}).get('name')} ({datasource.get('owner', {}).get('email')})

## FIELDS:
| Name | Description | Is Hidden | Folder Name |
| --- | --- | --- | --- |
"""
        for field in datasource.get('fields', []):
            details += f"| {field.get('name')} | {field.get('description') or 'N/A'} | {field.get('isHidden')} | {field.get('folderName') or 'N/A'} |\n"

        details += "\n## DOWNSTREAM METRIC DEFINITIONS:\n"
        if datasource.get('downstreamMetricDefinitions'):
            details += "| Name | ID | LUID | Fields |\n| --- | --- | --- | --- |\n"
            for metric in datasource['downstreamMetricDefinitions']:
                fields = ', '.join([f"{field['name']}" for field in metric.get('fields', [])])
                details += f"| {metric.get('name')} | {metric.get('id')} | {metric.get('luid')} | {fields} |\n"
        else:
            details += "No downstream metric definitions\n"

        print('***** DATASOURCE DETAILS ******')
        print(details)
        print('***** END DETAILS ******')
