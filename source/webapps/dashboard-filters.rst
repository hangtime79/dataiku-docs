Accessing dashboard filters
===========================

:doc:`/webapps/standard` can access the dashboard filters by listening for messages sent from the dashboard. This allows to dynamically adjust the content of the webapp based on the filters applied in the dashboard.

Here is an example of how to access the dashboard filters using JavaScript:

.. code-block:: javascript

    window.addEventListener('message', function(event) {
      const data = event.data;
      if (data && data.type === 'filters') {
          console.log(data.filters); // the filters
      } 
    });

This code listens for messages sent to the webapp. When a message of type 'filters' is received, it logs the filters and their parameters to the console. You can use this information to update the webapp's display dynamically.
