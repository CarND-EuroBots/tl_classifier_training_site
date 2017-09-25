# Traffic Light Classifier for Udacity CarND Capstone Project

The CarND Capstone project requires classification of traffic light from image.  This project includes the dataset and code for training this classifier

## Archtecture
The classifier is based on Mobilenet network, for its speed, retrained to classify each image to one of these classes:

* Green
* Yellow
* Red
* None - no traffic light is visible in image

The network is using TensorFlow and retrain program taken from Tensorflow example code:

[https://github.com/tensorflow/tensorflow/tree/master/tensorflow/examples/image_retraining](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/examples/image_retraining)

## Dataset

The dataset of train images was harvested from rosbags of data recorded in the Udacity circuit and included as part of project resources.  A total of 1840 images were collected and tagged using [tag.py](tag.py) script:

`python tag.py --src sourch_path --dest dest_path`

## Training

To train the network run this:

`python retrain.py --image_dir tl_images_all --architecture mobilenet_1.0_224`

## Test

To test the trained network, run this on a test image:

```
python label_image.py --graph=path_to_model.pb --labels=path_to_classes.txt
--image=path_to_test_image --input_layer=input --output_layer=final_result
 --input_mean=128 --input_std=128 --input_width=224 --input_height=224
```
