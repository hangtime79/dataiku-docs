Publish a Code Studio as a webapp
#################################

In addition to serving as high-end IDEs for code edition, Code Studios can also be used to run web applications that are not natively managed in DSS, i.e. which are not using the :doc:`DSS-webapp-managed frameworks, Flask, Bokeh, Shiny and Dash </webapps/index>`.


.. contents::
	:local:

Building a Code Studio template for webapps
===========================================

In order to be able to run as a Webapp, the Code Studio template should contain an entrypoint that will run the webapp.

Typically, a Code Studio template that's going to be used for webapps should contain the webapp framework (for example: Streamlit) and an IDE to edit each webapp's applicative code (for example: Visual Studio Code). This implies that the Code Studio template defines:

- several additions to the container image, either with existing blocks like the Visual Studio Code block, or with "Append toDockerfile" blocks, in order to install the necessary software onto the image
- several entrypoints: at least one to start the webapp, and usually one to start the IDE. The entrypoint for the webapp must  define an exposed port. The other endpoints may have their "launch for webapps" unchecked, if they're only needed to edit the webapp's code

.. note::

	Webapps can have more than 1 pod running a given Code Studio, and can be run with a "port-forward" exposition in DSS (it's actually the default). In such cases, each pod is served behind a different path prefix by the Nginx server of DSS, with the pod name used in the path prefix. It is thus recommended to use **TCP probing** on the "Kubernetes Parameters" block of the template, so that the deployments in Kubernetes can perform their rollout.

Creating a webapp from a Code Studio
====================================

The first step is to write the code of the webapp, so a Code Studio is instantiated from the template. Once the code is written and works, the webapp is created using the "publish" in the actions panel of the Code Studio. The created webapp is a reference to the Code Studio, and in particular, they share the same set of defining files (the Code Studio versioned and resource files).

.. note::

	After editing a Code Studio webapp, you don't need to publish it again. The webapp will always point to the latest state of its Code Studio reference after a restart.

Once a webapp runs, it can fetch files from the DSS server's filesystem like a regular Code Studio does, but cannot write back to the server's filesystem. It essentially has read-only access to the Code Studio files.


A complete example
====================

Now that we've seen how Code Studio Webapps work, let's rebuild the Streamlit sample from scratch.

The process up to a running webapp has several stages. We'll start by adding some script files in a location that templates can use:

- in "Global Shared code > Static web resources", create a ``start-streamlit.sh`` file with the following contents:

.. code-block:: bash

	#! /bin/bash

	USER=dataiku
	HOME=/home/dataiku

	LC_ALL=en_US.utf8 /opt/dataiku/bin/streamlit run --server.enableXsrfProtection=false --server.enableCORS=false --server.address=0.0.0.0 --server.port=8051 /home/dataiku/workspace/code_studio-versioned/app.py

- in "Global Shared code > Static web resources", create a ``streamlit-starter-app.py`` file with the following contents (for the original version, check `the Streamlit tutorial <https://docs.streamlit.io/library/get-started/>`_ ) :

.. code-block:: python

	import streamlit as st
	import pandas as pd
	import numpy as np

	st.title('Uber pickups in NYC')

	DATE_COLUMN = 'date/time'
	DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
	            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

	@st.cache
	def load_data(nrows):
	    data = pd.read_csv(DATA_URL, nrows=nrows)
	    lowercase = lambda x: str(x).lower()
	    data.rename(lowercase, axis='columns', inplace=True)
	    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
	    return data

	data_load_state = st.text('Loading data...')
	data = load_data(10000)
	data_load_state.text("Done! (using st.cache)")

	if st.checkbox('Show raw data'):
	    st.subheader('Raw data')
	    st.write(data)

	st.subheader('Number of pickups by hour')
	hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
	st.bar_chart(hist_values)

	# Some number in the range 0-23
	hour_to_filter = st.slider('hour', 0, 23, 17)
	filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

	st.subheader('Map of all pickups at %s:00' % hour_to_filter)
	st.map(filtered_data)


Once the resources are ready, we can build a Code Studio template that uses them. We denote by ``<k8s-config>`` the name of a Kubernetes config in "Administration > Settings > Containerized execution" to use.

- In "Administration > Code Studios", click **Create Code Studio template** and create a new ``defined by building blocks`` template named ``streamlit-template``
- in the "General" tab, for **Run on** select the ``<k8s-config>`` configuration
- in the "General" tab, for **Build for** select (at least) the ``<k8s-config>`` configuration
- in the "Definition" tab, click on **Add a block** and select ``Append to a dockerfile``
- name the block ``install streamlit``, check the **run as root** checkbox, and set the dockerfile addition to

.. code-block:: bash

	ENV LC_ALL en_US.utf8
	RUN /opt/dataiku/bin/python -m pip install markupsafe==2.0.1
	RUN /opt/dataiku/bin/python -m pip install streamlit \
	 && ln -s /opt/dataiku/pyenv/bin/streamlit /opt/dataiku/bin/streamlit \
	 && yum install -y psmisc


- in the "Definition" tab, click on **Add a block** and select ``Add an entrypoint``
- name the block ``run streamlit`` and set

   * set **Entrypoint** to ``/home/dataiku/start-streamlit.sh``
   * add an item to **Scripts** to copy ``${dip.home}/local/static/start-streamlit.sh`` to ``start-streamlit.sh``
   * toggle **Launch for webapps**
   * toggle **Expose port**
   * set **Exposed port label** to ``streamlit``
   * set **Exposed port** to 8501 (see value set in the ``/opt/dataiku/bin/streamlit`` command above)

- in the "Definition" tab, click on **Add a block** and select ``Visual Studio Code``
- in the "Definition" tab, click on **Add a block** and select ``Add starter files``
- in the block, add to the **Code Studio versioned files** a copy of ``${dip.home}/local/static/streamlit-starter-app.py`` to ``app.py``
- click **Save** then **Build**


Once the template is built, in a project with a project attached

- in "Code Studios" click **New Code Studio**
- select the ``streamlit-template`` Code Studio template, and create a new Code Studio named ``NYC``
- [optional] start the "NYC" code studio, edit the ``code_studio-versioned/app.py`` file, then click **Sync files with DSS**
- select the "NYC" Code Studio, and in its action panel, click **Publish**, then **Create**
- in the "Edit" tab of the "NYC" webapp, select ``<k8s-config>`` for **Container** (if not already selected)
- in the "Edit" tab of the "NYC" webapp, make sure the **exposition** is set to ``Port forwarding``. Usually this is the default at the instance level, but it can be overridden in the webapp's "Advanced settings"
- start the webapp and go to the "View" tab
