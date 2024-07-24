def bundles(bundles):
    # full corpus of metrics data
    metrics_corpus = {
        'corpus_metadata': '',
        'corpus': {}
    }
    # extract only necessary metadata, Q&A, markup, vizzes, facts & other semantic features
    for key, bundle in bundles.items():
        metric = bundle.get('metric')
        time_options = bundle.get('time_options')
        definition = metric.get('definition') if metric else None
        # remove 'viz_state_specification' if exists
        definition.pop('viz_state_specification', None)
        # creating a metadata string to describe each metric
        metadata = extractMetadata(metric=metric, definition=definition, time_options=time_options)
        # extract semantic data from metric insights
        insights_bundle = bundle.get('insights')
        insights = extractInsights(insights_bundle=insights_bundle, metric=metric, time_options=time_options)
        # set of documents for each metric
        documents = {
            'metadata': metadata,
            'insights': insights,
        }
        metric_name = metric.get('name')
        # metrics index to distinguish metrics with the same name
        index = f'{key}_{metric_name.replace(" ", "_")}'
        # docs in corpus are indentified by {index}
        metrics_corpus['corpus'][index] = documents

    # contains high level information about all metrics and metrics in general
    corpus_metadata = extractCorpusMetadata(bundles=bundles, time_options=time_options)
    metrics_corpus['corpus_metadata'] = corpus_metadata
    return metrics_corpus

def extractCorpusMetadata(bundles, time_options):
    metrics_count = 0
    insights_count = 0
    # extract only necessary metadata, Q&A, markup, vizzes, facts & other semantic features
    for key, bundle in bundles.items():
        metrics_count = metrics_count + 1
        insights_groups = bundle.get('insights')['bundle_response']['result']['insight_groups']
        for insight_group in insights_groups:
            insights_list = insight_group['insights']
            insights_count = insights_count + len(insights_list)

    # describe all insight types
    types_list = '\n'.join(
        f'{index}. {insight_types[type]['name']}: {insight_types[type]['description']} \n'
        for index, type in enumerate(insight_types)
    )
    # high level details for all metrics
    metrics_list = '\n'.join(
        f"""{index}. {bundles[bundle]['metric']['name']}: {bundles[bundle]['metric']['description']} \n
        """
        for index, bundle in enumerate(bundles)
    )

    corpus_metadata = f"""
    # Metrics & Insights

    ## How many metrics do I have?
    ## How many KPIs do I follow?
    You are subscribed to {metrics_count} metrics

    ## How many insights do I have?
    ## How many AI generated insights do you have?
    You received {insights_count} AI insights from Tableau Pulse generated
    from the metrics you follow

    ## What are my metrics?
    ## What KPIs do I have?
    ## Which indicators do I follow?
    This is the list of user subscribed metrics:
    {metrics_list}

    ## When were the metrics last updated?
    ## When were the insights last updated?
    ## When was the data last updated?
    All insights were generated at {time_options.get('formatted_time')}
    In the {time_options.get('timezone_name')} timezone
    """

    return corpus_metadata

def extractMetadata(metric, definition, time_options):
    metadata = f"""
    # Metric Summary

    ## What is {metric['name']}?
    ## Can you describe {metric['name']}?
    The metric name is {metric['name']}
    It is described as '{metric['description']}'
    This metric considers change in value as: {metric['representation_options']['sentiment_type']}

    ## Give me details about {metric['name']}
    ## What is {metric['name']} made of?
    It is represented as: {metric['representation_options']['type']}
    It is measured by these units:
    Singular: {metric['representation_options']['number_units']['singular_noun']}
    Plural: {metric['representation_options']['number_units']['plural_noun']}

    ## What is the data driving {metric['name']}?
    ## What are the dimensions used by {metric['name']}?
    The data driving this metric has these dimensions: {metric['extension_options']['allowed_dimensions']}
    ## What is the granularity of the data set for {metric['name']}?
    With these granularities: {metric['extension_options']['allowed_granularities']}

    ## What are the filters for {metric['name']}?
    ## What else can you tell me about {metric['name']}?
    Specification: {metric['specification']}
    Basic Definition: {definition}
    """
    return metadata

def extractInsights(insights_bundle, metric, time_options):
    metric_insights = {}
    for key, bundle in insights_bundle.items():
        insight_groups = bundle.get('result').get('insight_groups')
        print('Metric: ', metric.get('name'))
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

    return metric_insights

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
    # Current Value

    ## What is the current value of {metric.get('name')}?
    ## What is the value of {metric.get('name')}?
    The metric {metric.get('name')} has a value of {current_formatted_value} or {current_raw_value} in raw numbers
    ## When was the current value of {metric.get('name')} generated?
    The current value was recorded on {current_time_period} during a time range of {current_time_range} and is
    measured every {current_time_granularity}

    ## What was the previous value of {metric.get('name')}?
    The previous value for this metric was {previous_formatted_value} or {previous_raw_value} in raw numbers
    ## When was the previous value of {metric.get('name')} generated?
    The previous value was recorded on {previous_time_period} during a time range of {previous_time_range} and is
    measured every {previous_time_granularity}

    ## How are {metric.get('name')} doing?
    ## How do you feel about {metric.get('name')}?
    ## How do I know if {metric.get('name')} is doing well or doing poorly?
    This is considered {sentiment} since the metric is defined as
    {metric.get('representation_options').get('sentiment_type')}
    ## What is the trend of {metric.get('name')}?
    The metric value is currently trending {direction}.
    """

    period_over_period_change = f"""
    # {question}
    _Answer_: {answer}

    # {insight_types.get('popc').get('name')} for {metric.get('name')}

    ## What is {insight_types.get('popc').get('name')}?
    _Description_: {insight_types.get('popc').get('description')}

    ## What is the score for {insight_types.get('popc').get('name')} calculated for {metric.get('name')}?
    The insight has a score of: {score}

    ## How has {metric.get('name')} changed?
    ## How much has {metric.get('name')} changed?
    The metric had a relative change of {relative_formatted_difference} ({relative_raw_difference} in raw value)
    In absolute terms the change was {absolute_formatted_difference} ({absolute_raw_difference} in raw value)
    """
    ban = [current_metric_value, period_over_period_change]
    return ban

def extractAnchor(insights_array, metric, time_options):
    anchor = []
    for result in insights_array:
        if result.get('error'):
            print(result.get('error'))
            continue
        else:
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
                # {question}
                _Answer_: {answer}

                # {insight_types.get('unusualchange').get('name')} for {metric.get('name')}

                ## What is {insight_types.get('unusualchange').get('name')}?
                _Description_: {insight_types.get('unusualchange').get('description')}

                ## Any {insight_types.get('unusualchange').get('name')} for {metric.get('name')}?

                ## What is the score for {insight_types.get('unusualchange').get('name')} calculated for {metric.get('name')}?
                The insight has a score of: {score}

                ## Why is {metric.get('name')} unusual?
                ## Is there anything unusual or interesting about {metric.get('name')}?
                ## Any news about {metric.get('name')}?
                The metric is doing {sentiment} and the direction is {direction}
                The AI model expected a value of {expected_change_formatted_value} or {expected_change_raw_value} in raw numbers
                The data displays a relative change of {relative_change_formatted_value} or {relative_change_raw_value} in raw numbers
                In absolute terms the change was {absolute_change_formatted_value} or {absolute_change_raw_value} in raw numbers

                ## What is the period for unusual change?
                ## When was unusual change detected?
                {period_label}. Short term change was monitored throughout {period_range} which is currently trending {direction}
                Observation ran between {period_start} and {period_end} with a granularity of {period_granularity}
                The value during the observation period is {increment_formatted_value} ({increment_raw_value} in raw value)

                ## What is the score for {insight_types.get('unusualchange').get('name')} calculated for {metric.get('name')}?
                The insight has a score of: {score}
                """
                anchor.append(unusual_change)
            elif insight_type == 'currenttrend':
                score = result['result'].get('score')
                question = result['result'].get('question')
                answer = result['result'].get('markup')

                current_trend = f"""
                # {question}
                _Answer_: {answer}

                # {insight_types.get('currenttrend').get('name')} for {metric.get('name')}

                ## What is {insight_types.get('currenttrend').get('name')}?
                _Description_: {insight_types.get('currenttrend').get('description')}

                ## What is the {insight_types.get('currenttrend').get('name')} for {metric.get('name')}?

                ## What is the score for {insight_types.get('currenttrend').get('name')} calculated for {metric.get('name')}?
                The insight has a score of: {score}
                """
                anchor.append(current_trend)
            elif insight_type == 'newtrend':
                score = result['result'].get('score')
                question = result['result'].get('question')
                answer = result['result'].get('markup')

                new_trend = f"""
                # {question}
                _Answer_: {answer}

                # {insight_types.get('newtrend').get('name')} for {metric.get('name')}

                ## What is {insight_types.get('newtrend').get('name')}?
                _Description_: {insight_types.get('newtrend').get('description')}

                ## What is the {insight_types.get('newtrend').get('name')} for {metric.get('name')}?

                ## What is the score for {insight_types.get('newtrend').get('name')} calculated for {metric.get('name')}?
                The insight has a score of: {score}
                """
                anchor.append(new_trend)

    return anchor

def extractOthers(other_bundles, metric, time_options):
    other_insights = []
    for bundle in other_bundles:
        result = bundle.get('result')

        if result:
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
                # {question}
                _Answer_: {answer}

                # {insight_types.get('top-contributors').get('name')} for {metric.get('name')}

                ## What is {insight_types.get('top-contributors').get('name')}?
                _Description_: {insight_types.get('top-contributors').get('description')}

                ## What is the {insight_types.get('top-contributors').get('name')} for {metric.get('name')}?

                ## What is the score for {insight_types.get('top-contributors').get('name')} calculated for {metric.get('name')}?
                The insight has a score of: {score}


                {f"""## What is dimension?
                ## How is the dimension trending?
                The dimension is {dimension} and is trending {direction}
                """
                if facts else ''}
                """
                other_insights.append(top_contributors)
            elif type == 'bottom-contributors':
                bottom_contributors = f"""
                # {question}
                _Answer_: {answer}

                # {insight_types.get('bottom-contributors').get('name')} for {metric.get('name')}

                ## What is {insight_types.get('bottom-contributors').get('name')}?
                _Description_: {insight_types.get('bottom-contributors').get('description')}

                ## What is the {insight_types.get('bottom-contributors').get('name')} for {metric.get('name')}?

                ## What is the score for {insight_types.get('bottom-contributors').get('name')} calculated for {metric.get('name')}?
                The insight has a score of: {score}

                {f"""## What is dimension?
                ## How is the dimension trending?
                The dimension is {dimension} and is trending {direction}
                """
                if facts else ''}
                """
                other_insights.append(bottom_contributors)
            elif type == 'top-detractors':
                top_detractors = f"""
                # {question}
                _Answer_: {answer}

                # {insight_types.get('top-detractors').get('name')} for {metric.get('name')}

                ## What is {insight_types.get('top-detractors').get('name')}?
                _Description_: {insight_types.get('top-detractors').get('description')}

                ## What is the {insight_types.get('top-detractors').get('name')} for {metric.get('name')}?

                ## What is the score for {insight_types.get('top-detractors').get('name')} calculated for {metric.get('name')}?
                The insight has a score of: {score}
                """
                other_insights.append(top_detractors)
            elif type == 'riskmo':
                riskmo = f"""
                # {question}
                _Answer_: {answer}

                # {insight_types.get('riskmo').get('name')} for {metric.get('name')}

                ## What is {insight_types.get('riskmo').get('name')}?
                _Description_: {insight_types.get('riskmo').get('description')}

                ## What is the {insight_types.get('riskmo').get('name')} for {metric.get('name')}?

                ## What is the score for {insight_types.get('riskmo').get('name')} calculated for {metric.get('name')}?
                The insight has a score of: {score}
                """
                other_insights.append(riskmo)
            elif type == 'top-drivers':
                top_drivers = f"""
                # {question}
                _Answer_: {answer}

                # {insight_types.get('top-drivers').get('name')} for {metric.get('name')}

                ## What is {insight_types.get('top-drivers').get('name')}?
                _Description_: {insight_types.get('top-drivers').get('description')}

                ## What is the {insight_types.get('top-drivers').get('name')} for {metric.get('name')}?

                ## What is the score for {insight_types.get('top-drivers').get('name')} calculated for {metric.get('name')}?
                The insight has a score of: {score}
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
