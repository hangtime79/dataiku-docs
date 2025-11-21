Data augmentation
##################

Data augmentation adds additional diversity to your training dataset by applying distortions to your images that could be expected in the real world, thereby assisting the model to generalize.

Data augmentations settings
============================


.. image:: img/data-augmentation.png


Categories of augmentations can be enabled or not. They are independent from one to another (one can be applied when another is not). When activated, they are applied with a given probability for each image independently, at each epoch.


* **Color transformations**: Activating the color augmentation will alter the hue, contrast and brightness of your images.

* **Affine transformations**: Activating horizontal or vertical flip will invert your images. Activating the rotation will apply a rotation chosen randomly in the range [-maximum rotation, +maximum rotation] where maximum rotation is a parameter you can change.

* **Crop transformations**: When activated, a random portion of the images will be used for training, which is at least the size defined by the parameter "Min. kept ratio". By default it is set to 0.75, ensuring that between 75% - 100% of the image area is preserved. The kept area will have the same aspect ratio as the original image, and the crop is performed randomly (i.e. not always central).


N.b. Object detection
======================
For object detection, the bounding box annotations are updated to reflect the transformations applied to each image.

Crop and rotation can crop out of the image an annotated object. In this case the corresponding annotations for this object are removed. If the object is only partially cropped,
annotations are kept but updated to fit the new image dimensions.
In any case, DSS ensures that at least one bounding box remains after the augmentation is applied.
