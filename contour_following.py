#!/usr/bin/python3
import numpy as np
import cv2 as cv
from argparse import ArgumentParser

def test(result, ground_truth):

    intersection = cv.bitwise_and(result, ground_truth)
    
    TP = intersection
    FN = cv.bitwise_xor(intersection, ground_truth)
    FP = cv.bitwise_xor(intersection, result)
    TN = 255 - (TP + FN + FP)
    
    jacquard = TP[TP == 255].size / (TP[TP == 255].size + FN[FN == 255].size + FP[FP == 255].size)
    sensitivity = TP[TP == 255].size / (TP[TP == 255].size + FN[FN == 255].size)
    specificity = TN[TN == 255].size / (TN[TN == 255].size + FP[FP == 255].size)

    return jacquard, sensitivity, specificity
    
def D(p1, p2):

    return np.sqrt(((p1 - p2) ** 2).sum())

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('image')
    parser.add_argument('--test', '-t')
    parser.add_argument('--threshold', '-T', default=127, type=int)
    parser.add_argument('--min-area', '-a', default=50, type=int)
    parser.add_argument('--max-area', '-A', default=150, type=int)

    args = parser.parse_args()

    if args.min_area > args.max_area:
        
        args.max_area = 2 * args.min_area

    img = cv.imread(args.image, 0)
    _, img = cv.threshold(img, args.threshold, 255, cv.THRESH_BINARY)
    img, contours, hierarchy = cv.findContours(img, 1, 2)
    ret_img = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)


    for C in contours:

        C_geo_mean = np.array(C[:, 0, :].mean(axis=0), dtype=np.int)
    
        if cv.contourArea(C) < args.min_area or cv.contourArea(C) > args.max_area\
           or img[C_geo_mean[1], C_geo_mean[0]] == 0:            
        
            continue

        ret_img = cv.drawContours(ret_img, [C], 0, (255, 255, 255), cv.FILLED)

    # for i in range(512):
    #     for j in range(512):
    
    #         if ret_img[i, j, 3] == 0:
    
    #             ret_img[i, j, :] = np.append(orig_img[i, j, :], 255)
        
    cv.imwrite('contour_results/' + args.image.split('/')[-1].split('.')[0]\
               + '_contour.png', ret_img)

    if args.test:
       
        ground_truth = cv.imread(args.test, 0)

        jacquard, sensitivity, specificity = test(ret_img, ground_truth)
        
        print(','.join([''.join(args.image.split('.')[:-1]).split('/')[-1],
                        '%.3f' % round(jacquard,3),
                        '%.3f' % round(sensitivity,3),
                        '%.3f' % round(specificity,3)]))
