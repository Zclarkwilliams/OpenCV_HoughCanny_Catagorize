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

'''^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
load_imgs(diledir)
    Load all the files from the provided folder 
    inputs
        file directory -> string type path variable
            file type to load -> .jpg
    output
        imgfile -> list of files loaded from directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'''
def load_imgs(filedir):
    global imgfile
    imgfile = []
    i = 0

    print("Loading images from file...")

    for file in os.listdir(filedir):
        #    Decode the filename from the file system
        filename = os.fsdecode(file)
        if filename.endswith(".jpg"):
            imgfile.append(zack_path_ext + "/" + filename)
        else:
            print("ERROR: Incorrect File Type File: " + filename)
            exit
    global img_list
    img_list = []
    i = 0
    for i in range(len(imgfile)):
        img = cv2.imread(imgfile[i])
        r = 100.0 / img.shape[1]
        dim = (100, int(img.shape[0] * r))
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        img_list.append(resized)
    print("Images loaded successfully.")


'''^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
read_imgs(imagefile)
    Read in all loaded files as images to a list
    input
        imagefile -> list of loaded image files from load_imgs(directory)
    output
        img_list -> list of read images 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'''
def read_imgs(imagefile):
    global img_list
    img_list = []
    i = 0
    
    print("Reading images through...")

    for i in range(len(imgfile)):
        img = cv2.imread(imgfile[i])
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

    #   Threshold values for edge detection of Canny Filter
    min_thresh = 100
    max_thresh = 200

    print("Processing images through canny filter...")

    for i in range(len(imgs)):
        if imgs[i] is not None:
            #   Process through canny edge detection filter
            edge = cv2.Canny(imgs[i], min_thresh, max_thresh)
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
    if subs == 1:
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
print_imgs(og_imgs, fltr_imgs)
    Print the images, 1 original with its filtered counterpart
    input
        og_imgs   -> list of originally loaded images for comparative perspective
        fltr_imgs -> list of filtered or altered images
    output
        NONE -> This will diplay images in external window so there should be no 
               output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'''
def print_imgs(og_imgs, fltr_imgs):

    print("Plotting filtered and original iamges...")

    i = 0
    if len(og_imgs) == len(fltr_imgs):
        for i in range(len(og_imgs)):
            if og_imgs is not None and fltr_imgs is not None:
                plt.figure()
                a1 = plt.subplot(1,2,1)
                a1.imshow(fltr_imgs[i])
                plt.axis('off')
                a1.set_title('Filtered Image ' \
                              + str(i) \
                              + " of " \
                              + str(len(fltr_imgs)))
                a2 = plt.subplot(1,2,2)
                a2.imshow(og_imgs[i])
                plt.axis('off')
                a2.set_title('Original Image ' \
                              + str(i) \
                              + " of " \
                              + str(len(og_imgs)))
                plt.show()
            else:
                print("ERROR(print_imgs()): Image file is 'None' original image file: " \
                       + og_imgs[i] \
                       + " and filtered file " \
                       + fltr_imgs[i])
                exit
    else:
        print("ERROR(print_imgs()): The loaded the input file lists are not the same length.")
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
load_imgs(directory)
read_imgs(imgfile)
canny_fltr(img_list)
dilate_fltr(edge_list, 0)
print_imgs(img_list, img_diff_list)#edge_list)

wait_to_close()



# a) Dilation and subtraction to extract edge information
# subtract input img from dilated image:
#edgesImg = imsubtract( dilatedImg, inputImg )
#figure(3), imshow(edgesImg), title('Edges')
#imgComplement = imcomplement(edgesImg)
#figure(4), imshow(imgComplement), title('Edges, complemented image')
