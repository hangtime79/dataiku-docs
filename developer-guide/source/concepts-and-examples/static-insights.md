(static-insights)=

```{eval-rst}
..
  this code samples has been verified on DSS: 13.2.0
  Date of check: 24/09/2024
```

# Static insights

In DSS code recipes and notebooks, you can create static insights: data files that are created by code and that can be rendered on the dashboard.

This capability can notably be used to embed in one click charts created using:

- {doc}`Plot.ly <refdoc:python/plotly>`
- {doc}`Matplotlib <refdoc:python/matplotlib>`
- {doc}`Bokeh <refdoc:python/bokeh>`
- {doc}`Ggplot <refdoc:python/ggplot>`

You can also use it for embedding in the dashboard any kind of content (image, HTML, ...)

## Reference documentation

```{eval-rst}
.. autosummary::
        dataiku.insights.save_data
        dataiku.insights.save_figure
        dataiku.insights.save_bokeh
        dataiku.insights.save_plotly
        dataiku.insights.save_ggplot
```
