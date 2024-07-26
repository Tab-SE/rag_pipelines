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
        workbook_name = workbook['name']
        summary = f"""
# WORKBOOK NAME: {workbook_name}
This document provides a detailed description of the {workbook_name} workbook along with metadata such as
tags, dashboards, sheets and datasources

### DESCRIPTION:
 {workbook.get('description')}
Date Created: {workbook.get('createdAt')}
Date Last Updated: {workbook.get('updatedAt')}
Project Folder: {workbook.get('projectName')}

## FAQ
- Show me or describe the {workbook_name} workbook

## TAGS:
Use these keywords to help describe the use or application of this analysis

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
These are the dashboards contained in {workbook_name} which themselves are made up of sheets and other elements.
Dashboards are interactive views of data combining different charts or sheets into a single interface. As a result,
dashboards can answer multiple questions and present data in useful ways to stakeholders.

## FAQ
- List the dashboards in {workbook_name}
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
These are the sheets contained in {workbook_name}. Sheets can be standalone charts or used in combination
inside a dashboard. Sheets are created with desktop and or web authoring, constituting the basic building
block of visual analysis.

## FAQ
- What sheets, charts or vizzes are in the {workbook_name}?
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
Otherwise known as 'published datasources' these connections to databases, extracts or flat files
are made available to users of the application for self-serve analytice, to track organizational metrics
and constitute sources of truth. Workbooks may also possess 'embedded datasources' which are not shared
widely with other users and are therefore not listed.

## FAQ
- What datasources is {workbook_name} connected to?

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

#                 summary += """
# ## FIELDS:
# | Name | Description | Is Hidden | Folder Name |
# | --- | --- | --- | --- |
# """
#                 for field in datasource.get('fields', []):
#                     summary += f"| {field.get('name')} | {field.get('description') or 'N/A'} | {field.get('isHidden')} | {field.get('folderName') or 'N/A'} |\n"
        else:
            summary += "No upstream datasources\n"

        formatted_workbook_name = workbook_name.replace(' ', '_')

        workbook_summaries.append({formatted_workbook_name: summary})

    print('Total Workbooks: ', len(workbook_summaries))
    return workbook_summaries


def extract_workbooks_meta(workbook_summaries_json):
    workbook_summaries = json.loads(workbook_summaries_json)

    markdown_content = """# Workbooks Summary
This document lists all workbooks available to the user. When you respond to the user's query
use the following entire table verbatim as your response:

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

    markdown_content += """
## FAQ
- What workbooks, dashboards, charts, analysis, visualizations, vizzes or reports can I see?
- Show me what content I can explore
- what tableaus do I have access to?

## KEY TERMS
workbooks, charts, dashboards, analysis, visualizations, tableau, sheets
"""

    return markdown_content
