Simple scoring application
**************************

Prerequisites
##############

* Dataiku >= 12.1
* Access to an existing project with the following permissions:
    * "Read project content"
    * "Write project content"
* Access to a model deployed as an API endpoint for scoring

Introduction
############
In this tutorial, you will learn how to request an API endpoint.
This endpoint can be a deployed model (like in this tutorial) or anything else connected to an API endpoint.
This tutorial uses the model from the MLOps training (from Learning projects > MLOps project)
and a deployed API endpoint named ``SimpleScoring``.
It provides an API endpoint to predict the authorized flag for the provided data (transaction from credit card).

To follow the tutorial, you must know the URL where the endpoint is deployed.
You can find this URL in the **Local Deployer > API services**
and select the tab **Sample code** from your deployment, and note the IP address (and the port) as shown in
:ref:`Fig. 1<tutorial_webapp_standard_simple_scoring_ip_address>`

.. _tutorial_webapp_standard_simple_scoring_ip_address:

.. figure:: ./assets/ip-address.png
    :align: center
    :class: with-shadow image-popup
    :alt: Figure 1: Where to find the URL of an API endpoint.

    Figure 1: Where to find the URL of an API endpoint.

Once the URL is known, you are ready to start the tutorial.
Create a new "Simple web app to get started" standard webapp.

Building the webapp
#####################
You will rely on the method :meth:`dataikuapi.APINodeClient.predict_record`
from the ``dataikuapi`` package to use the API endpoint.
This method requires having an identifier of the endpoint to query and a Python dictionary of features.
Before using this method, you need to obtain a :class:`dataiku.APINodeClient`. This process is shown in
:ref:`Code 1<tutorial_webapp_standard_simple_scoring_get_prediction>`.

.. _tutorial_webapp_standard_simple_scoring_get_prediction:
.. literalinclude:: ./assets/webapp.py
    :caption: Code 1: Get a prediction from a :class:`dataiku.APINodeClient`
    :lines: 19-22
    :language: python

To instantiate the client, you need the endpoint's URL and the deployed endpoint's name.
So you will create a form for the user to enter this data.
And, as features must be supplied to use the :meth:`dataikuapi.APINodeClient.predict_record` method,
you will include this data entry in the form.
:ref:`Code 2<tutorial_webapp_standard_simple_scoring_html_form>` shows a possible implementation of such a form.

.. _tutorial_webapp_standard_simple_scoring_html_form:
.. literalinclude:: ./assets/webapp.html
    :caption: Code 2: Form implementation
    :lines: 7-55
    :language: html
    :emphasize-lines: 1

This form uses Bootstrap in its `5.1.3` version. You will find how to use this bootstrap version in the
:ref:`complete HTML code<tutorial_webapp_standard_simple_scoring_complete_html_code>` at the first and last line
by using a CDN. But you can use the embedded bootstrap version in Dataiku or a local one if needed.

The first line of the form defines the javascript function to call when the user clicks on the "Score it" button.
The `score` function is responsible for sending the data from the form to the backend
and sending back the backend response to the user (:ref:`Code 3<tutorial_webapp_standard_simple_scoring_js_code>`).

.. _tutorial_webapp_standard_simple_scoring_js_code:
.. literalinclude:: ./assets/webapp.js
    :caption: Code 3: Javascript code
    :language: javascript
    :emphasize-lines: 30-46

You do not know how many features will be sent to the backend, neither the order nor the name of the features.
This prevents you from defining a specific route to be processed by the backend.
It also prevents you from using the query string (``?...``).
You should use a ``POST`` request with a JSON body containing all information needed by the backend.
This is the purpose of the highlighted lines in :ref:`Code 3<tutorial_webapp_standard_simple_scoring_js_code>`.

The first function is sending the data to the backend
and processing the response to display the result on the frontend.
Some error handlings have been implemented, but you can do more.

The Python backend (:ref:`Code 4<tutorial_webapp_standard_simple_scoring_python_code>`) is pretty simple.
It extracts the needed information from the body request, uses it to predict the result,
and creates an appropriate response that you will send back to the caller
That is the javascript code in the context of this tutorial.

.. _tutorial_webapp_standard_simple_scoring_python_code:
.. literalinclude:: ./assets/webapp.py
    :caption: Code 4: Python code
    :language: python

Complete code and conclusion
############################
:ref:`Code 6<tutorial_webapp_standard_simple_scoring_complete_html_code>` is the complete HTML code you should have
at the end of the tutorial. Codes :ref:`7<tutorial_webapp_standard_simple_scoring_complete_js_code>` and
:ref:`8<tutorial_webapp_standard_simple_scoring_python_code>` are for the Javascript and the Python
code. You should not have specific CSS code, as you use Bootstrap. You now have a working webapp for scoring data.

You can go further by changing the result display, or the input form to adapt to your specific needs.


.. _tutorial_webapp_standard_simple_scoring_complete_html_code:
.. dropdown:: Code 6: Complete HTML code of the webapp

    .. literalinclude:: ./assets/webapp.html
        :language: html

.. _tutorial_webapp_standard_simple_scoring_complete_js_code:
.. dropdown:: Code 7: Complete Javascript code of the webapp

    .. literalinclude:: ./assets/webapp.js
        :language: javascript

.. _tutorial_webapp_standard_simple_scoring_complete_python_code:
.. dropdown:: Code 8: Complete python code of the webapp

    .. literalinclude:: ./assets/webapp.py
        :language: python
