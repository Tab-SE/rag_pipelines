import os

def resources(catalog):
    workbooks = {
        'files': extract_workbooks(catalog['workbooks']),
        'meta': extract_workbooks_meta(catalog['workbooks'])
    }

    return workbooks


def extract_workbooks(input):
    workbooks = input['data']['workbooks']
    print('******* WORKBOOK METADATA *********', [list(workbook.keys()) for workbook in workbooks])

    workbook_summaries = []

    for workbook in workbooks:
        workbook_name = workbook['name']
        summary = f"""# {workbook_name}
**Describe**: {workbook_name}
{workbook.get('description').strip()}
**Question**: When was {workbook_name} created or updated?
Date Created: {workbook.get('createdAt')}
Date Last Updated: {workbook.get('updatedAt')}
**Question**: What project is {workbook_name} in?
Project Folder: {workbook.get('projectName')}
**Question**: What are the tags for {workbook_name}?
"""
        if workbook.get('tags'):
            summary += "\nWhen you respond to the user's query use the following entire table verbatim as your response:\n"
            summary += "| Tag |\n| --- |\n"
            workbook_tags = workbook.get('tags', [])
            workbook_tag_names = [tag.get('name') for tag in workbook_tags if tag.get('name')]
            for tag in workbook_tag_names:
                summary += f"| {tag} |\n"
        else:
            summary += "No tags\n"

        domain = os.environ['TABLEAU_DOMAIN']
        site = os.environ['TABLEAU_SITE']

        summary += "\n## Dashboards:\n"
        summary += f"""**Question**: What dashboards are in {workbook_name}?
"""
        dashboards = workbook.get('dashboards')
        if dashboards:
            summary += "When you respond to the user's query use the following entire list and table verbatim as your response, keep the links inside the list and table:\n"

            # Add markdown list
            for dashboard in dashboards:
                summary += f"- [{dashboard.get('name')}]({domain}/#/site/{site}/views/{dashboard.get('path')})\n"

            summary += "\n"  # Add a blank line between the list and the table
        else:
            summary += "No dashboards\n"

        sheets = workbook.get('sheets')
        if sheets:
            summary += "## Sheets:\n"
            summary += f"""**Question**: What sheets are in {workbook_name}?\n"""
            summary += "When you respond to the user's query use the following entire list verbatim as your response:\n\n"

            # Add markdown list for sheets
            for sheet in sheets:
                summary += f"- [{sheet.get('name')}]({domain}/#/site/{site}/sheets/{sheet.get('path')})\n"

            summary += "\n"  # Add a blank line after the list
        else:
            summary += "No sheets\n"

#         summary += "\n## UPSTREAM DATASOURCES:\n"
#         summary += f"""
# **Question**: Which datasources is {workbook_name} connected to?
# """
#         if workbook.get('upstreamDatasources'):
#             for datasource in workbook['upstreamDatasources']:
#                 datasource_name = datasource.get('name')
#                 summary += f"""
# # DATASOURCE NAME: {datasource_name}
# ## Describe {datasource_name}
# ## What is {datasource_name}?
# ## What does {datasource_name} do?
# Description: {datasource.get('description').strip()}

# ## What project is {datasource_name} in?
# Project Folder: {datasource.get('projectName')}

# ## Is {datasource_name} a certified datasource?
# ## Has {datasource_name} been certified
# IS CERTIFIED: {datasource.get('isCertified')}

# ## Does {datasource_name} have extracts?
# ## is {datasource_name} an extract datasource?
# HAS EXTRACTS: {datasource.get('hasExtracts')}
# """
#                 summary += f"""
# ## Which metrics are connected to {datasource.get('name')}?
# ## Show me what metrics use {datasource.get('name')}
# """
#                 summary += "\nWhen you respond to the user's query use the following entire table verbatim as your response:\n"
#                 if datasource.get('downstreamMetricDefinitions'):
#                     summary += "| Name | ID | LUID | Fields |\n| --- | --- | --- | --- |\n"
#                     for metric in datasource['downstreamMetricDefinitions']:
#                         fields = ', '.join([f"{field['name']}" for field in metric.get('fields', [])])
#                         summary += f"| {metric.get('name')} | {metric.get('id')} | {metric.get('luid')} | {fields} |\n"
#                 else:
#                     summary += "No downstream metric definitions\n"
#         else:
#             summary += "No upstream datasources\n"

        formatted_workbook_name = workbook_name.replace(' ', '_')

        workbook_summaries.append({formatted_workbook_name: summary})

    print('Total Workbooks: ', len(workbook_summaries))
    return workbook_summaries

def extract_workbooks_meta(workbook_payload):
    markdown_content = """# What are my workbooks?
Related Questions: [
"What reports or analytics do I have access to?",
"List or show all of my workbooks",
"What workbooks are concerned with X (topic)?",
"Help me find workbooks that match my topic of interest",
"Which workbooks displays data for X (topic)?"
]

This document provides a summary of all Tableau workbooks that the given user has access to. The most important
data is the description provided to the analyst since it helps users find workbooks that answer their questions
or display information related to topics of interest.

This also helps provide users with information related to dashboards contained inside these workbooks.
Please include the "Path" in all of your responses:
"""
    for index, workbook in enumerate(workbook_payload['data']['workbooks']):
        name = workbook['name']
        description = workbook.get('description', 'N/A')
        created_at = workbook.get('createdAt', 'N/A')
        updated_at = workbook.get('updatedAt', 'N/A')
        dashboards = workbook.get('dashboards', [])
        datasources = workbook.get('upstreamDatasources', [])

        # Replace newline characters with spaces in the description
        if description != 'N/A':
            description = description.replace('\n', ' ')

        markdown_content += f"{index}. **{name}**\n"
        markdown_content += f"  - Description: {description.strip()}\n"
        # markdown_content += f"  - Created At: {created_at}\n"
        # markdown_content += f"  - Updated At: {updated_at}\n"

        # if dashboards:
        #     markdown_content += f"  - Dashboards:\n"
        #     for dashboard in dashboards:
        #         dashboard_name = dashboard.get('name', 'N/A')
        #         dashboard_path = dashboard.get('path', 'N/A')
        #         markdown_content += f"      - {dashboard_name}\n"
        #         markdown_content += f"          - Path: {os.environ['TABLEAU_DOMAIN']}/t/{os.environ['TABLEAU_SITE']}/views/{dashboard_path}\n"

        # if datasources:
        #     markdown_content += f"  - Datasources:\n"
        #     for datasource in datasources:
        #         datasource_name = datasource.get('name', 'N/A')
        #         datasource_description = datasource.get('description', 'N/A')
        #         is_certified = datasource.get('isCertified', False)
        #         markdown_content += f"      - {datasource_name}\n"
        #         markdown_content += f"          - Description: {datasource_description}\n"
        #         markdown_content += f"          - Certified: {is_certified}\n"

    return markdown_content
