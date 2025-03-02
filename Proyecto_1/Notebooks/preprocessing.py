
import tensorflow as tf
import tensorflow_transform as tft

import constants_preprocessing

NUMERIC_FEATURE_KEYS = constants_preprocessing.NUMERIC_FEATURE_KEYS
CATEGORICAL_FEATURE_KEYS = constants_preprocessing.CATEGORICAL_FEATURE_KEYS
LABEL_KEY = constants_preprocessing.LABEL_KEY
transformed_name = constants_preprocessing.transformed_name

# Define the transformations
def preprocessing_fn(inputs):
    """tf.transform's callback function for preprocessing inputs.
    Args:
        inputs: map from feature keys to raw not-yet-transformed features.
    Returns:
        Map from string feature key to transformed feature operations.
    """
    outputs = {}

    # Scale these features to the range [0,1]
    for key in NUMERIC_FEATURE_KEYS:
        outputs[transformed_name(key)] = tft.scale_to_0_1(
            inputs[key])
    
    # Bucketize these features
    #for key in BUCKET_FEATURE_KEYS:
     #   outputs[transformed_name(key)] = tft.bucketize(
      #      inputs[key], _FEATURE_BUCKET_COUNT[key])

    # Convert strings to indices in a vocabulary
    for key in CATEGORICAL_FEATURE_KEYS:
        outputs[transformed_name(key)] = tft.compute_and_apply_vocabulary(inputs[key])

    # Convert the label strings to an index
    outputs[transformed_name(LABEL_KEY)] = tft.compute_and_apply_vocabulary(inputs[LABEL_KEY])

    return outputs
