import os

def insights_corpus(insights):
    try:
        # create 'data/insights/' folder if it doesn't exist
        corpus_path = os.path.join('data', 'insights')
        os.makedirs(corpus_path, exist_ok=True)
        #
        corpus_metadata_path = os.path.join('data', 'insights', 'insights_metadata.md')
        # metadata file in root of insights/
        with open(corpus_metadata_path, 'w') as f:
            f.write(insights['corpus_metadata'])
    except Exception as e:
        print(f"An error occurred while processing metadata: {e}")

    # loop through key-value pairs in insights dict
    for key, metric in insights['corpus'].items():
        try:
            folder_path = os.path.join('data', 'insights', key)
            # create 'data/insights/ folder if it doesn't exist
            os.makedirs(folder_path, exist_ok=True)
            # write metadata file to parent folder
            metadata_path = os.path.join(folder_path, f'{key}.md')
            with open(metadata_path, 'w') as f:
                f.write(metric['metadata'])
        except Exception as e:
            print(f"An error occurred while processing 'metadata' for key '{key}': {e}")

        # create 'data/insights/{key}/insights' child folder if it doesn't exist
        insights_folder_path = os.path.join('data', 'insights', key, 'insights')
        os.makedirs(insights_folder_path, exist_ok=True)

        try:
            # write insight summary files
            metric_insights = metric['insights']
            for index, insight in enumerate(metric_insights['ban']):
                ban_path = os.path.join(insights_folder_path, f'ban_{index}.md')
                with open(ban_path, 'w') as f:
                    f.write(insight)
        except Exception as e:
            print(f"An error occurred while processing 'ban' for key '{key}': {e}")

        try:
            for index, insight in enumerate(metric_insights['anchor']):
                anchor_path = os.path.join(insights_folder_path, f'anchor_{index}.md')
                with open(anchor_path, 'w') as f:
                    f.write(insight)
        except Exception as e:
            print(f"An error occurred while processing 'anchor' for key '{key}': {e}")

        try:
            for index, insight in enumerate(metric_insights['breakdown']):
                breakdown_path = os.path.join(insights_folder_path, f'breakdown_{index}.md')
                with open(breakdown_path, 'w') as f:
                    f.write(insight)
        except Exception as e:
            print(f"An error occurred while processing 'breakdown' for key '{key}': {e}")

        try:
            for index, insight in enumerate(metric_insights['followup']):
                followup_path = os.path.join(insights_folder_path, f'followup_{index}.md')
                with open(followup_path, 'w') as f:
                    f.write(insight)
        except Exception as e:
            print(f"An error occurred while processing 'followup' for key '{key}': {e}")
    return True

def catalog_corpus(catalog):
    output_dir='data/catalog/workbooks'
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Define the file path for workbooks metadata file
    meta_path = 'data/catalog/workbooks.md'
    # Write the markdown content to the file
    with open(meta_path, 'w', encoding='utf-8') as file:
        file.write(catalog['meta'])

    print(f"Markdown metadata file written: {meta_path}")

    # similar logic but loops through summaries in list
    for summary in catalog['files']:
        for key, markdown_content in summary.items():
            files_path = os.path.join(output_dir, f"{key}.md")

            # Write the markdown content to the file
            with open(files_path, 'w', encoding='utf-8') as file:
                file.write(markdown_content)

            print(f"Markdown file written: {files_path}")
