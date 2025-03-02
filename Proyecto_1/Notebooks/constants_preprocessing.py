
# Definir nombres de características y tipos
NUMERIC_FEATURE_KEYS = [
    'Elevation',
     'Slope',
     'Horizontal_Distance_To_Hydrology',
     'Horizontal_Distance_To_Roadways',
     'Hillshade_9am',
     'Hillshade_Noon',
     'Horizontal_Distance_To_Fire_Points'
]
CATEGORICAL_FEATURE_KEYS = ["Wilderness_Area", 'Soil_Type']
LABEL_KEY = "Cover_Type"

# Utility function for renaming the feature
def transformed_name(key):
    return key + '_xf'
