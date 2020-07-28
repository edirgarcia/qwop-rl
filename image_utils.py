from PIL import Image
import cv2
import numpy as np

import datetime


def main():
    
    
    im = Image.open("images/200727_151827.png")

    # The crop method from the Image module takes four coordinates as input.
    # The right can also be represented as (left+width)
    # and lower can be represented as (upper+height).
    (sc_left, sc_upper, sc_right, sc_lower) = (825, 310, 925, 360) 
    (st_left, st_upper, st_right, st_lower) = (725, 410, 1125, 810) 

    # Here the image "im" is cropped and assigned to new variable score_crop
    score_crop = im.crop((sc_left, sc_upper, sc_right, sc_lower))
    
    score_crop.save("images/score_crop.png")
    
    
    state_crop = im.crop((st_left, st_upper, st_right, st_lower))
    
    state_crop.save("images/state_crop.png")
        
        
    image = cv2.imread('images/score_crop.png') 
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
    print("Number of Contours found = " + str(contour_count)) 
      
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
    
    time_stamp = datetime.datetime.now().strftime("%H%M%S")
    
    for i in range(len(centroids)):
        curr_centroid = centroids[i]
        (ch_left, ch_upper, ch_right, ch_lower) = (int(curr_centroid[0] - 14), int(curr_centroid[1] - 19), int(curr_centroid[0] + 14), int(curr_centroid[1] + 19))
        #print((ch_left, ch_upper, ch_right, ch_lower))
        char_crop = score_crop.crop((ch_left, ch_upper, ch_right, ch_lower))
        char_crop.save("images/char_crop_{}.png".format(str(i)+time_stamp))
        
      
    #cv2.imshow('Contours', image) 
    #cv2.waitKey(0) 
    #cv2.destroyAllWindows() 
    
    
        


if __name__ == '__main__':
    main()