from PIL import Image
import os
# Basic usage
"""
path = "C:/Users/andre/Downloads/Profile/52_7bc51bd0-97f1-45f4-bb19-47e32e186204.jpg"
im = Image.open(path)
im2 = im.resize((2550, 3300))
im2.save(path)
"""
def resize_images_in_folder(parent_folder, width=2550, height=3300):
    for img in os.listdir(parent_folder):
        path = parent_folder + "/" + img
        print("Processing ", path, "...")
        im = Image.open(path)
        im2 = im.resize((2550, 3300))
        im2.save(path)

resize_images_in_folder("C:\\Users\\andre\\Documents\\github\\auto-lineweights\\datasets\\dataset5\\simplified\\Profile")
print("Done1!")
resize_images_in_folder("C:\\Users\\andre\\Documents\\github\\auto-lineweights\\datasets\\dataset5\\simplified\\Contour")
print("Done2!")
resize_images_in_folder("C:\\Users\\andre\\Documents\\github\\auto-lineweights\\datasets\\dataset5\\simplified\\Detail")
print("Done3!")