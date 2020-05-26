import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
import os
from PIL import Image as pil_image

DANK_MEMES_DIR = 'dankmemes-checked'
REGULAR_MEMES_DIR = 'regularmemes-checked'
ALT_MEMES_DIR = 'newalternative-checked'


def input_fn():
      return tf.compat.v1.train.limit_epochs(
                    tf.convert_to_tensor(points, dtype=tf.float32), num_epochs=1)

def analyze_images(directory, feature_name_list, model):
    memes = os.scandir(directory)
    for i, file_name in enumerate(memes):
        full_path = directory + "/" + file_name.name
        print("    Status: %s / %s" %(i, full_path), end="\r")
        img = image.load_img(full_path, target_size=(224, 224))
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)
        features = np.array(model.predict(img_data))
        feature_name_list.append((features.flatten(), full_path))

def main():
    model = VGG16(weights='imagenet', include_top=False)
    feature_and_name_list = []
    analyze_images(DANK_MEMES_DIR, feature_and_name_list, model)
    analyze_images(REGULAR_MEMES_DIR, feature_and_name_list, model)
    analyze_images(ALT_MEMES_DIR, feature_and_name_list, model)
    print("Predictions DONE!")

    np.save("feature_name_array.npy", feature_and_name_list)

if __name__ == "__main__":
    main()
