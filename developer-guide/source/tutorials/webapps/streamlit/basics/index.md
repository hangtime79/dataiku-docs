# Streamlit: your first webapp

In order to follow the steps in this tutorial you will need:

## Prerequisites

* Dataiku >= 11.0
* A Kubernetes cluster properly linked to the Dataiku instance (for more details, see the reference documentation page on {doc}`Elastic AI Computation <refdoc:containers/index>`).
* Access to a Project with relevant permissions to create Code Studios.
* A functioning Code Studio template for Streamlit webapps (for more details, see the reference documentation page on {doc}`Code Studio templates <refdoc:code-studios/code-studio-templates>`).

[Streamlit](https://streamlit.io/) is a popular web application framework, designed for building rich interactive applications using Python. In this article, you will develop a Streamlit application in Dataiku using the Code Studio feature and then deploy it as a Dataiku webapp.



## Preparing the source data

This tutorial is inspired by [one of Streamlit's demos](https://github.com/streamlit/demo-uber-nyc-pickups) and mostly reuses the same code and data. 

Start by downloading the source data following [this link](https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz) and make it available in your Dataiku Project, for example by uploading the *.csv.gz* file to it. Name the resulting Dataiku dataset `uber_raw_data_sep14`.

The dataset contains information about Uber pickup dates, times and geographical coordinates (latitude and longitude). To better understand this data, you will build a few data visualizations in the rest of the tutorial, but first, you need to set up the webapp's edition environment.

## Setting up the edition environment

In Dataiku, Streamlit webapps are built on top of {doc}`Code Studios <refdoc:code-studios/index>`, which are also used to provide advanced development environments. This tutorial assumes that you already have access to a functioning Code Studio template for Streamlit, referred to as `streamlit-template`. 

From your Project, create a new Code Studio instance: 

* In the "Code" menu, go to "Code Studios"


```{image} assets/01_menu_code_studio.png
:class: image-popup
```


* Click on "Create your first Code Studio"

* In the "New Code Studio" modal, select  `streamlit-template`, name your instance `uber-nyc-dev` and click on "Create".


```{image} assets/02_modal_create_code_studio.png
:class: image-popup w400
:align: center
```


The `uber-nyc` Code Studio is now created, but not started yet. To start it, click on *Start Code Studio*. After waiting for the start operation to be completed, you should see a "Hello World" message: this is the initial rendering of your Streamlit webapp! For now, it doesn't do much, but you will add more functionalities in the next sections.


```{image} assets/03_vscode_start.png
:class: image-popup
```


## Editing the webapp source code

Your first task is to surface the Uber pickup data in the webapp. Access the IDE environment in the "VS Code" tab of the Code Studio, and go to "Workspace > code_studio-versioned/streamlit/app.py". This will open the source code file of the webapp.


Add the following code:

```python
import streamlit as st
import dataiku
import pandas as pd

DATE_TIME_COL = "date/time"

#############
# Functions #
#############

@st.experimental_singleton
def load_data(nrows):
    data = dataiku.Dataset("uber_raw_data_sep14") \
        .get_dataframe(limit=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_TIME_COL] = pd.to_datetime(data[DATE_TIME_COL],
                                       format="%m/%d/%Y %H:%M:%S")
    return data

##############
# App layout #
##############

data = load_data(nrows=10000)

st.title('Uber pickups in NYC')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)
```

The structure of the code is split in two: 

* The *Functions* part contains all functions that rule the **behavior** of the application
* The *App layout* part lists the different visual components that the application is made of, hence defining its **appearance**.

For this initial step, you created a `load_data()` function that retrieves the source data and turns in into a pandas DataFrame that you'll be able to manipulate later for more advanced operations. The layout is fairly simple: it displays the content of that DataFrame as a table if the "Show raw data" box is ticked.

```{image} assets/04_streamlit_df.png
:class: image-popup
```

### Breaking down rides by hour of the day

Suppose now that you want to further investigate your data and check if there is a particular time of the day when the number of pickups is higher or lower than usual. To do so, you will create a histogram at the hour level and display it in the application. First, add a few more dependencies to import at the beginning of the file:

```
import altair as alt
import numpy as np
import pandas as pd
```

Then, add the histogram computation function to the *Functions* part:

```python
@st.experimental_memo
def histdata(df):
    hist = np.histogram(df[DATE_TIME_COL].dt.hour, bins=24, range=(0, 24))[0]
    return pd.DataFrame({"hour": range(24), "pickups": hist})
```

Finally, incorporate the histogram visualization in the application by adding this to the *App layout* section:

```python
# Histogram

chart_data = histdata(data)
st.write(
    f"""**Breakdown of rides per hour**"""
)

st.altair_chart(
    alt.Chart(chart_data)
    .mark_area(
        interpolate="step-after",
    )
    .encode(
        x=alt.X("hour:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=["hour", "pickups"],
    )
    .configure_mark(opacity=0.2, color="red"),
    use_container_width=True,
)
```

If you check back on the *Streamlit* tab you should now see a nice histogram rendered: 

```{image} assets/05_streamlit_histogram.png
:class: image-popup
```

### Drawing a scatter map with pickup locations

For the final item of your application, you will create a map displaying the pickup locations. To make it more interactive, you will also add a slider to filter the data and keep only a specific hour of the day.

No additional computation is needed here, so you can directly add the following code to the *App layout* part:

```python
# Map and slider

hour_to_filter = st.slider('', 0, 23, 17)
filtered_data = data[data[DATE_TIME_COL].dt.hour == hour_to_filter]
st.subheader(f"Map of all pickups at {hour_to_filter}:00")
st.map(filtered_data)
```

If you go back once more to the *Streamlit* tab you will see the newly-added map:

```{image} assets/06_streamlit_map.png
:class: image-popup
```

### Putting it all together

Your webapp is now fully functional! Here is the complete code for your application:

```python
import streamlit as st
import dataiku
import numpy as np
import pandas as pd
import altair as alt

DATE_TIME_COL = "date/time"

#############
# Functions #
#############

@st.experimental_singleton
def load_data(nrows):
    data = dataiku.Dataset("uber_raw_data_sep14") \
        .get_dataframe(limit=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_TIME_COL] = pd.to_datetime(data[DATE_TIME_COL],
                                       format="%m/%d/%Y %H:%M:%S")
    return data

@st.experimental_memo
def histdata(df):
    hist = np.histogram(df[DATE_TIME_COL].dt.hour, bins=24, range=(0, 24))[0]
    return pd.DataFrame({"hour": range(24), "pickups": hist})

##############
# App layout #
##############

# Load a sample from the source Dataset
data = load_data(nrows=10000)

st.title('Uber pickups in NYC')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# Histogram

chart_data = histdata(data)
st.write(
    f"""**Breakdown of rides per hour**"""
)

st.altair_chart(
    alt.Chart(chart_data)
    .mark_area(
        interpolate="step-after",
    )
    .encode(
        x=alt.X("hour:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=["hour", "pickups"],
    )
    .configure_mark(opacity=0.2, color="red"),
    use_container_width=True,
)

# Map and slider

hour_to_filter = st.slider('', 0, 23, 17)
filtered_data = data[data[DATE_TIME_COL].dt.hour == hour_to_filter]
st.subheader(f"Map of all pickups at {hour_to_filter}:00")
st.map(filtered_data)
```


## Publishing the webapp

Up to this point, your application is still living inside your development environment, namely your Code Studio instance. The final step of this tutorial is to make it widely available for other Dataiku users to view. 

* In the "Code Studios" list screen, select `uber-nyc-dev`
* In the Action panel on the right, select "Publish" and name your webapp (e.g. `Uber NYC App`) then click on "Create"

```{image} assets/07_modal_publish_webapp.png
:class: image-popup
```

Your Streamlit application is now deployed as a Dataiku webapp, congratulations! You can access it in "Code > Webapps > Uber NYC App". 

```{note}
Once you have deployed a Code Studio application as a Dataiku webapp, if you change the source code in the Code Studio editor then those changes will be directly reflected in the webapp. That is because the webapp itself constantly points to the latest state of the Code Studio.
```

## Wrapping up 

In this tutorial, you saw how to build a simple Streamlit application and deploy it as a Dataiku webapp, while leveraging the advanced code edition capabilities offered by the Code Studios feature. If you want to experiment with other frameworks like Dash or Bokeh, check out the available tutorials in the Webapp section.
