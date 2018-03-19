#! Python 3
import os
import cv2
import numpy as np
import array as array
from pathlib import Path
from matplotlib import pyplot as plt

zack_path_ext = "C:/Users/Zachary/Documents/A School/ECE578-9_IntelligentRobotics_1-2/HW_6_CannyHough/pics"

#path = "C:/Users" + zack_path_ext
#path = os.path.realpath(path)
#os.startfile(path)

directory = os.fsencode(zack_path_ext)
kernel = np.ones((5,5),np.uint8)
dilatedimgs = []
imgs = []
edges = []

for file in os.listdir(directory):
   #    Decode the filename from the file system
    filename = os.fsdecode(file)
    
    #   Proceed through all 'jpeg' files in folder with
    if filename.endswith(".jpg"):
        print(filename)
        #   load the image file
        img = cv2.imread(filename,0)
        imgs.append(img)
        #   perform canny edge detection process
        edge = cv2.Canny(img,100,110)
        edges.append(edge)
        #   dilate the image and generate morphological graph
        dilatedimg = cv2.dilate(img, kernel, iterations = 1)
        dilatedimgs.append(dilatedimg)
        continue
    else:
        print("All Files Loaded and Run")

# a) Dilation and subtraction to extract edge information

#imjesus = cv2.imread(imgfile,0)
#se = strel('square', 5);                            # structuring element
#dilatedimg = cv2.dilate(img[0], kernel, iterations = 1)                # Dilate input image
#figure(2), imshow(dilatedImg), title('Dilated')
# subtract input img from dilated image:
#edgesImg = imsubtract( dilatedImg, inputImg )
#figure(3), imshow(edgesImg), title('Edges')
#imgComplement = imcomplement(edgesImg)
#figure(4), imshow(imgComplement), title('Edges, complemented image')


'''
j = 0
while j < len(imgs):
    #   Generate image graph for the original image
    plt.subplot(2,1,1),plt.imshow(imgs[j],cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    #   Generate iamge graph for the canny transform
    plt.subplot(2,1,2),plt.imshow(edges[j],cmap = 'gray')
    plt.title('Canny Edge Detection'), plt.xticks([]), plt.yticks([])
    #   Print image graphs generated
    plt.show()
    j += 1

'''