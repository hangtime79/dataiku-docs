Downloading from a Dataiku Webapp
*********************************

.. meta::
  :title: Download from a Dataiku webapp
  :description: How to download files from a Dataiku webapp
  :tag: 9.0
  :tag: webapps
  :tag: code
  :tag: python


.. for reference: https://community.dataiku.com/t5/Using-Dataiku-DSS/Download-from-DSS-in-a-Webapp/m-p/15838/highlight/true#M6619

When building a webapp in Dataiku, you may want to allow users to download a file from a `managed folder <https://doc.dataiku.com/dss/latest/connecting/managed_folders.html>`_. Here are steps to build an HTML button, which will allow webapp users to download files stored in a managed folder.

Basic Download
=================

Here's how you can download a file from a managed folder by clicking on a button in a webapp.

In the Python part of the webapp, define an endpoint like:

.. code-block:: python

    import dataiku
    from flask import request
    from flask import send_file
    import io
    @app.route('/downloadFile')
    def first_call():
        filename = request.args.get('filename')
        stream = dataiku.Folder('FOLDER_ID').get_download_stream(filename)
        with stream:
            return send_file(
                io.BytesIO(stream.read()),
                as_attachment=True,
                attachment_filename=filename)



Then in the Javascript section, you'd need a function like:

.. code-block:: javascript

    window.download = function(){
        window.location.href = getWebAppBackendUrl('/downloadFile?filename=test.txt');
    }


Finally, in the HTML you can add a button to trigger that JS function:

.. code-block:: html

    <button onclick="download()">Download</button>


What’s Next?
=================

To learn more about webapps in Dataiku, visit the :doc:`documentation <refdoc:webapps/index>`.
