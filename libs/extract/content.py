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
## Describe {workbook_name}
## What is {workbook_name} about?
## What does {workbook_name} do?
 {workbook.get('description').strip()}

## When was {workbook_name}?
## At what time was {workbook_name} last updated?
Date Created: {workbook.get('createdAt')}
Date Last Updated: {workbook.get('updatedAt')}

## What project is {workbook_name} in?
Project Folder: {workbook.get('projectName')}

## What are the tags for {workbook_name}?
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

        summary += "\n## DASHBOARDS:\n"
        summary += f"""
## What dashboards are in {workbook_name}?
## Show me {workbook_name}'s dashboards
"""
        dashboards = workbook.get('dashboards')
        if dashboards:
            summary += "\nWhen you respond to the user's query use the following entire list and table verbatim as your response, keep the links inside the list and table:\n\n"

            # Add markdown list
            for dashboard in dashboards:
                summary += f"- [{dashboard.get('name')}]({domain}/#/site/{site}/views/{dashboard.get('path')})\n"

            summary += "\n"  # Add a blank line between the list and the table

            # Add table
            summary += "| Dashboard | Created At | Updated At |\n"
            summary += "| --- | --- | --- |\n"
            for dashboard in dashboards:
                if dashboard.get('tags'):
                    dashboard_tags = dashboard.get('tags', [])
                    dashboard_tag_names = [tag.get('name') for tag in dashboard_tags if tag.get('name')]
                summary += f"| [{dashboard.get('name')}]({domain}/#/site/{site}/views/{dashboard.get('path')}) | {dashboard.get('createdAt')} | {dashboard.get('updatedAt')} |\n"
        else:
            summary += "No dashboards\n"

        summary += "\n## SHEETS:\n"
        summary += f"""
## What sheets are in the {workbook_name}?
## Which charts or vizzes are in {workbook_name}?
## List {workbook_name}'s visualizations
"""
        sheets = workbook.get('sheets')
        if sheets:
            summary += "\nWhen you respond to the user's query use the following entire table verbatim as your response:\n"
            summary += "\n| Name | Path | Created At | Updated At |\n| --- | --- | --- | --- |\n"
            for sheet in sheets:
                summary += f"| {sheet.get('name')} | {sheet.get('path')} | {sheet.get('createdAt')} | {sheet.get('updatedAt')}\n"
        else:
            summary += "No sheets\n"

        summary += "\n## UPSTREAM DATASOURCES:\n"
        summary += f"""
## Which datasources is {workbook_name} connected to?
## What data does {workbook_name} use?
## Show me the datasets for {workbook_name}
"""
        if workbook.get('upstreamDatasources'):
            for datasource in workbook['upstreamDatasources']:
                datasource_name = datasource.get('name')
                summary += f"""
# DATASOURCE NAME: {datasource_name}
## Describe {datasource_name}
## What is {datasource_name}?
## What does {datasource_name} do?
Description: {datasource.get('description').strip()}

## What project is {datasource_name} in?
Project Folder: {datasource.get('projectName')}

## Is {datasource_name} a certified datasource?
## Has {datasource_name} been certified
IS CERTIFIED: {datasource.get('isCertified')}

## Does {datasource_name} have extracts?
## is {datasource_name} an extract datasource?
HAS EXTRACTS: {datasource.get('hasExtracts')}
"""
                summary += f"""
## Which metrics are connected to {datasource.get('name')}?
## Show me what metrics use {datasource.get('name')}
"""
                summary += "\nWhen you respond to the user's query use the following entire table verbatim as your response:\n"
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

# def extract_workbooks_meta(workbook_summaries_json):
#     workbook_summaries = json.loads(workbook_summaries_json)

#     markdown_content = """## What are my workbooks?
# ## What reports or analytics do I have access to?
# ## List or show all of my workbooks
# """
#     for index, workbook in enumerate(workbook_summaries['data']['workbooks']):
#         name = workbook['name']
#         description = workbook.get('description', 'N/A')

#         # Replace newline characters with spaces in the description
#         if description != 'N/A':
#             description = description.replace('\n', ' ')

#         markdown_content += f"{index}. {name} | {description.strip()}\n"

#     return markdown_content

def extract_workbooks_meta(workbook_payload):
    markdown_content = """## What are my workbooks?
## What reports or analytics do I have access to?
## List or show all of my workbooks
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
        markdown_content += f"  - Created At: {created_at}\n"
        markdown_content += f"  - Updated At: {updated_at}\n"

        if dashboards:
            markdown_content += f"  - Dashboards:\n"
            for dashboard in dashboards:
                dashboard_name = dashboard.get('name', 'N/A')
                dashboard_path = dashboard.get('path', 'N/A')
                markdown_content += f"      - {dashboard_name}\n"
                markdown_content += f"          - Path: {os.environ['TABLEAU_DOMAIN']}/t/{os.environ['TABLEAU_SITE']}/views/{dashboard_path}\n"

                'https://prod-useast-b.online.tableau.com/t/embeddingplaybook/views/AUTOMATIC_COSTOVERVIEW/CostOverview'

        if datasources:
            markdown_content += f"  - Datasources:\n"
            for datasource in datasources:
                datasource_name = datasource.get('name', 'N/A')
                datasource_description = datasource.get('description', 'N/A')
                is_certified = datasource.get('isCertified', False)
                markdown_content += f"      - {datasource_name}\n"
                markdown_content += f"          - Description: {datasource_description}\n"
                markdown_content += f"          - Certified: {is_certified}\n"

    return markdown_content
