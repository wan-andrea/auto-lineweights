# Given two file paths to images, mask the image with its mask
import cv2
import numpy as np
import os

# adopted from https://stackoverflow.com/questions/59432324/how-to-mask-image-with-binary-mask
def create_masked_img (img_path, mask_path, save_location):
    img = cv2.imread(img_path)
    mask = cv2.imread(mask_path)
    result = img.copy()
    result[mask == 0] = 0
    result[mask != 0] = img[mask != 0]
    name = os.path.splitext(os.path.basename(mask_path))[0] + "_masked.png"
    cv2.imwrite(save_location + name, result)


create_masked_img("C:/Users/andre/Downloads/PDF24844_000.png", "C:/Users/andre/Downloads/Contour/52_132c20b0-23f9-4cc9-99db-0fe87b598ea0.jpg", "C:/Users/andre/Downloads/")