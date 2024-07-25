import json
from datetime import datetime

def resources(catalog):
    workbooks = {
        'files': extract_workbooks(catalog['workbooks']),
        'meta': extract_workbooks_meta(catalog['workbooks'])
    }

    return workbooks


def extract_workbooks(input):
    formatted_input = json.loads(input)
    workbooks = formatted_input['data']['workbooks']
    print('******* WORKBOOK METADATA *********', [list(workbook.keys()) for workbook in workbooks])

    workbook_summaries = []

    for workbook in workbooks:
        name = workbook['name']
        summary = f"""
# WORKBOOK NAME: {name}
### DESCRIPTION: {workbook.get('description')}
### CREATED_AT: {workbook.get('createdAt')}
### UPDATED_AT: {workbook.get('updatedAt')}
### PROJECT: {workbook.get('projectName')}

## TAGS:
"""
        if workbook.get('tags'):
            summary += "| Tag |\n| --- |\n"
            for tag in workbook['tags']:
                summary += f"| {tag} |\n"
        else:
            summary += "No tags\n"

        summary += "\n## DASHBOARDS:\n"
        if workbook.get('dashboards'):
            summary += "| Name | Path | Created At | Updated At | Tags |\n| --- | --- | --- | --- | --- |\n"
            for dashboard in workbook['dashboards']:
                summary += f"| {dashboard.get('name')} | {dashboard.get('path')} | {dashboard.get('createdAt')} | {dashboard.get('updatedAt')} | {', '.join(dashboard.get('tags')) if dashboard.get('tags') else 'No tags'} |\n"
        else:
            summary += "No dashboards\n"

        summary += "\n## SHEETS:\n"
        if workbook.get('sheets'):
            summary += "| Name | Path | Created At | Updated At | Tags |\n| --- | --- | --- | --- | --- |\n"
            for sheet in workbook['sheets']:
                summary += f"| {sheet.get('name')} | {sheet.get('path')} | {sheet.get('createdAt')} | {sheet.get('updatedAt')} | {', '.join(sheet.get('tags')) if sheet.get('tags') else 'No tags'} |\n"
        else:
            summary += "No sheets\n"

        summary += "\n## UPSTREAM DATASOURCES:\n"
        if workbook.get('upstreamDatasources'):
            for datasource in workbook['upstreamDatasources']:
                summary += f"""
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
                summary += f"| {field.get('name')} | {field.get('description') or 'N/A'} | {field.get('isHidden')} | {field.get('folderName') or 'N/A'} |\n"

            summary += "\n## DOWNSTREAM METRIC DEFINITIONS:\n"
            if datasource.get('downstreamMetricDefinitions'):
                summary += "| Name | ID | LUID | Fields |\n| --- | --- | --- | --- |\n"
                for metric in datasource['downstreamMetricDefinitions']:
                    fields = ', '.join([f"{field['name']}" for field in metric.get('fields', [])])
                    summary += f"| {metric.get('name')} | {metric.get('id')} | {metric.get('luid')} | {fields} |\n"
            else:
                summary += "No downstream metric definitions\n"
        else:
            summary += "No upstream datasources\n"

        workbook_summaries.append({name: summary})

    print('Total Workbooks: ', len(workbook_summaries))
    return workbook_summaries


def extract_datasources(input):
    formatted_input = json.loads(input)
    datasources = formatted_input['data']['datasources']
    print('******* DATASOURCE METADATA *********', [list(datasource.keys()) for datasource in datasources])

    for datasource in datasources:
        summary = f"""
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
            summary += f"| {field.get('name')} | {field.get('description') or 'N/A'} | {field.get('isHidden')} | {field.get('folderName') or 'N/A'} |\n"

        summary += "\n## DOWNSTREAM METRIC DEFINITIONS:\n"
        if datasource.get('downstreamMetricDefinitions'):
            summary += "| Name | ID | LUID | Fields |\n| --- | --- | --- | --- |\n"
            for metric in datasource['downstreamMetricDefinitions']:
                fields = ', '.join([f"{field['name']}" for field in metric.get('fields', [])])
                summary += f"| {metric.get('name')} | {metric.get('id')} | {metric.get('luid')} | {fields} |\n"
        else:
            summary += "No downstream metric definitions\n"

        return summary


def extract_workbooks_meta(workbook_summaries_json):
    workbook_summaries = json.loads(workbook_summaries_json)

    markdown_content = """# Workbook Summary
###### What dashboards, charts or analysis do I follow?
###### What assets do I have access to?
###### What workbooks, dashboards or charts can I see?
###### What or where are my reports?

| Name | Description |
|------|-------------|
"""

    for workbook in workbook_summaries['data']['workbooks']:
        name = workbook['name']
        description = workbook.get('description', 'N/A')

        markdown_content += f"| {name} | {description} |\n"

    return markdown_content
