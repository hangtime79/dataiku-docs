:orphan:

Endpoint APIs
#############

Once a model has been deployed to the flow, it can be deployed on the API node to score one or several images on demand.
See :doc:`../../apinode/index` for more details.

Input format
============

The supported input format for scoring computer vision models with API endpoints is as follows:

.. code-block:: javascript

    {
        "features": {
            "input": base64_image
        }
    }


with `base64_image` being the `base64 <https://en.wikipedia.org/wiki/Base64>`_ encoded image.

The results will be the same than in the scoring recipe.
Note that for Object detection, predictions are filtered based on the `Confidence score threshold` set in the corresponding Saved Model. See :doc:`./performance-assessment` for more details.