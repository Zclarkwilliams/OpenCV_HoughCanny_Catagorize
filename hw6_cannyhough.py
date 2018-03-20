<<<<<<< HEAD
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
    
    print("Images being read through...")

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

    print("Images processing through canny filter...")

    for i in range(len(imgs)):
        if imgs[i] is not None:
            edge = cv2.Canny(imgs[i], 100, 101)
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
def dilate_fltr(imgs):
    global dilated_list
    global img_diff_list
    img_diff_list = []
    dilated_list = []
    i = 0
    kernel = np.ones((5,5), np.uint8)

    print("Images processing through dilation...")
    
    #   Dilate images
    for i in range(len(imgs)):
        if imgs[i] is not None:
            dilated_img = cv2.dilate(imgs[i], kernel, iterations = 1)
            dilated_list.append(dilated_img)
        else:
            print("ERROR(dilate_fltr()): Image file is 'None' file: " + str(imgs[i]))
            exit
    print("Images processed through dilation successfully.")

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
    i = 0
    if len(og_imgs) == len(fltr_imgs):
        for i in range(len(og_imgs)):
            if og_imgs is not None and fltr_imgs is not None:
                cv2.imshow('image' + str(fltr_imgs[i]), fltr_imgs[i])#img_horizontal_concat)
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
dilate_fltr(img_list)
#print_imgs(img_list, edge_list)

wait_to_close()



# a) Dilation and subtraction to extract edge information
# subtract input img from dilated image:
#edgesImg = imsubtract( dilatedImg, inputImg )
#figure(3), imshow(edgesImg), title('Edges')
#imgComplement = imcomplement(edgesImg)
#figure(4), imshow(imgComplement), title('Edges, complemented image')
=======
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
>>>>>>> c6dc5d46c3a96e562c83e9ab9aaf5fb494c924d1
