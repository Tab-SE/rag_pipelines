import os

def insights_corpus(params):
    # Extract insights and mode from params
    insights = params.get('insights')
    mode = params.get('mode')

    # Validate mode
    if mode not in ['md', 'txt']:
        raise ValueError("Mode must be either 'md' or 'txt'.")

    # Set file extension based on mode
    file_extension = f'.{mode}'

    try:
        # Create 'data/analytics/metrics/' folder if it doesn't exist
        metrics_path = os.path.join('data', 'analytics', 'metrics')
        os.makedirs(metrics_path, exist_ok=True)

        # Metadata file in root of insights/
        corpus_metadata_path = os.path.join(metrics_path, f'insights_metadata{file_extension}')
        with open(corpus_metadata_path, 'w') as f:
            f.write(insights['corpus_metadata'])
    except Exception as e:
        print(f"An error occurred while processing metadata: {e}")

    # Loop through key-value pairs in insights dict
    for index, (key, metric) in enumerate(insights['corpus'].items()):
        folder_name = f"{key.replace(' ', '_')}"
        folder_path = os.path.join(metrics_path, folder_name)

        try:
            # Create 'data/analytics/metrics/{folder_name}' folder if it doesn't exist
            os.makedirs(folder_path, exist_ok=True)
            # Write metadata file to parent folder
            metadata_path = os.path.join(folder_path, f'{folder_name}{file_extension}')
            with open(metadata_path, 'w') as f:
                f.write(metric['metadata'])
        except Exception as e:
            print(f"An error occurred while processing 'metadata' for key '{key}': {e}")

        # Create 'data/analytics/metrics/{folder_name}/insights' child folder if it doesn't exist
        insights_folder_path = os.path.join(folder_path, 'insights')
        os.makedirs(insights_folder_path, exist_ok=True)

        try:
            # Write insight summary files
            metric_insights = metric['insights']
            for i, insight in enumerate(metric_insights['ban']):
                ban_path = os.path.join(insights_folder_path, f'ban_{i}{file_extension}')
                with open(ban_path, 'w') as f:
                    f.write(insight)
        except Exception as e:
            print(f"An error occurred while processing 'ban' for key '{key}': {e}")

        try:
            for i, insight in enumerate(metric_insights['anchor']):
                anchor_path = os.path.join(insights_folder_path, f'anchor_{i}{file_extension}')
                with open(anchor_path, 'w') as f:
                    f.write(insight)
        except Exception as e:
            print(f"An error occurred while processing 'anchor' for key '{key}': {e}")

        try:
            for i, insight in enumerate(metric_insights['breakdown']):
                breakdown_path = os.path.join(insights_folder_path, f'breakdown_{i}{file_extension}')
                with open(breakdown_path, 'w') as f:
                    f.write(insight)
        except Exception as e:
            print(f"An error occurred while processing 'breakdown' for key '{key}': {e}")

        try:
            for i, insight in enumerate(metric_insights['followup']):
                followup_path = os.path.join(insights_folder_path, f'followup_{i}{file_extension}')
                with open(followup_path, 'w') as f:
                    f.write(insight)
        except Exception as e:
            print(f"An error occurred while processing 'followup' for key '{key}': {e}")

    return True


def catalog_corpus(params):
    # Extract catalog and mode from params
    catalog = params.get('catalog')
    mode = params.get('mode')

    # Validate mode
    if mode not in ['md', 'txt']:
        raise ValueError("Mode must be either 'md' or 'txt'.")

    # Set file extension based on mode
    file_extension = f'.{mode}'

    output_dir = 'data/analytics/catalog/workbooks'
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Define the file path for workbooks metadata file
    meta_path = f'data/analytics/catalog/workbooks_meta{file_extension}'

    # Write the metadata content to the file
    with open(meta_path, 'w', encoding='utf-8') as file:
        file.write(catalog['meta'])

    print(f"Metadata file written: {meta_path}")

    # Loop through summaries in the catalog
    for index, summary in enumerate(catalog['files']):
        for key, markdown_content in summary.items():
            folder_name = f"{index}_{key.replace(' ', '_')}"
            folder_path = os.path.join(output_dir, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            files_path = os.path.join(folder_path, f"{folder_name}{file_extension}")

            # Write the content to the file
            with open(files_path, 'w', encoding='utf-8') as file:
                file.write(markdown_content)

            print(f"File written: {files_path}")
