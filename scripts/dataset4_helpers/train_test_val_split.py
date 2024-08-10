# Utility which takes in an image folder such as img_combined, and splits it into train, test, and validation dataset subfolders at random based on percentages

import os
import shutil
import random

def train_test_val_split(path, train_percent, test_percent, new_path):

    # Validate input percentages
    if train_percent + test_percent >= 1:
        raise ValueError("Train and test percentages must sum to less than 1")

    # Create output folders
    train_dir = os.path.join(new_path, 'train')
    test_dir = os.path.join(new_path, 'test')
    val_dir = os.path.join(new_path, 'val')
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    # Get a list of all image files in the folder
    images = [f for f in os.listdir(path) if f.endswith(('.jpg', '.jpeg', '.png'))]
    num_images = len(images)

    # Calculate number of images for each set
    num_train = int(train_percent * num_images)
    num_test = int(test_percent * num_images)
    num_val = num_images - num_train - num_test

    # Randomly shuffle the image list
    random.shuffle(images)

    # Split the images into train, test, and val sets
    train_images = images[:num_train]
    test_images = images[num_train:num_train+num_test]
    val_images = images[num_train+num_test:]

    # Copy images to respective folders
    for image in train_images:
        shutil.copy(os.path.join(path, image), os.path.join(train_dir, image))
    for image in test_images:
        shutil.copy(os.path.join(path, image), os.path.join(test_dir, image))
    for image in val_images:
        shutil.copy(os.path.join(path, image), os.path.join(val_dir, image))

train_test_val_split("C:/Users/andre/Documents/github/auto-lineweights/datasets/dataset4/test", 0.8, 0.1, "C:/Users/andre/Documents/github/auto-lineweights/datasets/dataset4/imgs_combined_split")
print("Done!")