# Help with dataset loading
# Do you care about the performance of loading the model, 
# and sharing it between processes where a memory mapped object on disk is beneficial?
# If yes, then you can consider using joblib.
import joblib
import os 
# Adopted from https://kapernikov.com/tutorial-image-classification-with-scikit-learn/
from skimage.io import imread
from skimage.transform import resize

def resize_all(src, pklname, include, width, height=None):
    """
    load images from path, resize them and write them as arrays to a dictionary, 
    together with labels and metadata. The dictionary is written to a pickle file 
    named '{pklname}_{width}x{height}px.pkl'.
     
    Parameter
    ---------
    src: str
        path to data
    pklname: str
        path to output file
    width: int
        target width of the image in pixels
    include: set[str]
        set containing str
    """
     
    height = height if height is not None else width
     
    data = dict()
    data['description'] = 'resized ({0}x{1})animal images in rgb'.format(int(width), int(height))
    data['label'] = []
    data['filename'] = []
    data['data'] = []   
     
    pklname = f"{pklname}_{width}x{height}px.pkl"
 
    # read all images in PATH, resize and write to DESTINATION_PATH
    for subdir in os.listdir(src):
        if subdir in include:
            print(subdir)
            current_path = os.path.join(src, subdir)
 
            for file in os.listdir(current_path):
                if file[-3:] in {'jpg', 'png'}:
                    im = imread(os.path.join(current_path, file))
                    im = resize(im, (width, height)) #[:,:,::-1]
                    data['label'].append(subdir[:-4])
                    data['filename'].append(file)
                    data['data'].append(im)
 
        joblib.dump(data, pklname)

data_path = "C:\\Users\\andre\\Documents\\github\\auto-lineweights\\datasets\\dataset5\\simplified_masked"
os.listdir(data_path)
include = {"Profile", "Contour", "Detail"} # edited 
# Create the dataset
resize_all(src=data_path, pklname="dataset5", width=300, include=include) # edited