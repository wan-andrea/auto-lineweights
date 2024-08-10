## Dataset Creation
The dataset was created based on a subset of the [ABC-Dataset](https://deep-geometry.github.io/abc-dataset/), which features a bunch of CAD models including step format. The .STEP file format is easily read by Rhinoceros 3D and can be used in conjunction with the Make2D command, allowing for a quicker way to (manually) produce 2D line drawings without tracing screenshots. With the exception of files which failed the Make2D command or created corrupt Illustrator files, there were no specific criteria which prevented a model from being used to create the dataset.

For more information on how the .STEP file format is handled in Rhino, read [here](https://docs.mcneel.com/rhino/5/help/en-us/fileio/step_stp_import_export.htm). 

For more information on the Make2D command in Rhino, read [here](https://docs.mcneel.com/rhino/5/help/en-us/commands/make2d.htm). 

For more information about the creation of corrupt Illustrator files, follow the bug tracking identified in [this forum post](https://discourse.mcneel.com/t/zlib-error-trying-to-import-illustrator-file/188325).


## Dataset formats

### Dataset 1
The first version of the dataset contains:
- The original .STEP file used to create the line drawing, usually named something like "00000003_1ffb81a71e5b402e966b9341_step_002".
- The original .STEP file in Rhino .3dm format, which has the same name. (In most cases, this also includes a locked Perspective view, which shows the view at which the Make2D command was run, though this is NOT guaranteed due to human errors in creating the dataset.)
- An Adobe .pdf file, which was created when exporting the linework from Rhino.
- Two .jpg image files, one representing the normal map of the view, and another representing the z-buffer of the view.
- An Illustrator .ai file, which was created to align the linework from the .pdf with the .jpg images of the normal maps of each view.
- *Another Rhino .3dm file, which is simply named the number of the item in the dataset, like "3" or "76". This contains an import of the contents in the Illustrator file.

Normal maps were generated with a screenshot of the viewport, using the Rhino command TestShowNormalMap, which is only visible when the viewport is in Rendered display mode. For more information, refer to the forum post [here](https://discourse.mcneel.com/t/something-like-showzbuffer-that-shows-normals-of-a-scene/184889/4).

Similarly, z-buffer maps were also created with a screenshot of the viewport, using the Rhino command ShowZBuffer. For more information on the command, refer to the documentation [here](https://docs.mcneel.com/rhino/7/help/en-us/commands/showzbuffer.htm).

### Dataset 2
The first dataset consisted of curve attributes. This means that each line item in the dataset represents information about a curve in the drawing. In order to create this dataset, the Rhino files mentioned in Dataset 1 (see starred) were processed with a custom Grasshopper script, which extracted the following attributes about each curve:

- Curve type: Rhino classifies curves into different types of curves, such as lines, polylines, arcs, circular, elliptical, etc. For more information, refer to [this forum post](https://discourse.mcneel.com/t/how-to-identify-if-something-is-a-curve-polyline-polycurve-etc/183522/8).
- Curve closed: Indicates if the curve is a closed curve.
- Curve length: A float representing the length of the curve.
- Curve degree: For more information on curve degree, refer to [this explanation](https://www.rhino3d.com/features/nurbs/#:~:text=The%20knots%20are%20a%20list,must%20satisfy%20several%20technical%20conditions.) on NURBs curves.
- Curve deformable: A deformable curve in Rhino can be modified by "squishy" transformations such as projections, shears, and non-uniform scaling. For more information on curve attributes in Rhino, refer to [this documentation](https://developer.rhino3d.com/api/rhinocommon/rhino.geometry.curve#constructors). This is not really an important feature in our situation, so we can discard this feature.
- Curve periodic: A periodic curve (e.g. sine wave) is a curve that consists of a repeating pattern. This is usually not the case, so really, we can discard this feature.
- Curve span count: For more information on this attribute, refer to [this forum post](https://discourse.mcneel.com/t/how-do-i-determine-control-the-number-of-spans-in-a-curve/106131). This feature doesn't really provide any useful information, so we can discard this feature.
- Curve number of control points: For more information on curve attributes in Rhino, refer to [this documentation](https://developer.rhino3d.com/api/rhinocommon/rhino.geometry.curve#constructors).
- Curve distance from edge of page: This is a custom feature calculated based on distance between the midpoint of the curve and the closest point on the drawing boundary. It is unclear if this feature is useful, so we may discard it.
- Curve average normal value: This is a custom feature calculated by averaging the color of the normal map image sampled at all of the points on the curve. The way it is calculated makes it useless.
- Curve average zbuffer value: This is a custom feature calculated by averaging the color of the z-buffer image sampled at all of the points on the curve. The way it is calculated makes it useless.
- Curve Rhino ID: The Rhino object ID which is used to refer to the curve.

The .pkl files are named by drawing number, and contain all the curve attributes for each curve in each drawing. Because the dataset performed poorly in early experiments, it is an incomplete dataset consisting of only information from the first ~30 drawings.

#### Scripts used
The get_features.gh script runs on Rhino files to get the label by the layer name. An improved script get_features_by_color.gh instead uses the curve color to get the label (Profile = red, Contour = green, Detail = blue, Cut = magenta).

The functions.py provides all the functions which are used in main.py, which uses scikit-learn implementations of logistic regression, decision trees, etc. on the curve attributes extracted.

### Dataset 3
The second dataset focused on splitting the normal map image of each drawing based on the bounding box of each curve in the drawing. It contains:
- A .pkl file created using a Grasshopper script, which represents the coordinates of the bounding box* with which to crop the normal map image, and
- The normal map image of each drawing

From there, two versions of the dataset are created: one which is padded (so all the images have the same dimensions), and one which is not. The dataset is split into 4 folders: Cut, Profile, Contour, Detail, where each folder represents a class/label that we want to predict.

#### Scripts used

##### Data extraction
The Grasshopper scripts get_rec_bounds_coordinates.gh and get_rec_bounds_coordinates_v2.gh are used to extract the bounding boxes of each curve, and saves them as .pkl files to be read by Python.

##### Data processing
The crop_imgs.py script creates cropped images from a given .pkl file and a normal map image. make_dataset.py is a wrapper which calls this on all the images in a parent folder.

##### Models
train3.py is a model that looks at images of normal maps cropped to a curve and attempts to classify it as "Profile," "Contour," "Detail," or "Cut."

#### Dataset 3.1
The first version consists of images which are cropped using the bounding boxes (see starred), which is padded with black so that all the images are the same size. This is located in a folder called "cropped_padded".

#### Dataset 3.2
The second version provides a variation in which the images are NOT padded with black, and maintain their original size. This is located in a folder called "cropped".

### Dataset 4
The third dataset operates at the drawing level. It consists of normal map images and rasterized lineweighted drawings in which line weights are represented by color; these drawings are aligned and cropped the same way so that when overlapped, they go right on top of each other. The images are named identically by drawing number and are available in two folders, and in typical pix2pix fashion, combined into one image in a third folder.

### Dataset 5
The fourth dataset operates at the curve level. It consists of normal map images which are masked using an outline of each curve in the drawing.

#### Dataset 5.1
This is the raw output of the masks generated from the Grasshopper scripts.


#### Dataset 5.2
This dataset can be found in the "simplified" folder. The images are resized to ensure they are exactly the same size as the normal map images.

Since there are so few cut lines, we may as well consolidate them with the Profile lines. "Invalid" category is discarded. Now there are only three categories to classify, which should improve the conditions. However, the dataset is still imbalanced - we have:
- 1,557 Profile items
- 1,016 Contour items
- 585 Detail items

Nevertheless, this can still be used to create the image masks.


#### Scripts used
The mask_maker.gh Grasshopper script offsets each of the curves in a drawing, and creates a mask image from each curve. This must be run on Dataset 1's Rhino files.

These images need to be resized to the standard 2550 x 3300 in Datset 1's normal images in order to be used as masks for them. This is done by the resize_images.py script.

The images also need to be masked. This is done in the masking.py script.

