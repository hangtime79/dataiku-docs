def add_metrics_probes_col_stats(probes, aggregation, column):
    """
    Add a metrics of column statistics to probes
    :param probes: the list of existing probes
    :param aggregation: which aggregation is used
    :param column: the column dataset to use

     Usage example:

    .. code-block:: python

        settings: DSSDatasetSettings = dataset.get_settings()
        metrics: ComputedMetrics = settings.get_raw()['metrics']
        add_metrics_probes_col_stats(metrics['probes'], 'MIN', 'purchase_amount')

    """

    types_index = next((index for (index, d) in enumerate(probes) if d["type"] == 'col_stats'), None)
    if types_index:
        types_value = probes[types_index]
        existing_aggregation = types_value['configuration']['aggregates']
        to_append = {'aggregated': aggregation, 'column': column}
        if to_append not in existing_aggregation:
            existing_aggregation.append(to_append)
    else:
        probes.append({'computeOnBuildMode': 'NO',
                       'configuration': {'aggregates': [{'aggregated': aggregation,
                                                         'column': column}
                                                        ]},
                       'enabled': True,
                       'meta': {'level': 2, 'name': 'Columns statistics'},
                       'type': 'col_stats'})


def add_displayed_state_to_metrics(displayed_state, type_to_add, function_to_add, column=""):
    """
    Add to the metrics used a new one
    :param displayed_state: the previous state
    :param type_to_add: which kind of metrics
    :param function_to_add: function that been used
    :param column: column if any

    Usage example:
    .. code-block:: python

        settings: DSSDatasetSettings = dataset.get_settings()
        metrics: ComputedMetrics = settings.get_raw()['metrics']
        add_displayed_state_to_metrics(metrics['displayedState'], 'col_stats', 'MIN', 'purchase_amount')

    """

    line_to_add = type_to_add + ':' + function_to_add
    if column:
        line_to_add += ':' + column
    if line_to_add not in displayed_state['metrics']:
        displayed_state['metrics'].append(line_to_add)


def add_metrics_checks_numeric_range(checks, label, which, parameters):
    """
    Add a metric if only it doesn't exist
    :param checks: Existing checks
    :param label: Label for the check
    :param which: Probe for the check
    :param parameters: Operation to check
    
    Usage example:
    .. code-block:: python

        settings: DSSDatasetSettings = dataset.get_settings()
        checks = settings.get_raw()['metricsChecks']
        CHECK_RECORDS_NAME = 'Number of records should be greater than 100'
        add_metrics_checks_numeric_range(checks, CHECK_RECORDS_NAME, 'records:COUNT_RECORDS',
                                         [('minimum', 100)])

    """

    is_already_present = next((check for check in checks['checks'] if check['type'] == 'numericRange' and
                               check['metricId'] == which), None)
    if not is_already_present:
        new_metric = {
            'computeOnBuildMode': 'PARTITION',
            'meta': {
                'label': label,
                'name': 'Value in range'
            },
            'metricId': which,
            'maximum': 0.0,
            'maximumEnabled': False,
            'minimum': 0.0,
            'minimumEnabled': False,
            'softMaximum': 0.0,
            'softMaximumEnabled': False,
            'softMinimum': 0.0,
            'softMinimumEnabled': False,
            'type': 'numericRange'
        }
        for parameter in parameters:
            new_metric[parameter[0]] = parameter[1]
            new_metric[parameter[0] + 'Enabled'] = True
        checks['checks'].append(new_metric)


def set_check_visible(checks, label):
    """
    Add a defined checks to the displayed state (so the user can see it in the GUI)
    :param checks: the metricsChecks part of the dataset settings
    :param label: label to use
    :return:
    
    Usage example:
    .. code-block:: python

        settings: DSSDatasetSettings = dataset.get_settings()
        CHECK_RECORDS_NAME = 'Number of records should be greater than 100'
        checks = settings.get_raw()['metricsChecks']
        set_check_visible(checks, CHECK_RECORDS_NAME)

    """

    displayed_state = checks['displayedState']
    displayed = displayed_state['checks']
    if label not in displayed:
        displayed.append(label)


def get_metrics(dataset):
    """
    Compute and return all used metrics (only id) for a particular dataset
    :param dataset: the dataset

    Usage example:
    .. code-block:: python

        last_metrics = dataset.get_last_metric_values()
        metrics = get_metrics(dataset)
        for metric in metrics:
            metric_value = last_metrics.get_metric_by_id(metric)
            if metric_value and metric_value['lastValues']:
                result[metric] = {
                    'initialValue': metric_value['lastValues'][0]['value']
                }
    """
    dataset.compute_metrics()
    last_metrics = dataset.get_last_metric_values().get_raw()
    return_list = list()
    id_metrics = list(map((lambda metric: metric['metric']['id']),
                          filter(lambda metric: metric['displayedAsMetric'], last_metrics['metrics'])))
    return_list.extend(id_metrics)
    return return_list


def get_checks_used(settings):
    """
    Get the list of all used checks for a dataset
    :param settings: the settings of the dataset
    :return: the list of all checks used for this dataset
    """
    return list(map((lambda check: 'check:CHECK:'+check), settings['metricsChecks']['displayedState']['checks']))

def get_checks(dataset):
    """
    Compute and return all used checks (only id) for a particular dataset
    :param dataset: the dataset

    Usage example:
    .. code-block:: python

        last_metrics = dataset.get_last_metric_values()
        checks = get_checks(dataset)
        for check in checks:
            check_value = last_metrics.get_metric_by_id(metric)
            if check_value and check_value['lastValues']:
                result[metric] = {
                    'initialValue': metric_value['lastValues'][0]['value']
                }
    """
    dataset.compute_metrics()
    dataset.run_checks()
    return_list = list()
    return_list.extend(get_checks_used(dataset.get_settings().get_raw()))
    return return_list

