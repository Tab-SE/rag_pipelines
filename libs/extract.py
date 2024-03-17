from jsonpath_ng import jsonpath, parse

def bundles(bundles):
    corpus = {}
    # extract only necessary metadata, Q&A, markup, vizzes, facts & other semantic features
    for key, bundle in bundles.items():
        metric = bundle['metric']
        time_options = bundle['time_options']
        definition = metric['definition']
        # remove 'viz_state_specification' if exists
        definition.pop('viz_state_specification', None)
        # creating a metadata string
        metadata = extractMetadata(metric=metric, definition=definition, time_options=time_options)
        insights_bundle = bundle['insights']
        insights = extractInsights(insights_bundle=insights_bundle, metric=metric, time_options=time_options)
        # payload containing document strings for loading
        documents = {
            'metadata': metadata,
            'insights': insights,
        }
        # to identify metrics with the same name but different definitions
        index = f'{key} - {metric['name']}'
        # docs in corpus are indentified by {index}
        corpus[index] = documents
    return corpus

def extractMetadata(metric, definition, time_options):
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
    return metadata

def extractInsights(insights_bundle, metric, time_options):
    for key, bundle in insights_bundle.items():
        insight_groups = bundle['result']['insight_groups']
        for insight_group in insight_groups:
            # extract facts about the metric's current value
            if insight_group['type'] == 'ban':
                detail = bundle['result']['insight_groups'][0]['insights']
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
                The metric {metric['name']} has a value of {current_formatted_value} ({current_raw_value} in raw value)
                The current value was recorded on {current_time_period} during a time range of {current_time_range} and is
                measured every {current_time_granularity}

                The previous value for this metric was {previous_formatted_value} ({previous_raw_value} in previous raw value)
                The previous value was recorded on {previous_time_period} during a time range of {previous_time_range} and is
                measured every {previous_time_granularity}

                Therefore the metric value is currently trending {direction}. This is considered {sentiment} since the metric
                is defined as {metric['representation_options']['sentiment_type']}

                This Tableau Pulse AI generated insights was created at {time_options['formatted_time']}
                In the {time_options['timezone_name']} timezone
                """

                print('current_metric_value', current_metric_value)

                period_over_period_change = f"""
                Metric: {metric['name']}
                Insight Type: {insight_types['popc']['name']}
                Description: {insight_types['popc']['description']}
                The insight has a score of: {score}

                Question: {question}
                Answer: {answer}

                The metric had a relative change of {relative_formatted_difference} ({relative_raw_difference} in raw value)
                In absolute terms the change was {absolute_formatted_difference} ({absolute_raw_difference} in raw value)

                This Tableau Pulse AI generated insights was created at {time_options['formatted_time']}
                In the {time_options['timezone_name']} timezone
                """

                print('period_over_period_change', period_over_period_change)

            # extract facts about the metric's current value
            if insight_group['type'] == 'anchor':
                detail = bundle['result']['insight_groups'][0]['insights']

    insights = {
        'current_metric_value': current_metric_value,
        'period_over_period_change': period_over_period_change,
    }

    return insights


insight_types = {
    'popc': {
        'name': 'Period over Period Change',
        'description': """Shows how a metric has changed between two periods. Highlights the change between a metric value for a
    recent time range compared to an equivalent time range in a prior period or the past"""
    },
    'riskmo': {
        'name': 'Risky Monopoly',
        'description': """Shows when a small number of dimension members make up a majority (50% or more) of the contribution
        to a metric. Shows dimensions with a concentration of very high values"""
    },
    'top-contributors': {
        'name': 'Top Contributors',
        'description': """Shows the highest values in a dimension for a metric within a given time range. A top contributor
        is a dimension member that ranks in the top N in contribution to the scoped metric's value, aggregated on a specified
        time range.
        or
        Shows the lowest values in a dimension for a metric within a given time range. A bottom contributor is a dimension member
        that ranks in the bottom N in contribution to the scoped metricâ€™s value, aggregated on a specified time range.
        """
    },
    'bottom-contributors': {
        'name': 'Bottom Contributors',
        'description': """Shows the lowest values in a dimension for a metric within a given time range. A bottom contributor is
        a dimension membercthat ranks in the bottom N in contribution to the scoped metricâ€™s value, aggregated on a specified
        time range.
        """
    },
    'top-drivers': {
        'name': 'Top Drivers',
        'description': """Shows values for dimension members that changed the most in the same direction as the observed change
        in the metric. Shows the values for a metric that increased the most across a specified time offset

        A top driver is a dimension member that ranks in the top N in driving a change in a metric value between two separate
        but equivalent time ranges

        Top drivers are analyzed using metric values from two separate but equivalent time ranges (such as Sales for day of
        October 2 versus Sales for day of October 3) to look for changes to the contributions in the same direction of the change
        made by dimension members
        """
    },
    'top-detractors': {
        'name': 'Top Detractors',
        'description': """Shows values for dimension members that changed the most in the opposite direction to the observed change
        in the metric. Shows values for a metric that are most opposed to top drivers decreased the most across a specified time offset

        A top detractor is a dimension member that ranks in the bottom N in driving a change in a metric value between two separate
        but equivalent time ranges. This insight's values oppose the observed change the most

        Top detractors are analyzed using metric values from two separate but equivalent time ranges (such as Sales for day of
        October 2 versus Sales for day of October 3) to look for changes to the contributions in the same direction of the change
        made by dimension members
        """
    },
    'unusualchange': {
        'name': 'Unusually High/Low Metric value',
        'description': """Shows unexpected changes in a metric value

        Shows when the value of a metric for a given time range is higher or lower than the expected range based on historic
        observations of the metric.

        This insight highlights when the value of a metric for a given time range is higher or lower than the expected range
        based on historic observations of the metric.
        """
    },
    'newtrend': {
        'name': 'New Trend Detected',
        'description': """Shows new trends that vary significantly from the current trend. This insight communicates the
        rate of change, direction, and fluctuations for the metric value
        """
    },
    'currenttrend': {
        'name': 'Current Trend',
        'description': """The current trend of a metric. For instance, that overall sales are tending to increase by
        10% year over year
        """
    }
}

