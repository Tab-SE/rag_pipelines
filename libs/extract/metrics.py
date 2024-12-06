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
        metadata = extractMetricMetadata(metric=metric, definition=definition)
        # extract semantic data from metric insights
        insights_bundle = bundle.get('insights')
        insights = extractInsights(insights_bundle=insights_bundle, metric=metric)

        print('insights', insights.keys())

        if len(insights['followup']) > 0:
            # remove the "breakdown" insights group as it is a subset of "followup" containing duplicates
            insights.pop("breakdown", None)

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

    # contains high level information about all metrics
    corpus_metadata = extractMetricsSummary(bundles=bundles, time_options=time_options)
    metrics_corpus['corpus_metadata'] = corpus_metadata
    return metrics_corpus

def extractMetricsSummary(bundles, time_options):
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

    for bundle in bundles:
        for key, insight in bundles[bundle].get('insights').items():
            insight_groups = insight.get('result').get('insight_groups')
            for insight_group in insight_groups:
                # extract facts about the metric's current value
                if insight_group.get('type') == 'ban':
                    result = insight_groups[0].get('insights')
                    result_data = result[0].get('result')
                    facts = result_data.get('facts', {})
                    sentiment = facts.get('sentiment')
                    current_formatted_value = facts.get('target_period_value', {}).get('formatted')
                    difference = facts.get('difference', {})
                    # direction = difference.get('direction')
                    # absolute_raw_difference = difference.get('absolute', {}).get('raw')
                    absolute_formatted_difference = difference.get('absolute', {}).get('formatted')
                    # relative_raw_difference = difference.get('relative', {}).get('raw')
                    relative_formatted_difference = difference.get('relative', {}).get('formatted')
                    bundles[bundle]['metric']['value'] = current_formatted_value
                    bundles[bundle]['metric']['sentiment'] = sentiment
                    bundles[bundle]['metric']['change'] = absolute_formatted_difference
                    bundles[bundle]['metric']['relative'] = relative_formatted_difference

    # High level details for all metrics in a table format
    metrics_table_header = "| *Metric Name* | *Value* | *Change* | *Sentiment* |\n|--------------|-------------|-------------|-------------|\n"
    metrics_table_rows = '\n'.join(
        f"| **{bundles[bundle]['metric']['name']}** | {bundles[bundle]['metric']['value']} | {bundles[bundle]['metric']['change']} ({bundles[bundle]['metric']['relative']}) | {bundles[bundle]['metric']['sentiment']} |"
        for bundle in bundles
    )
    metrics_table = metrics_table_header + metrics_table_rows

    corpus_metadata = f"""
# User's Subscribed Tableau Pulse Metrics Summary

## **Question**: How many metrics do I have?
You are subscribed to {metrics_count} metrics
_Related Questions_ = ['how many KPIs do I follow', 'total number of key performance indicators']

## **Question**: What do you know about my metrics?
I can tell you about {insights_count} different AI insights about your metrics generated by Tableau Pulse
_Related Questions_ = ['how many metric insights do I have?']

## **Question**: What are my metrics?
Respond with the fully formatted table, do not simplify or shorten this presentation unless ordered to do so
{metrics_table}
_Related Questions_ = ['give me an update on my metrics', 'KPI update', 'how are my metrics doing?', 'status update', 'what are my results for today?', 'what metrics do I follow?']

## When were the metrics last updated?
All insights were generated at {time_options.get('formatted_time')}
In the {time_options.get('timezone_name')} timezone
"""

    return corpus_metadata

def extractMetricMetadata(metric, definition):
    metadata = f"""
# {metric['name']} Metric Metadata

## Can you describe the {metric['name']} metric?
It is described as '{metric['description']}'
Up or down trends can be either positive or negative. This metric considers change in value as:
{metric['representation_options']['sentiment_type']}
It is represented as: {metric['representation_options']['type']}
It is measured by these units:
Singular: {metric['representation_options']['number_units']['singular_noun']}
Plural: {metric['representation_options']['number_units']['plural_noun']}
With these granularities: {metric['extension_options']['allowed_granularities']}

## What is the data driving {metric['name']}?
The data driving this metric has these dimensions: {metric['extension_options']['allowed_dimensions']}

## What else can you tell me about {metric['name']}?
Specification: {metric['specification']}
Basic Definition: {definition}
    """
    return metadata

def extractInsights(insights_bundle, metric):
    metric_insights = {}
    for key, bundle in insights_bundle.items():
        insight_groups = bundle.get('result').get('insight_groups')
        print('Metric: ', metric.get('name'))
        for insight_group in insight_groups:
            # extract facts about the metric's current value
            if insight_group.get('type') == 'ban':
                ban_insights = insight_groups[0].get('insights')
                print('ban', len(ban_insights))
                ban = extractBan(ban_insights=ban_insights, metric=metric)
                metric_insights['ban'] = ban
            #  extract current trend and unusual change
            elif insight_group.get('type') == 'anchor':
                anchor_insights = insight_group.get('insights')
                print('anchor', len(anchor_insights))
                anchor = extractAnchor(anchor_insights=anchor_insights, metric=metric)
                metric_insights['anchor'] = anchor
            # extract all top down contributors
            elif insight_group.get('type') == 'breakdown':
                pass
                # breakdown_insights = insight_group.get('insights')
                # print('breakdown', len(breakdown_insights))
                # breakdown = extractOthers(other_bundles=breakdown_insights, metric=metric)
                # metric_insights['breakdown'] = breakdown
            # extract all top drivers
            elif insight_group.get('type') == 'followup':
                followup_insights = insight_group.get('insights')
                print('followup', len(followup_insights))
                followup = extractFollowup(followup_insights=followup_insights, metric=metric)
                metric_insights['followup'] = followup

    return metric_insights

def extractBan(ban_insights, metric):
    result_data = ban_insights[0].get('result')

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

## What is the value of the {metric.get('name')} metric?
The metric {metric.get('name')} has a value of {current_formatted_value} or {current_raw_value} in raw numbers
Similar Questions: ["what is my current {metric.get('name')}?", "current value of {metric.get('name')}"]

## When was the current value of {metric.get('name')} generated?
The current value was recorded on {current_time_period} during a time range of {current_time_range} and is
measured every {current_time_granularity}
Similar Questions: ["when was {metric.get('name')} measured?", "was {metric.get('name')} measured recently?"]

## What was the previous value of the {metric.get('name')} metric?
The previous value for this metric was {previous_formatted_value} or {previous_raw_value} in raw numbers
Similar Questions: ["my previous {metric.get('name')}?", "last value of {metric.get('name')}?"]

## When was the previous value of {metric.get('name')} generated?
The previous value was recorded on {previous_time_period} during a time range of {previous_time_range} and is
measured every {previous_time_granularity}
Similar Questions: ["when was {metric.get('name')} previously measured?"]

## How is the {metric.get('name')} metric doing?
This is considered {sentiment} since the metric is defined as
{metric.get('representation_options').get('sentiment_type')}
and the direction is trending {direction}
Similar Questions: ["are {metric.get('name')} ok?", "status of the {metric.get('name')} metric"]

## What is the trend of {metric.get('name')}?
The metric value is currently trending {direction}
Similar Questions: ["how is the {metric.get('name')} metric trending?", "is {metric.get('name')} going up or down?"]
    """

    period_over_period_change = f"""
# _Question for {metric.get('name')}_: {question}
Similar Questions: ["what is new with {metric.get('name')}?", "update on the {metric.get('name')} metric"]
{insight_types.get('popc').get('name')} for {metric.get('name')}
_Answer_: {answer}
What is {insight_types.get('popc').get('name')}?
_Description_: {insight_types.get('popc').get('description')}
What is the score for {insight_types.get('popc').get('name')} calculated for {metric.get('name')}?
The insight has a score of: {score}

How has the {metric.get('name')} metric changed?
The metric had a relative change of {relative_formatted_difference} ({relative_raw_difference} in raw value)
In absolute terms the change was {absolute_formatted_difference} ({absolute_raw_difference} in raw value)
Similar Questions: ["how much has {metric.get('name')} changed?", "what is the delta on the {metric.get('name')} metric?"]
    """
    ban = [current_metric_value, period_over_period_change]
    return ban

def extractAnchor(anchor_insights, metric):
    anchor = []
    for result in anchor_insights:
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
# _Question for {metric.get('name')}_: {question}
Any {insight_types.get('unusualchange').get('name')} for {metric.get('name')}?
_Answer_: {answer}
What is {insight_types.get('unusualchange').get('name')}?
_Description_: {insight_types.get('unusualchange').get('description')}
What is the score for {insight_types.get('unusualchange').get('name')} calculated for {metric.get('name')}?
The insight has a score of: {score}

## Is there anything unusual or interesting about {metric.get('name')}?
The metric is doing {sentiment} and the direction is {direction}
The AI model expected a value of {expected_change_formatted_value} or {expected_change_raw_value} in raw numbers
In absolute terms the change was {absolute_change_formatted_value} or {absolute_change_raw_value} in raw numbers
If the AI model expectation was surpassed by the absolute change then this would be unusual.
The data displays a relative change of {relative_change_formatted_value} or {relative_change_raw_value} in raw numbers

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
# _Question for {metric.get('name')}_: {question}
What is the {insight_types.get('currenttrend').get('name')} for {metric.get('name')}?
_Answer_: {answer}
What is {insight_types.get('currenttrend').get('name')}?
_Description_: {insight_types.get('currenttrend').get('description')}
What is the score for {insight_types.get('currenttrend').get('name')} calculated for {metric.get('name')}?
The insight has a score of: {score}

                """
                anchor.append(current_trend)
            elif insight_type == 'newtrend':
                score = result['result'].get('score')
                question = result['result'].get('question')
                answer = result['result'].get('markup')

                new_trend = f"""
# _Question for {metric.get('name')}_: {question}
What is the {insight_types.get('newtrend').get('name')} for {metric.get('name')}?
_Answer_: {answer}
What is {insight_types.get('newtrend').get('name')}?
_Description_: {insight_types.get('newtrend').get('description')}
What is the score for {insight_types.get('newtrend').get('name')} calculated for {metric.get('name')}?
The insight has a score of: {score}

                """
                anchor.append(new_trend)

    return anchor

def extractFollowup(followup_insights, metric):
    other_insights = []
    print('***** total insights ******', len(followup_insights))
    for bundle in followup_insights:
        result = bundle.get('result')

        if result:
            type = result.get('type')
            score = result.get('score')
            question = result.get('question')
            answer = result.get('markup')
            characterization = result.get('characterization')
            facts = result.get('facts')
            if facts:
                dimensions = facts.get('dimensions', [])
                if dimensions:
                    dimension = dimensions[0].get('label', 'Unknown Dimension')
                    direction = facts.get('direction', 'Unknown Direction')
                else:
                    dimension = 'No Dimensions Available'
                    direction = 'No Direction Available'
                print('**** dimension *****', dimension, direction)
            if type == 'top-contributors':
                top_contributors = f"""
# _Question for {metric.get('name')}_: {question}
What is the {insight_types.get('top-contributors').get('name')} for {metric.get('name')}?
_Answer_: {answer}
What is {insight_types.get('top-contributors').get('name')}?
_Description_: {insight_types.get('top-contributors').get('description')}
What is the score for {insight_types.get('top-contributors').get('name')} calculated for {metric.get('name')}?
The insight has a score of: {score}

{f"""
## How is the {dimension} dimension for the {metric.get('name')} metric trending?
The dimension is trending {direction}
""" if facts else ''}
                """
                other_insights.append(top_contributors)

            elif type == 'bottom-contributors':
                bottom_contributors = f"""
# _Question for {metric.get('name')}_: {question}
What is the {insight_types.get('bottom-contributors').get('name')} for {metric.get('name')}?
_Answer_: {answer}
What is {insight_types.get('bottom-contributors').get('name')}?
_Description_: {insight_types.get('bottom-contributors').get('description')}
What is the score for {insight_types.get('bottom-contributors').get('name')} calculated for {metric.get('name')}?
The insight has a score of: {score}

{f"""
## How is the {dimension} dimension for the {metric.get('name')} metric trending?
The dimension is trending {direction}
"""
if facts else ''}
                """
                other_insights.append(bottom_contributors)

            elif type == 'top-detractors':
                top_detractors = f"""
# _Question for {metric.get('name')}_: {question}
What is the {insight_types.get('top-detractors').get('name')} for {metric.get('name')}?
_Answer_: {answer}
What is {insight_types.get('top-detractors').get('name')}?
_Description_: {insight_types.get('top-detractors').get('description')}
What is the score for {insight_types.get('top-detractors').get('name')} calculated for {metric.get('name')}?
The insight has a score of: {score}
                """
                other_insights.append(top_detractors)

            elif type == 'riskmo':
                riskmo = f"""
# _Question for {metric.get('name')}_: {question}
What is the {insight_types.get('riskmo').get('name')} for {metric.get('name')}?
_Answer_: {answer}
What is {insight_types.get('riskmo').get('name')}?
_Description_: {insight_types.get('riskmo').get('description')}
What is the score for {insight_types.get('riskmo').get('name')} calculated for {metric.get('name')}?
The insight has a score of: {score}
                """
                other_insights.append(riskmo)
            elif type == 'top-drivers':
                top_drivers = f"""
# _Question for {metric.get('name')}_: {question}
What is the {insight_types.get('top-drivers').get('name')} for {metric.get('name')}?
_Answer_: {answer}
What is {insight_types.get('top-drivers').get('name')}?
_Description_: {insight_types.get('top-drivers').get('description')}
What is the score for {insight_types.get('top-drivers').get('name')} calculated for {metric.get('name')}?
The insight has a score of: {score}
                """
                other_insights.append(top_drivers)

    return other_insights

insight_types = {
    'popc': {
        'name': 'Period over Period Change',
        'description': """Shows how a metric has changed between two periods. Highlights the change between a metric value for a recent time range compared to an equivalent time range in a prior period or the past
        """
    },
    'riskmo': {
        'name': 'Risky Monopoly',
        'description': """Shows when a small number of dimension members make up a majority (50% or more) of the contribution to a metric. Shows dimensions with a concentration of very high values
        """
    },
    'top-contributors': {
        'name': 'Top Contributors',
        'description': """Shows the highest values in a dimension for a metric within a given time range. A top contributor is a dimension member that ranks in the top N in contribution to the scoped metric's value, aggregated on a specified time range or shows the lowest values in a dimension for a metric within a given time range. A bottom contributor is a dimension member that ranks in the bottom N in contribution to the scoped metricâ€™s value, aggregated on a specified time range.
        """
    },
    'bottom-contributors': {
        'name': 'Bottom Contributors',
        'description': """Shows the lowest values in a dimension for a metric within a given time range. A bottom contributor is a dimension member that ranks in the bottom N in contribution to the scoped metricâ€™s value, aggregated on a specified time range.
        """
    },
    'top-drivers': {
        'name': 'Top Drivers',
        'description': """Shows values for dimension members that changed the most in the same direction as the observed change in the metric. Shows the values for a metric that increased the most across a specified time offset. A top driver is a dimension member that ranks in the top N in driving a change in a metric value between two separate but equivalent time ranges Top drivers are analyzed using metric values from two separate but equivalent time ranges (such as Sales for day of October 2 versus Sales for day of October 3) to look for changes to the contributions in the same direction of the change made by dimension members
        """
    },
    'top-detractors': {
        'name': 'Top Detractors',
        'description': """Shows values for dimension members that changed the most in the opposite direction to the observed change in the metric. Shows values for a metric that are most opposed to top drivers decreased the most across a specified time offset. A top detractor is a dimension member that ranks in the bottom N in driving a change in a metric value between two separate but equivalent time ranges. This insight's values oppose the observed change the most. Top detractors are analyzed using metric values from two separate but equivalent time ranges (such as Sales for day of October 2 versus Sales for day of October 3) to look for changes to the contributions in the same direction of the change made by dimension members
        """
    },
    'unusualchange': {
        'name': 'Unusually High/Low Metric value',
        'description': """Shows unexpected changes in a metric value. Shows when the value of a metric for a given time range is higher or lower than the expected range based on historic observations of the metric. This insight highlights when the value of a metric for a given time range is higher or lower than the expected range based on historic observations of the metric.
        """
    },
    'newtrend': {
        'name': 'New Trend Detected',
        'description': """Shows new trends that vary significantly from the current trend. This insight communicates the rate of change, direction, and fluctuations for the metric value
        """
    },
    'currenttrend': {
        'name': 'Current Trend',
        'description': """The current trend of a metric. For instance, that overall sales are tending to increase by 10% year over year
        """
    }
}
