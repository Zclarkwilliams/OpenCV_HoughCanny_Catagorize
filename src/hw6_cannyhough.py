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
RGB = 0
GRY = 1
LINES = 0
PROB = 1
POINTS = 2
CIRCLES = 3

'''^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
load_imgs(diledir)
    Load all the files from the provided folder 
    inputs
        file directory -> string type path variable
            file type to load -> .jpg
    output
        imgfile -> list of files loaded from directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'''
def load_imgs(file_dir):
    global img_file
    img_file = []
    i = 0

    print("Loading images from file...")

    for file in os.listdir(file_dir):
        #    Decode the filename from the file system
        filename = os.fsdecode(file)
        if filename.endswith(".jpg"):
            img_file.append(zack_path_ext + "/" + filename)
        else:
            print("ERROR: Incorrect File Type File: " + filename)
            exit
    global img_list
    img_list = []
    i = 0
    for i in range(len(img_file)):
        img = cv2.imread(img_file[i])
        r = 100.0 / img.shape[1]
        dim = (100, int(img.shape[0] * r))
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        img_list.append(resized)
    print("Images loaded successfully.")

'''^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
read_imgs(imagefile)
    Read in all loaded files as images to a list
    input
        imagefile   -> list of loaded image files from load_imgs(directory)
        loadtype    -> chose to process image as grayscale, rgb, or other
    output
        img_list -> list of read images 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'''
def read_imgs(image_file):
    global img_list
    img_list = []
    i = 0
    
    print("Reading images through...")

    for i in range(len(img_file)):
        img = cv2.imread(img_file[i])

        #   Add image to list
        img_list.append(img)

    print("Images read successfully.")

'''^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
canny_fltr(imgs)
    Apply Canny edge detection from OpenCV3 to a read-in image
    input 
        imgs -> list of read-in images from read_imgs()
    output
        edge_list -> list of images with edges detected with canny filtering
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'''
def canny_fltr(imgs):
    global edge_list
    edge_list = []
    i = 0
    j = 0

    #   Threshold values for edge detection of Canny Filter
    min_thresh = 50
    max_thresh = 200

    print("Processing images through canny filter...")

    for i in range(len(imgs)):
        if imgs[i] is not None:
            #   Convert the image to greyscale for processing
            img = cv2.cvtColor(imgs[i],cv2.COLOR_BGR2GRAY)

            #   Process through canny edge detection filter
            edge = cv2.Canny(img, min_thresh, max_thresh, apertureSize = 3)
            edge_list.append(edge)
        else:
            print("ERROR(canny_fltr()): Image file is 'None' file: " + str(imgs[i]))
            exit

    print("Images processed through Canny filter successfully.")

'''^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
dilate_fltr(imgs)
    Apply dilation filter/effect from OpenCV3 to a read-in image
    input 
        imgs -> list of read-in images from read_imgs()
    output
        dilated_list -> list of images that have been dilated through OpenCV
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'''
def dilate_fltr(imgs, subs):
    global dilated_list
    global img_diff_list
    img_diff_list = []
    img_diff = []
    dilated_list = []
    i = 0
    
    #   Setup kernel for dialtion processing
    kern_size = (5,5)
    kernel = np.ones(kern_size, np.uint8)

    print("Dilation of images processing...")
    
    #   Dilate images
    for i in range(len(imgs)):
        if imgs[i] is not None:
            #   Dilate the image on a 5x5 kernel 
            dilated_img = cv2.dilate(imgs[i], kernel, iterations = 1)
            dilated_list.append(dilated_img)
        else:
            print("ERROR(dilate_fltr()): Image file is 'None' file: " + str(imgs[i]))
            exit
    print("Images processed through dilation successfully.")

    #   Subtract original image from dilated image
    if subs == True:
        print("Dilated images seperating from original image...")
        j = 0
        for j in range(len(dilated_list)):
            if dilated_list[j] is not None:
                #   Convert lists to numpy array for subtraction operation
                #   Subract src2 from src1 assign to numpy array (img_diff = src1 - src2)
                img_diff = (dilated_list[j] - imgs[j])
                img_diff_list.append(img_diff)
        print("Original image removed from dilated transformation successfully.")

'''^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
hough_fltr(img_edges)
    Apply Hough transofrm with a line detectiong to image that is read-in.
    The image list fed in is expected to be run through the canny filter 
    first, canny_fltr(). Hough lines filter/effect from OpenCV3.
    input 
        img_edges -> list of images from already processed through Canny
        trans_type -> chose transform function type
                            HoughLines
                            HoughLinesP
                            HoughLinesPoint_Set
                            HoughCircles
                            
    output
        hough_list -> list of images with hough line detection applied
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'''
def hough_fltr(og_imgs, img_edges, trans_type):
    global hough_list
    hough_list = []
    i = 0

    #   Set parameters
    minLineLength = 500
    maxLineGap = 10
    ctheta = np.pi/180
    linethresh = 200
    thresh = 750
    rho = 1
    numlines = 100
    linewidth = 2
    green = 0
    blue = 255
    red = 255

    print("Processing Lough line detection transform...")

    for i in range(len(img_edges)):
        if img_edges[i] is not None:
            #   Set copy of original images to integrate lines in
            img = og_imgs[i]

            if trans_type == PROB:       #   Hough Lines Probabilistic Function
                #   Derived probabalistic line points
                lines = cv2.HoughLinesP(img_edges[i],rho,ctheta,thresh,minLineLength,maxLineGap)
                #   Process the lines derived and apply to image
                for line in lines:
                    x1,y1,x2,y2 = line[0]
                    cv2.line(img,(x1,y1),(x2,y2),(blue,green,red),linewidth)

            elif trans_type == POINTS:    #   Hough Lines Point Set Function
                print("ERROR: Point cloud functionality not setup yet. (hough_fltr())")
                #lines = cv2.HoughLinesPointSet()

            elif trans_type == CIRCLES:  #   Hough Cirles Function
                print("ERROR: Circles functionality not setup yet. (hough_fltr())")
                #lines = cv2.HoughCircles()
            
            elif trans_type == LINES:    #   Default to process as HoughLines function
                lines = cv2.HoughLines(img_edges[i],rho,ctheta,linethresh,numlines)
                for line in lines:
                    rho,theta = line[0]
                    a = np.cos(theta)
                    b = np.sin(theta)
                    x0 = a*rho
                    y0 = b*rho
                    x1 = int(x0 + 1000*(-b))
                    y1 = int(y0 + 1000*(a))
                    x2 = int(x0 - 1000*(-b))
                    y2 = int(y0 - 1000*(a))

                    cv2.line(img,(x1,y1),(x2,y2),(blue,green,red),linewidth)

            else:   #   Error control for transform type
                print("ERROR: Invalid transform type entered. (hough_fltr())")
            
            #   Add edited image to the array of images
            hough_list.append(img)

            #   Save image with lines integrated
            #cv2.imwrite('houghlines' + str(i) + '.jpg', img)

        else:   #   
            print("ERROR: File number %s from filter imaged loaded was empty. (hough_fltr())" + str(i))

'''^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
print_imgs(og_imgs, fltr_imgs)
    Print the images, 1 original with its filtered counterpart
    input
        imgs      -> list of originally loaded images for comparative perspective
        fltr_imgs -> list of filtered or altered images
    output
        NONE -> This will diplay images in external window so there should be no 
               output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'''
def print_imgs(imgs, fltr_imgs):

    print("Plotting filtered and original iamges...")

    i = 0
    if len(imgs) == len(fltr_imgs):
        for i in range(len(imgs)):
            if imgs is not None and fltr_imgs is not None:
                plt.figure()
                a1 = plt.subplot(1,2,1)
                a1.imshow(fltr_imgs[i])
                plt.axis('off')
                a1.set_title('Filtered Image ' \
                              + str(i) \
                              + " of " \
                              + str(len(fltr_imgs) + 1))
                a2 = plt.subplot(1,2,2)
                a2.imshow(imgs[i])
                plt.axis('off')
                a2.set_title('Original Image ' \
                              + str(i) \
                              + " of " \
                              + str(len(imgs)))
                plt.show()
            else:
                print("ERROR(print_imgs()): Image file is 'None' original image file: " \
                       + imgs[i] \
                       + " and filtered file " \
                       + fltr_imgs[i])
                exit
    else:
        print("ERROR(print_imgs()): The loaded the input file lists are not the same length." \
              + " Original image list length: " + str(len(imgs) + 1) \
              + " Filtered image list length: " + str(len(fltr_imgs)))
        exit

'''^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
wait_to_close()
    This function will pause the system and wait for the 'esc' key to be 
    pushed before closing any windows and exiting the system
    input
        NONE
    output
        NONE
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'''
def wait_to_close():
    print("Press 'esc' to close windows")
    #   Wait to close the windows
    key = cv2.waitKey(0)
    if key == 27: # escape
        print("Closing all windows now.")
        #   Close all opened image graph windows
        cv2.destroyAllWindows()

'''^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    MAIN Function call and script run section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'''
#   Load the image files
load_imgs(directory)

#   Read in images / encode as bitmap
read_imgs(img_file)

#   Apply Canny Transform filtering to the read image/bitmap
canny_fltr(img_list)

#   Dilate and differentiate the image with noise
dilate_fltr(edge_list, False)

#   Apply Hough transform for line/circle/point/lineprobabalistic image analysis
'''
houghtype = input("\n\nWhich Hough trans type; Lines(l), LineProbability(lp), Circles(c), Points(p): ")
if houghtype == 'p' or houghtype == 'P':
    hough_fltr(img_list, edge_list, POINTS)
elif houghtype == 'lp' or houghtype == 'LP':
    hough_fltr(img_list, edge_list, PROB)
elif houghtype == 'c' or houghtype == 'C':
    hough_fltr(img_list, edge_list, CIRCLES)
else:   # Default type LINES
    hough_fltr(img_list, edge_list, LINES)
'''
hough_fltr(img_list, dilated_list, PROB)

#   Print the image files, both original and transformed/filtered images
print_imgs(img_list, hough_list)

#   Wait to close system 
wait_to_close()
