from PIL import Image
import cv2
import numpy as np
import os
from scorers import MnistScorer 

import datetime

def main():
    
    path = 'images/'

    #this to process all images
    # for root, directories, files in os.walk(path, topdown=False):
    #     for name in files:
    #         curr_img = os.path.join(root, name)

    curr_img = "images/200728_145911.png"
    img = Image.open(curr_img)
    score_crop_path = get_score_crop(img)
    get_state_crop(img)
    score = extract_score(score_crop_path)
    print(score)

def get_state_crop(im, step=0):

    (st_left, st_upper, st_right, st_lower) = (770, 485, 1070, 785)
    
    state_crop = im.crop((st_left, st_upper, st_right, st_lower))
    save_path = "images/state_crops/{}.png".format(step)
    state_crop.save(save_path)

    return save_path

def get_score_crop(im, step=0):
    
    # The crop method from the Image module takes four coordinates as input.
    # The right can also be represented as (left+width)
    # and lower can be represented as (upper+height).
    (sc_left, sc_upper, sc_right, sc_lower) = (860, 365, 935, 400) 
    
    # Here the image "im" is cropped and assigned to new variable score_crop
    score_crop = im.crop((sc_left, sc_upper, sc_right, sc_lower))
    save_path = "images/score_crops/{}.png".format(step)
    score_crop.save(save_path)

    return save_path


def extract_score(img_path, step=0):
    
    image = cv2.imread(img_path)
    score_crop_image= img = Image.open(img_path)
    cv2.waitKey(0) 
    
    # Grayscale 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    
    # Find Canny edges 
    edged = cv2.Canny(gray, 30, 200) 
    cv2.waitKey(0) 
    
    # Finding Contours 
    # Use a copy of the image e.g. edged.copy() 
    # since findContours alters the image 
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    
    #not showing this for now
    #cv2.imshow('Canny Edges After Contouring', edged) 
    #cv2.waitKey(0) 
    
    contour_count = len(contours)
    #print("Number of Contours found = " + str(contour_count)) 
    
    # Draw all contours 
    # -1 signifies drawing all contours 
    cv2.drawContours(image, contours, -1, (0, 255, 0), 3) 
        
    centroids = np.zeros((contour_count, 2))
    
    for i in range(len(contours)):
        curr_centroid = np.mean(contours[i] , axis = 0)[0]
        #print(type(curr_centroid))
        #print("contour " + str(i) + str(curr_centroid))
        #print(curr_centroid[0])
        centroids[i] = curr_centroid

    #sort centroids here
    #print(centroids)
    centroids = centroids[centroids[:,0].argsort()]
    #print(centroids)

    score_str = ""
    mnist_scorer = MnistScorer()
    
    for i in range(len(centroids)):
        curr_centroid = centroids[i]
        (ch_left, ch_upper, ch_right, ch_lower) = (int(curr_centroid[0] - 14), int(curr_centroid[1] - 19), int(curr_centroid[0] + 14), int(curr_centroid[1] + 19))
        #print((ch_left, ch_upper, ch_right, ch_lower))
        char_crop = score_crop_image.crop((ch_left, ch_upper, ch_right, ch_lower))
        char_crop.save("images/char_crops/{}_{}.png".format(step, str(i)))
        # cv2.imshow('Contours', char_crop) 
        # cv2.waitKey(0) 
        # cv2.destroyAllWindows() 
        tmp_char = mnist_scorer.score(char_crop)
        score_str += tmp_char


    return float(score_str)
        
if __name__ == '__main__' :
    main()