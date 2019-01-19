#!/usr/bin/python3
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import skimage, os
from skimage.morphology import ball, disk, dilation, binary_erosion, remove_small_objects, erosion, closing, reconstruction, binary_closing
from skimage.measure import label,regionprops, perimeter
from skimage.filters import roberts, sobel
from skimage import measure, feature
from skimage.segmentation import clear_border
from skimage import data
from scipy import ndimage as ndi
import matplotlib.pyplot as plt
from pydicom.data import get_testdata_files
import pydicom
# Input data files are available in the \../input/\ directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory
from subprocess import check_output
# Any results you write to the current directory are saved as output.
import dicom
import scipy.misc
import numpy as np
import cv2
from argparse import ArgumentParser
from contour_following import test

# filename = get_testdata_files()[0]
# lung = pydicom.dcmread('../input/1.2.826.0.1.3680043.2.656.4.1.1.896.55.dcm')
# slice = lung.pixel_array
# slice[slice == -2000] = 0
# print (lung.RescaleIntercept, lung.RescaleSlope, np.min(slice), np.max(slice))
# plt.imshow(slice, cmap=plt.cm.gray)

def get_segmented_lungs(im):
    # Convert into a binary image. 
    binary = im < 604
    
    # Remove the blobs connected to the border of the image
    cleared = clear_border(binary)
    # Label the image
    label_image = label(cleared)
    # Keep the labels with 2 largest areas
    areas = [r.area for r in regionprops(label_image)]
    areas.sort()
    if len(areas) > 2:
        for region in regionprops(label_image):
            if region.area < areas[-2]:
                for coordinates in region.coords:                
                    label_image[coordinates[0], coordinates[1]] = 0
    binary = label_image > 0
    # Closure operation with disk of radius 12
    selem = disk(2)
    binary = binary_erosion(binary, selem)
    
    selem = disk(10)
    binary = binary_closing(binary, selem)
    
    # Fill in the small holes inside the lungs
    edges = roberts(binary)
    binary = ndi.binary_fill_holes(edges)
    # Superimpose the mask on the input image
    get_high_vals = binary == 0
    im[get_high_vals] = 0
        
    return im

def read_ct_scan(image_path):
    # filename = get_testdata_files('1.2.826.0.1.3680043.2.656.4.1.1.896.46.dcm')[0]
    slices = pydicom.dcmread(image_path)
    
    # Get the pixel values for all the slices
    slices = np.stack([slices.pixel_array])
    slices[slices == -2000] = 0
    
    return slices

def segment_lung_from_ct_scan(ct_scan):
    
    return np.asarray([get_segmented_lungs(slice) for slice in ct_scan])

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument('image')
    parser.add_argument('--test', '-t')
    
    args = parser.parse_args()

    ct_scan = read_ct_scan(args.image)
    segmented_ct_scan = segment_lung_from_ct_scan(ct_scan)
    # plt.imsave('segmented1', segmented_ct_scan[0], cmap=plt.cm.gray)
    
    segmented_ct_scan[segmented_ct_scan < 700] = 0
    segmented_ct_scan[segmented_ct_scan > 255] = 255
    segmented_ct_scan = np.array([segmented_ct_scan[0]], dtype=np.uint8)
    plt.imsave('watershed_results/' + args.image.split('/')[-1].split('.')[0]\
               + '_watershed.png', segmented_ct_scan[0], cmap=plt.cm.gray)

    if args.test:

        ground_truth = cv2.imread(args.test, 0)
        
        jacquard, sensitivity, specificity = test(segmented_ct_scan[0], ground_truth)

        print(','.join([''.join(args.image.split('.')[:-1]).split('/')[-1],
                        '%.3f' % round(jacquard,3),
                        '%.3f' % round(sensitivity,3),
                        '%.3f' % round(specificity,3)]))
