import tensorflow as tf
import tensorflow_hub as hub
import numpy as np

from PIL import Image

model_name = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/4"

# Load the pre-trained model
img_shape = (224, 224)
classifier = tf.keras.Sequential([
    hub.KerasLayer(model_name, input_shape=img_shape+(3,))
])

# Download image and compute prediction
img_url = "https://upload.wikimedia.org/wikipedia/commons/b/b0/Bengal_tiger_%28Panthera_tigris_tigris%29_female_3_crop.jpg"
img = tf.keras.utils.get_file('image.jpg', img_url)
img = Image.open(img).resize(IMAGE_SHAPE)
img = np.array(img)/255.0
result = classifier.predict(img[np.newaxis, ...])

# Map the prediction result to the corresponding class label
labels_url = "https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt"
predicted_class = tf.math.argmax(result[0], axis=-1)
labels_path = tf.keras.utils.get_file('ImageNetLabels.txt', labels_url)
imagenet_labels = np.array(open(labels_path).read().splitlines())
predicted_class_name = imagenet_labels[predicted_class]

print(f"Predicted class name: {predicted_class_name}")