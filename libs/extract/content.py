import json

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
### DESCRIPTION:

{workbook.get('description')}
Date Created: {workbook.get('createdAt')}
Date Last Updated: {workbook.get('updatedAt')}
Project Folder: {workbook.get('projectName')}

## FAQ
- Show me {name}
- describe the {name} workbook
- tell me about the workbook called {name}

## TAGS:
"""
        if workbook.get('tags'):
            summary += "| Tag |\n| --- |\n"
            workbook_tags = workbook.get('tags', [])
            workbook_tag_names = [tag.get('name') for tag in workbook_tags if tag.get('name')]
            for tag in workbook_tag_names:
                summary += f"| {tag} |\n"
        else:
            summary += "No tags\n"

        summary += "\n## DASHBOARDS:\n"
        summary += f"""
## FAQ
- What dashboards are in the {name} workbook?
- Show me the dashboards for {name}
- List the dashboards found in {name}
"""
        dashboards = workbook.get('dashboards')
        if dashboards:
            summary += "\n| Name | Path | Created At | Updated At | Tags |\n| --- | --- | --- | --- | --- |\n"
            for dashboard in dashboards:
                if dashboard.get('tags'):
                    dashboard_tags = dashboard.get('tags', [])
                    dashboard_tag_names = [tag.get('name') for tag in dashboard_tags if tag.get('name')]
                summary += f"| {dashboard.get('name')} | {dashboard.get('path')} | {dashboard.get('createdAt')} | {dashboard.get('updatedAt')} | {', '.join(dashboard_tag_names) if dashboard.get('tags') else 'No tags'} |\n"
        else:
            summary += "No dashboards\n"

        summary += "\n## SHEETS:\n"
        summary += f"""
## FAQ
- What sheets are in the {name} workbook?
- Show me the charts for {name}
- List the vizzes found in {name}
"""
        sheets = workbook.get('sheets')
        if sheets:
            summary += "\n| Name | Path | Created At | Updated At | Tags |\n| --- | --- | --- | --- | --- |\n"
            for sheet in sheets:
                if sheet.get('tags'):
                    sheet_tags = sheet.get('tags', [])
                    sheet_tag_names = [tag.get('name') for tag in sheet_tags if tag.get('name')]
                summary += f"| {sheet.get('name')} | {sheet.get('path')} | {sheet.get('createdAt')} | {sheet.get('updatedAt')} | {', '.join(sheet_tag_names) if sheet.get('tags') else 'No tags'} |\n"
        else:
            summary += "No sheets\n"

        summary += "\n## UPSTREAM DATASOURCES:\n"
        summary += f"""
## FAQ
- What are the datasources used by the {name} dashboard?
- Which datasources is {name} connected to?
- show me the data for {name}

"""
        if workbook.get('upstreamDatasources'):
            for datasource in workbook['upstreamDatasources']:
                summary += f"""
# DATASOURCE NAME: {datasource.get('name')}
### DESCRIPTION: {datasource.get('description')}
### PROJECT: {datasource.get('projectName')}
### IS CERTIFIED: {datasource.get('isCertified')}
### HAS EXTRACTS: {datasource.get('hasExtracts')}
"""
                summary += "\n## DOWNSTREAM METRIC DEFINITIONS:\n"
                if datasource.get('downstreamMetricDefinitions'):
                    summary += "| Name | ID | LUID | Fields |\n| --- | --- | --- | --- |\n"
                    for metric in datasource['downstreamMetricDefinitions']:
                        fields = ', '.join([f"{field['name']}" for field in metric.get('fields', [])])
                        summary += f"| {metric.get('name')} | {metric.get('id')} | {metric.get('luid')} | {fields} |\n"
                else:
                    summary += "No downstream metric definitions\n"

                summary += """
## FIELDS:
| Name | Description | Is Hidden | Folder Name |
| --- | --- | --- | --- |
"""
                for field in datasource.get('fields', []):
                    summary += f"| {field.get('name')} | {field.get('description') or 'N/A'} | {field.get('isHidden')} | {field.get('folderName') or 'N/A'} |\n"
        else:
            summary += "No upstream datasources\n"

        workbook_summaries.append({name: summary})

    print('Total Workbooks: ', len(workbook_summaries))
    return workbook_summaries


def extract_workbooks_meta(workbook_summaries_json):
    workbook_summaries = json.loads(workbook_summaries_json)

    markdown_content = """# Workbooks Summary
## FAQ
- What are my workbooks?
- What dashboards, charts or analysis do I follow?
- What assets do I have access to?
- What workbooks, dashboards or charts can I see?
- What or where are my reports?
- What analysis do I have access to?
- Which analytics is available to me?
- List the vizzes or visualizations that I can look at
- Show me what content I can explore
- what tableaus can I see?

## KEY TERMS
workbooks, charts, dashboards, analysis, analytics, visualizations, tableau, tableaus, sheets

| Name | Description |
|------|-------------|
"""

    for workbook in workbook_summaries['data']['workbooks']:
        name = workbook['name']
        description = workbook.get('description', 'N/A')

        # Replace newline characters with spaces in the description
        if description != 'N/A':
            description = description.replace('\n', ' ')

        markdown_content += f"| {name} | {description} |\n"

    return markdown_content
