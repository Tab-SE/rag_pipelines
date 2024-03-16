from jsonpath_ng import jsonpath, parse

def bundles(bundles):
    corpus = {}
    # extract only necessary metadata, Q&A, markup, vizzes, facts & other semantic features
    for key, bundle in bundles.items():
        metric = bundle['metric']
        time_options = bundle['time_options']
        insights = bundle['insights']
        definition = metric['definition']
        # remove 'viz_state_specification' if exists
        definition.pop('viz_state_specification', None)
        # creating a metadata string
        metadata = f"""
        The metric name is {metric['name']}
        It is described as '{metric['description']}'
        This metric considers change in value as: {metric['representation_options']['sentiment_type']}

        It is represented as: {metric['representation_options']['type']}
        It is measured by these units:
        Singular: {metric['representation_options']['number_units']['singular_noun']}
        Plural: {metric['representation_options']['number_units']['plural_noun']}

        The data driving this metric has these dimensions: {metric['extension_options']['allowed_dimensions']}
        With these granularities: {metric['extension_options']['allowed_granularities']}

        Tableau Pulse's AI generated insights were created at {time_options['formatted_time']}
        In the {time_options['timezone_name']} timezone

        Other Technical Descriptors:
        Specification: {metric['specification']}
        Basic Definition: {definition}
        """
        print('metadata', metadata)

        # for key, value in insights.items():
        #     print('key value', key, ':', value)

        for key, bundle in insights.items():
            bundle_type = bundle['result']['insight_groups'][0]['type']
            detail = bundle['result']['insight_groups'][0]['insights']
            # extract facts about the metric's current value
            if bundle_type == 'ban':
                insight_type = detail[0]['result']['type']
                score = detail[0]['result']['score']
                question = detail[0]['result']['question']
                answer = detail[0]['result']['markup']
                sentiment = detail[0]['result']['facts']['sentiment']
                current_raw_value = detail[0]['result']['facts']['target_period_value']['raw']
                current_formatted_value = detail[0]['result']['facts']['target_period_value']['formatted']
                previous_raw_value = detail[0]['result']['facts']['comparison_period_value']['raw']
                previous_formatted_value = detail[0]['result']['facts']['comparison_period_value']['formatted']
                current_time_period = detail[0]['result']['facts']['target_time_period']['label']
                current_time_range = detail[0]['result']['facts']['target_time_period']['range']
                current_time_granularity = detail[0]['result']['facts']['target_time_period']['granularity']
                previous_time_period = detail[0]['result']['facts']['comparison_time_period']['label']
                previous_time_range = detail[0]['result']['facts']['comparison_time_period']['range']
                previous_time_granularity = detail[0]['result']['facts']['comparison_time_period']['granularity']
                direction = detail[0]['result']['facts']['difference']['direction']
                absolute_raw_difference = detail[0]['result']['facts']['difference']['absolute']['raw']
                absolute_formatted_difference = detail[0]['result']['facts']['difference']['absolute']['formatted']
                relative_raw_difference = detail[0]['result']['facts']['difference']['relative']['raw']
                relative_formatted_difference = detail[0]['result']['facts']['difference']['relative']['formatted']

                current_metric_value = f"""
                """

        # payload containing document strings for loading
        documents = {
            "metadata": metadata,
            "current_metric_value": current_metric_value
        }
        # to identify metrics with the same name but different definitions
        index = f'{key} - {metric['name']}'
        # docs in corpus are indentified by {index}
        corpus[index] = documents
    return corpus
