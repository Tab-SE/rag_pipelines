from jsonpath_ng import jsonpath, parse

def bundles(bundles):
    corpus = {}
    # extract only necessary metadata, Q&A, markup, vizzes, facts & other semantic features
    for key, bundle in bundles.items():
        metric = bundle.get('metric')
        time_options = bundle.get('time_options')
        definition = metric.get('definition') if metric else None

        # remove 'viz_state_specification' if exists
        definition.pop('viz_state_specification', None)
        # creating a metadata string
        metadata = extractMetadata(metric=metric, definition=definition, time_options=time_options)
        insights_bundle = bundle.get('insights')
        insights = extractInsights(insights_bundle=insights_bundle, metric=metric, time_options=time_options)
        # payload containing document strings for loading
        documents = {
            'metadata': metadata,
            'insights': insights,
        }
        #
        #
        #
        #
        # print(documents['metadata'])
        print(documents['insights'])
        metric_name = metric.get('name')
        # to identify metrics with the same name but different definitions
        index = f'{key}_{metric_name.replace(" ", "_")}'
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
    insights = []
    for key, bundle in insights_bundle.items():
        metric_insights = {}
        insight_groups = bundle.get('result').get('insight_groups')
        for insight_group in insight_groups:
            # extract facts about the metric's current value
            if insight_group.get('type') == 'ban':
                result = insight_groups[0].get('insights')
                print('ban', len(result))
                ban = extractBan(result=result, metric=metric, time_options=time_options)
                metric_insights['ban'] = ban
            #  extract current trend and unusual change
            elif insight_group.get('type') == 'anchor':
                insights_array = insight_group.get('insights')
                print('anchor', len(insights_array))
                anchor = extractAnchor(insights_array=insights_array, metric=metric, time_options=time_options)
                metric_insights['anchor'] = anchor
            # extract all top down contributors
            elif insight_group.get('type') == 'breakdown':
                breakdown_bundles = insight_group.get('insights')
                print('breakdown', len(breakdown_bundles))
                breakdown = extractOthers(other_bundles=breakdown_bundles, metric=metric, time_options=time_options)
                metric_insights['breakdown'] = breakdown
            # extract all top drivers
            elif insight_group.get('type') == 'followup':
                followup_bundles = insight_group.get('insights')
                print('followup', len(followup_bundles))
                followup = extractOthers(other_bundles=followup_bundles, metric=metric, time_options=time_options)
                metric_insights['followup'] = followup

        insights.append(metric_insights)

    return insights

def extractBan(result, metric, time_options):
    result_data = result[0].get('result')

    score = result_data.get('score')
    question = result_data.get('question')
    answer = result_data.get('markup')

    facts = result_data.get('facts', {})

    sentiment = facts.get('sentiment')
    current_raw_value = facts.get('target_period_value', {}).get('raw')
    current_formatted_value = facts.get('target_period_value', {}).get('formatted')
    previous_raw_value = facts.get('comparison_period_value', {}).get('raw')
    previous_formatted_value = facts.get('comparison_period_value', {}).get('formatted')

    target_time_period = facts.get('target_time_period', {})
    current_time_period = target_time_period.get('label')
    current_time_range = target_time_period.get('range')
    current_time_granularity = target_time_period.get('granularity')

    comparison_time_period = facts.get('comparison_time_period', {})
    previous_time_period = comparison_time_period.get('label')
    previous_time_range = comparison_time_period.get('range')
    previous_time_granularity = comparison_time_period.get('granularity')

    difference = facts.get('difference', {})
    direction = difference.get('direction')
    absolute_raw_difference = difference.get('absolute', {}).get('raw')
    absolute_formatted_difference = difference.get('absolute', {}).get('formatted')
    relative_raw_difference = difference.get('relative', {}).get('raw')
    relative_formatted_difference = difference.get('relative', {}).get('formatted')


    current_metric_value = f"""
    The metric {metric.get('name')} has a value of {current_formatted_value} ({current_raw_value} in raw value)
    The current value was recorded on {current_time_period} during a time range of {current_time_range} and is
    measured every {current_time_granularity}

    The previous value for this metric was {previous_formatted_value} ({previous_raw_value} in previous raw value)
    The previous value was recorded on {previous_time_period} during a time range of {previous_time_range} and is
    measured every {previous_time_granularity}

    Therefore the metric value is currently trending {direction}. This is considered {sentiment} since the metric
    is defined as {metric.get('representation_options').get('sentiment_type')}

    This Tableau Pulse AI generated insight was created at {time_options.get('formatted_time')}
    In the {time_options.get('timezone_name')} timezone
    """

    period_over_period_change = f"""
    Metric: {metric.get('name')}
    Insight Type: {insight_types.get('popc').get('name')}
    Description: {insight_types.get('popc').get('description')}
    The insight has a score of: {score}

    Question: {question}
    Answer: {answer}

    The metric had a relative change of {relative_formatted_difference} ({relative_raw_difference} in raw value)
    In absolute terms the change was {absolute_formatted_difference} ({absolute_raw_difference} in raw value)

    This Tableau Pulse AI generated insight was created at {time_options.get('formatted_time')}
    In the {time_options.get('timezone_name')} timezone
    """
    ban = {
        'current_metric_value': current_metric_value,
        'period_over_period_change': period_over_period_change
    }
    return ban

def extractAnchor(insights_array, metric, time_options):
    anchor = {}
    for result in insights_array:
        insight_type = result.get('result').get('type')
        if insight_type == 'unusualchange':
            score = result['result'].get('score')
            question = result['result'].get('question')
            answer = result['result'].get('markup')
            characterization = result['result'].get('characterization')
            facts = result['result'].get('facts')
            sentiment = facts.get('sentiment')
            increment_raw_value = facts.get('value', {}).get('raw')
            increment_formatted_value = facts.get('value', {}).get('formatted')
            absolute_change_raw_value = facts.get('value_change', {}).get('absolute', {}).get('raw')
            absolute_change_formatted_value = facts.get('value_change', {}).get('absolute', {}).get('formatted')
            relative_change_raw_value = facts.get('value_change', {}).get('relative', {}).get('raw')
            relative_change_formatted_value = facts.get('value_change', {}).get('relative', {}).get('formatted')
            expected_change_raw_value = facts.get('expected_value_change', {}).get('raw')
            expected_change_formatted_value = facts.get('expected_value_change', {}).get('formatted')
            period_range = facts.get('last_complete_period', {}).get('range')
            period_label = facts.get('last_complete_period', {}).get('label')
            period_granularity = facts.get('last_complete_period', {}).get('granularity')
            period_start = facts.get('last_complete_period', {}).get('start_timestamp')
            period_end = facts.get('last_complete_period', {}).get('end_timestamp')
            direction = facts.get('difference', {}).get('direction')

            unusual_change = f"""
            Metric: {metric['name']}
            Insight Type: {insight_types.get('unusualchange').get('name')}
            Description: {insight_types.get('unusualchange').get('description')}
            The insight has a score of: {score}
            Change Sentiment: {sentiment}
            Period: {period_label}

            Question: {question}
            Answer: {answer}

            Short term change was monitored throughout {period_range} which is currently trending {direction}
            Observation ran between {period_start} and {period_end} with a granularity of {period_granularity}
            The value during the observation period is {increment_formatted_value} ({increment_raw_value} in raw value)

            The AI model expected a value of {expected_change_formatted_value} ({expected_change_raw_value} in raw value)

            The data displays a relative change of {relative_change_formatted_value} ({relative_change_raw_value} in raw value)
            In absolute terms the change was {absolute_change_formatted_value} ({absolute_change_raw_value} in raw value)

            This Tableau Pulse AI generated insight was created at {time_options.get('formatted_time')}
            In the {time_options.get('timezone_name')} timezone
            """
            anchor['unusual_change'] = unusual_change
        elif insight_type == 'currenttrend':
            score = result['result'].get('score')
            question = result['result'].get('question')
            answer = result['result'].get('markup')

            current_trend = f"""
            Metric: {metric['name']}
            Insight Type: {insight_types.get('currenttrend').get('name')}
            Description: {insight_types.get('currenttrend').get('description')}
            The insight has a score of: {score}

            Question: {question}
            Answer: {answer}

            This Tableau Pulse AI generated insight was created at {time_options.get('formatted_time')}
            In the {time_options.get('timezone_name')} timezone
            """
            anchor['current_trend'] = current_trend
        elif insight_type == 'newtrend':
            score = result['result'].get('score')
            question = result['result'].get('question')
            answer = result['result'].get('markup')

            new_trend = f"""
            Metric: {metric['name']}
            Insight Type: {insight_types.get('newtrend').get('name')}
            Description: {insight_types.get('newtrend').get('description')}
            The insight has a score of: {score}

            Question: {question}
            Answer: {answer}

            This Tableau Pulse AI generated insight was created at {time_options.get('formatted_time')}
            In the {time_options.get('timezone_name')} timezone
            """
            anchor['new_trend'] = new_trend

    return anchor

def extractOthers(other_bundles, metric, time_options):
    other_insights = [];
    for bundle in other_bundles:
        result = bundle.get('result')
        type = result.get('type')
        score = result.get('score')
        question = result.get('question')
        answer = result.get('markup')
        characterization = result.get('characterization')
        facts = result.get('facts')
        if facts:
            dimension = facts.get('dimensions')[0].get('label')
            direction = facts.get('direction')
        if type == 'top-contributors':
            top_contributors = f"""
            Metric: {metric['name']}
            Insight Type: {insight_types.get('top-contributors').get('name')}
            Description: {insight_types.get('top-contributors').get('description')}
            The insight has a score of: {score}
            {f"""The dimension is {dimension} and is trending {direction}""" if facts else ''}

            Question: {question}
            Answer: {answer}

            This Tableau Pulse AI generated insight was created at {time_options.get('formatted_time')}
            In the {time_options.get('timezone_name')} timezone
            """
            other_insights.append(top_contributors)
        elif type == 'bottom-contributors':
            bottom_contributors = f"""
            Metric: {metric['name']}
            Insight Type: {insight_types.get('bottom-contributors').get('name')}
            Description: {insight_types.get('bottom-contributors').get('description')}
            The insight has a score of: {score}
            {f"""The dimension is {dimension} and is trending {direction}""" if facts else ''}

            Question: {question}
            Answer: {answer}

            This Tableau Pulse AI generated insight was created at {time_options.get('formatted_time')}
            In the {time_options.get('timezone_name')} timezone
            """
            other_insights.append(bottom_contributors)
        elif type == 'top-detractors':
            top_detractors = f"""
            Metric: {metric['name']}
            Insight Type: {insight_types.get('top-detractors').get('name')}
            Description: {insight_types.get('top-detractors').get('description')}
            The insight has a score of: {score}

            Question: {question}
            Answer: {answer}

            This Tableau Pulse AI generated insight was created at {time_options.get('formatted_time')}
            In the {time_options.get('timezone_name')} timezone
            """
            other_insights.append(top_detractors)
        elif type == 'riskmo':
            riskmo = f"""
            Metric: {metric['name']}
            Insight Type: {insight_types.get('riskmo').get('name')}
            Description: {insight_types.get('riskmo').get('description')}
            The insight has a score of: {score}

            Question: {question}
            Answer: {answer}

            This Tableau Pulse AI generated insight was created at {time_options.get('formatted_time')}
            In the {time_options.get('timezone_name')} timezone
            """
            other_insights.append(riskmo)
        elif type == 'top-drivers':
            top_drivers = f"""
            Metric: {metric['name']}
            Insight Type: {insight_types.get('top-drivers').get('name')}
            Description: {insight_types.get('top-drivers').get('description')}
            The insight has a score of: {score}

            Question: {question}
            Answer: {answer}

            This Tableau Pulse AI generated insight was created at {time_options.get('formatted_time')}
            In the {time_options.get('timezone_name')} timezone
            """
            other_insights.append(top_drivers)

    return other_insights

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

