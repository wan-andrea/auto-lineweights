from random import sample
import os

parent = 'C:\\Users\\andre\\Documents\\github\\auto-lineweights\\datasets\\dataset5\\simplified_binary_balanced\\Profile'
files = os.listdir('C:\\Users\\andre\\Documents\\github\\auto-lineweights\\datasets\\dataset5\\simplified_binary_balanced\\Profile')
for file in sample(files, 541):
    os.remove(parent + "\\" + file)