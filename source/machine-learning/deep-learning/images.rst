Using image features
####################

It is possible to handle images using DSS deep learning. To do so, you must store your images in a managed folder (See :doc:`../../connecting/managed_folders`).

Then, you need to indicate in the dataset that will be used for running the analysis the location of your images. Create a new column containing the relative path of each image inside the managed folder. Then, in the "Features handling" tab of the analysis, select "Image" as type for this column.

You need to precise the managed folder where the images are stored in `Image location`, and to do a `Custom preprocessing` that looks like:

.. code-block:: python

    from tensorflow.keras.applications.imagenet_utils import preprocess_input
    from dataiku.doctor.deep_learning.keras_utils import load_img

    # This will give you an input shape of (197, 197, 3)
    def preprocess_image(image_file):
        # resized_dims - an optional resizing step
        # channels     -  'L', 'RGB' or 'CMYK'
        # data_format  - 'channels_last' or 'channels_first'
        array = load_img(image_file, resized_dims=(197, 197), channels='RGB', data_format='channels_last')
        # You can use your own preprocessing, here for example we use tensorflow's out of the box one
        array = preprocess_input(array, mode='tf')
        return array

where we see that the output for an image has a `(197, 197, 3)` shape. Then, this output is sent to a `image_path_preprocessed` input (if the name of the original column was `image_path`), so the corresponding input in the model should look like:

.. code-block:: python

	input_img = Input(shape=(197, 197, 3), name="image_path_preprocessed")


See `Deep learning for image classification <https://knowledge.dataiku.com/latest/ml-analytics/images/classification-code/tutorial-index.html>`_  for a step-by-step example of this in practice.

Scoring images
===================

When using a saved model that has image feature(s) for scoring, you can provide in the corresponding column(s):

* the relative path to the image, which must be stored in the **same** managed folder that was used for training
* a string that is the `Base64 <https://en.wikipedia.org/wiki/Base64>`_ representation of the image file.
