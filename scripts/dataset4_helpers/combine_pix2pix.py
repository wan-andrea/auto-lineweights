# As modified from https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/datasets/combine_A_and_B.py

import os
import numpy as np
import cv2
import argparse
from multiprocessing import Pool

def stack_images_horizontally(path_A, path_B, path_AB):
    print(f"Processing: {path_A} and {path_B}")  # Debugging print
    im_A = cv2.imread(path_A, cv2.IMREAD_COLOR)
    im_B = cv2.imread(path_B, cv2.IMREAD_COLOR)

    # Check if images are loaded properly
    if im_A is None:
        print(f"Error loading image A: {path_A}")
        return
    if im_B is None:
        print(f"Error loading image B: {path_B}")
        return

    # Resize B to match A if needed
    if im_A.shape != im_B.shape:
        im_B = cv2.resize(im_B, (im_A.shape[1], im_A.shape[0]))

    # Stack images horizontally
    combined_image = np.hstack((im_A, im_B))
    
    # Save the combined image
    cv2.imwrite(path_AB, combined_image)
    print(f"Saved stacked image to: {path_AB}")  # Debugging print

def main():
    parser = argparse.ArgumentParser(description='Stack images from two folders horizontally')
    parser.add_argument('--fold_A', dest='fold_A', help='Input directory for images A', type=str, required=True)
    parser.add_argument('--fold_B', dest='fold_B', help='Input directory for images B', type=str, required=True)
    parser.add_argument('--fold_AB', dest='fold_AB', help='Output directory', type=str, required=True)
    parser.add_argument('--num_imgs', dest='num_imgs', help='Number of images to process', type=int, default=1000000)
    parser.add_argument('--use_AB', dest='use_AB', help='If true, process matching pairs (0001_A, 0001_B) to (0001_AB)', action='store_true')
    parser.add_argument('--no_multiprocessing', dest='no_multiprocessing', help='Disable multiprocessing', action='store_true', default=False)
    args = parser.parse_args()

    # Check if output directory exists, create if not
    if not os.path.isdir(args.fold_AB):
        os.makedirs(args.fold_AB)

    # Get list of images in A folder
    img_list = os.listdir(args.fold_A)
    
    # If using _A/_B convention, filter the list
    if args.use_AB:
        img_list = [img_path for img_path in img_list if '_A.' in img_path]

    num_imgs = min(args.num_imgs, len(img_list))
    print(f'Using {num_imgs}/{len(img_list)} images')

    if not args.no_multiprocessing:
        pool = Pool()

    for n in range(num_imgs):
        name_A = img_list[n]
        path_A = os.path.join(args.fold_A, name_A)
        name_B = name_A.replace('_A.', '_B.') if args.use_AB else name_A
        path_B = os.path.join(args.fold_B, name_B)
        name_AB = name_A.replace('_A.', '.') if args.use_AB else name_A
        path_AB = os.path.join(args.fold_AB, name_AB)

        # Process images
        if os.path.isfile(path_A) and os.path.isfile(path_B):
            if not args.no_multiprocessing:
                pool.apply_async(stack_images_horizontally, args=(path_A, path_B, path_AB))
            else:
                stack_images_horizontally(path_A, path_B, path_AB)

    if not args.no_multiprocessing:
        pool.close()
        pool.join()

if __name__ == "__main__":
    main()
