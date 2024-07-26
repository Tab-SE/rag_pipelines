import os, json

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
        summary = f"""# {workbook_name}
## DESCRIPTION:
 {workbook.get('description').strip()}

## FAQ
- Show me or describe {workbook_name}

### Metadata
Date Created: {workbook.get('createdAt')}
Date Last Updated: {workbook.get('updatedAt')}
Project Folder: {workbook.get('projectName')}

## TAGS:
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
## FAQ
- List the dashboards in {workbook_name}
"""
        dashboards = workbook.get('dashboards')
        if dashboards:
            summary += "\nWhen you respond to the user's query use the following entire list and table verbatim as your response, keep the links inside the list and table:\n\n"

            # Add markdown list
            for dashboard in dashboards:
                summary += f"- [{dashboard.get('name')}]({domain}/#/site/{site}/views/{dashboard.get('path')})\n"

            summary += "\n"  # Add a blank line between the list and the table

            # Add table
            summary += "| Dashboard | Created At | Updated At | Tags |\n"
            summary += "| --- | --- | --- | --- |\n"
            for dashboard in dashboards:
                if dashboard.get('tags'):
                    dashboard_tags = dashboard.get('tags', [])
                    dashboard_tag_names = [tag.get('name') for tag in dashboard_tags if tag.get('name')]
                summary += f"| [{dashboard.get('name')}]({domain}/#/site/{site}/views/{dashboard.get('path')}) | {dashboard.get('createdAt')} | {dashboard.get('updatedAt')} | {', '.join(dashboard_tag_names) if dashboard.get('tags') else 'No tags'} |\n"
        else:
            summary += "No dashboards\n"

        summary += "\n## SHEETS:\n"
        summary += f"""
## FAQ
- What sheets, charts or vizzes are in the {workbook_name}?
"""
        sheets = workbook.get('sheets')
        if sheets:
            summary += "\nWhen you respond to the user's query use the following entire table verbatim as your response:\n"
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
- What datasources is {workbook_name} connected to?

"""
        if workbook.get('upstreamDatasources'):
            for datasource in workbook['upstreamDatasources']:
                summary += f"""
# DATASOURCE NAME: {datasource.get('name')}
### DESCRIPTION: {datasource.get('description').strip()}
### PROJECT: {datasource.get('projectName')}
### IS CERTIFIED: {datasource.get('isCertified')}
### HAS EXTRACTS: {datasource.get('hasExtracts')}
"""
                summary += "\n## DOWNSTREAM METRIC DEFINITIONS:\n"
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


def extract_workbooks_meta(workbook_summaries_json):
    workbook_summaries = json.loads(workbook_summaries_json)

    markdown_content = """# Table Listing Workbooks Availabld to the User
When you respond to the user's query use the following entire table verbatim as your response:

| WORKBOOK | DESCRIPTION |
|------|-------------|
"""
    for workbook in workbook_summaries['data']['workbooks']:
        name = workbook['name']
        description = workbook.get('description', 'N/A')

        # Replace newline characters with spaces in the description
        if description != 'N/A':
            description = description.replace('\n', ' ')

        markdown_content += f"| {name} | {description.strip()} |\n"

    markdown_content += '\n' + """
## FAQ
- What are my workbooks?
- What workbooks or analytics do I have access to?
- List or Show all of my workbooks
"""

    return markdown_content
