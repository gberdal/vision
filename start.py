import io
import os
import pprint
import imghdr
import numpy as np
from skimage import io

# Imports the Google Cloud client library
# noinspection PyPackageRequirements
from google.cloud import vision
# noinspection PyPackageRequirements
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# Uncomment to see color histogram.
show_histogram = False


def read_image(image_path):
    """
    Reads images as bytes
    :param image_path: string
    :return: Google Vision Image object
    """
    exceptions = ['.DS_Store']
    supported_img_types = ['jpg', 'jpeg', 'png']
    filename = os.path.basename(image_path)
    img_type = imghdr.what(image_path)
    if filename in exceptions:
        return
    if img_type not in supported_img_types:
        raise Exception('Invalid image type')
    with open(image_path, 'rb') as fh:
        content = fh.read()
    
    # create an image object
    # noinspection PyUnresolvedReferences
    _image = types.Image(content=content)
    return _image


def detect_labels(vision_image):
    """
    Performs label detection on images
    :param vision_image: Google Vision Image
    :return: list of strings
    """
    response = client.label_detection(image=vision_image)
    labels = response.label_annotations

    # allows selection of attributes
    selected_label_attrs = [label.description for label in labels]
    return selected_label_attrs


def detect_landmarks(vision_image):
    """
    Attempts to detect landmarks on images
    :param vision_image: Google Vision Image
    :return: dictionary
    """
    response = client.landmark_detection(image=vision_image)
    landmarks = response.landmark_annotations

    # just formatting output
    detected_landmarks = []
    for landmark in landmarks:
        new_landmark = {
            "name": landmark.description,
            "locations":  []
        }
        for location in landmark.locations:
            lat_lng = location.lat_lng
            new_location = (lat_lng.latitude, lat_lng.longitude)
            new_landmark["locations"].append(new_location)
        detected_landmarks.append(new_landmark)
    return detected_landmarks


def detect_logos(vision_image):
    """
    Detects known logos on images
    :param vision_image: Google Vision Image
    :return: list of strings
    """
    response = client.logo_detection(image=vision_image)
    logos = response.logo_annotations

    # allows selection of attributes
    selected_attrs = [logo.description for logo in logos]
    return selected_attrs


def get_color_palette(vision_image, show=True):
    """
    Uses MatPlotLib to show a histogram of the color palette
    derived from the color analysis of the image.
    If show is False, returns the detected properties.
    :param vision_image: Google Vision Image
    :param show: boolean (when True the histogram is shown)
    :return: dictionary
    """
    response = client.image_properties(image=vision_image)
    props = response.image_properties_annotation

    if not show:
        return props

    # create the palette out of the colors in the response
    rgb_array = []

    for color in props.dominant_colors.colors:
        red = color.color.red
        green = color.color.green
        blue = color.color.blue
        rgb = [red, green, blue]
        rgb_array.append(rgb)

    palette = np.array(rgb_array, dtype=np.uint8)
    indices = np.ndarray(shape=[1, 10], buffer=np.array(range(0, len(rgb_array))), dtype=int)

    io.imshow(palette[indices])
    io.show()


def detect_objects(vision_image):
    """
    Detects objects and their locations on images
    :param vision_image: Google Vision Image
    """
    objects = client.object_localization(
        image=vision_image).localized_object_annotations

    objects_found = []
    for object_ in objects:
        new_object = {
            "name": object_.name,
            "coordinates": object_.bounding_poly.normalized_vertices
        }
        objects_found.append(new_object)


def detect_image_safety(vision_image):
    """
    Performs a NSFW kind analysis on the image.
    :param vision_image: Google Vision Image
    :return: dictionary
    """
    response = client.safe_search_detection(image=vision_image)
    safe = response.safe_search_annotation
    return safe


# The name of the image file to annotate
file_name = os.path.abspath('images/bikini.jpg')

# Loads the image into memory
image = read_image(image_path=file_name)

# Performs label detection on the image file
print("\nLabels:")
pprint.pprint(detect_labels(image))

# Landmark Detection
print('\nLandmarks:')
pprint.pprint(detect_landmarks(image))

# Color palette from property analysis
print("\nColor palette:")
if show_histogram:
    get_color_palette(image)
else:
    print("Displaying color palette is disabled.")

# Detect Logos
print("\nLogos:")
pprint.pprint(detect_logos(image))

# Localised Objects
print("\nObjects:")
pprint.pprint(detect_objects(image))

# Perform Safe Search
print("\nSafe Search:")
pprint.pprint(detect_image_safety(image))
