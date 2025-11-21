(metrics)=

```{eval-rst}
..
  this code samples has been verified on DSS: 14.2.0-alpha3
  Date of check: 15/09/2025

  this code samples has been verified on DSS: 13.2.0
  Date of check: 03/10/2024
```

# Metrics and checks

:::{note}
There are two main parts related to handling of metrics and checks in Dataiku's Python APIs:

- {class}`dataiku.core.metrics.ComputedMetrics` in the `dataiku` package. It was initially designed for usage within DSS
- {class}`dataikuapi.dss.metrics.ComputedMetrics` in the `dataikuapi` package. It was initially designed for usage outside of DSS.

Both classes have fairly similar capabilities

For more details on the two packages, please see {doc}`index`
:::


## Add metric on a column

:::{literalinclude} examples/metrics/metrics.py
:pyobject: add_metrics_probes_col_stats
:::

```python
settings = dataset.get_settings()
metrics = settings.get_raw()['metrics']
add_metrics_probes_col_stats(metrics['probes'], 'MIN', 'purchase_amount')
```

## Make a defined metric visible
    
:::{literalinclude} examples/metrics/metrics.py
:pyobject: add_displayed_state_to_metrics
:::

```python
settings = dataset.get_settings()
metrics = settings.get_raw()['metrics']
add_displayed_state_to_metrics(metrics['displayedState'], 'col_stats', 'MIN', 'purchase_amount')
```

## Define a new numerical check

:::{literalinclude} examples/metrics/metrics.py
:pyobject: add_metrics_checks_numeric_range
:::

```python
setting = dataset.get_settings()
checks = settings.get_raw()['metricsChecks']
CHECK_RECORDS_NAME = 'Number of records should be greater than 100'
add_metrics_checks_numeric_range(checks, CHECK_RECORDS_NAME, 'records:COUNT_RECORDS',
                                         [('minimum', 100)])
```

## Make a defined check visible

:::{literalinclude} examples/metrics/metrics.py
:pyobject: set_check_visible
:::

```python
settings = dataset.get_settings()
CHECK_RECORDS_NAME = 'Number of records should be greater than 100'
checks = settings.get_raw()['metricsChecks']
set_check_visible(checks, CHECK_RECORDS_NAME)
```

## Retrieve metric results

:::{literalinclude} examples/metrics/metrics.py
:pyobject: get_metrics
:::

```python
result = {}

last_metrics = dataset.get_last_metric_values()
metrics = get_metrics(dataset)
for metric in metrics:
    metric_value = last_metrics.get_metric_by_id(metric)
    if metric_value and metric_value['lastValues']:
        result[metric] = {
            'initialValue': metric_value['lastValues'][0]['value']
        }
        
print(result)
```
## Retrieve check results

```{eval-rst}
.. literalinclude:: examples/metrics/metrics.py
    :pyobject: get_checks_used

.. literalinclude:: examples/metrics/metrics.py
    :pyobject: get_checks
 
```

## Reference documentation

### Classes

```{eval-rst}
.. autosummary::
        dataiku.core.metrics.ComputedMetrics
        dataiku.core.metrics.MetricDataPoint
        dataiku.core.metrics.ComputedChecks
        dataikuapi.dss.metrics.ComputedMetrics
```

### Functions

```{eval-rst}
.. autosummary::
    ~dataikuapi.dss.dataset.DSSDataset.compute_metrics
    ~dataikuapi.dss.dataset.DSSDataset.get_last_metric_values
    ~dataikuapi.dss.dataset.DSSDataset.get_settings
    ~dataikuapi.dss.dataset.DSSDatasetSettings.get_raw
    ~dataikuapi.dss.dataset.DSSDataset.run_checks
```

