from cgitb import reset
from turtle import width
#import progressbar
import numpy as np
import matplotlib.pyplot as plt
import cv2
import time

rollerRadius = 20 #mm
RPM = 0
MAX_SPEED = 30 #mm/s
MAX_DELAY = 5 #ms
SENSOR_READ = True

class ImageMetaData(object):
    def __init__(self):
        self.roi = []
        self.shape = {'width': 0, 'height': 0}

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

def calcTimer(RPM):
    speedW = (2*3.14*RPM)/60
    speed = speedW * rollerRadius
    timer = ((MAX_SPEED-speed)/MAX_SPEED) * MAX_DELAY
    return timer
    # return timer in sleep function in the scan function



def scan():
    input_dir = '1.mp4'
    input_cam = 0
    video_obj = cv2.VideoCapture(input_cam)
    #totalFrames = int(video_obj.get(cv2.CAP_PROP_FRAME_COUNT))
    fig = plt.gcf()
    #fig.canvas.set_window_title('Video')
    centroid = {'x': 0, 'y': 0}
    success = True
    count = 0
    list_of_Frames = []

    x = 1


    while success:
        image_metadata = ImageMetaData()
        success, image = video_obj.read()
        
        if not success:
            continue
        if image is None:
            continue
        if np.sum(image) == 0:
            continue
        #image_rot = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        image_rot = image

        rows, cols = image_rot.shape[:2]
        image_metadata.shape['width'] = cols
        image_metadata.shape['height'] = rows

        if count == 0:
            centroid['x'] = cols/2
            centroid['y'] = rows/2
        
        ROi = image_rot[0:rows, int(centroid['x']) : int(centroid['x']+1)].copy()

        lineofpixels = np.array(image_rot[0:rows, int(centroid['x']) : int(centroid['x']+3)].copy())
        if x == 1:
            lineofpixelsprev = np.empty_like(lineofpixels)
            lineofpixelsprev = lineofpixels.copy()
            x = 2

        if((lineofpixels == lineofpixelsprev).all()):
            print("skip")
            continue
        else:
            print("ok")

        #print(lineofpixels)
        image_metadata.roi = ROi
        list_of_Frames.append(image_metadata)
        image_t = image_rot.copy()
        #image_t = cv2.cvtColor(image_t, cv2.COLOR_BGR2RGB)
        count += 1

        lineofpixelsprev = lineofpixels

        if count == 300:
            break


    return list_of_Frames
        


    

def store(list_of_Frames):
    video_height = list_of_Frames[0].shape['height']
    video_width = list_of_Frames[0].shape['width']
    flatImage = np.empty((video_height , len(list_of_Frames), 3), np.uint8)
    result = []

    for n, im in enumerate(list_of_Frames, start = 0):
        image1 = list_of_Frames[n].roi
        colROi = image1[:, int(image1.shape[1]/2)].copy()
        flatImage[:, n] = colROi

        if(n+1 < len(list_of_Frames)):
            image2 = list_of_Frames[n+1].roi
            image1_roi = image1.copy()
            image2_roi = image2.copy()

            if n > 0:
                stitched_image = np.concatenate((result, image2_roi), axis = 1)
            else:
                stitched_image = np.concatenate((image1_roi, image2_roi), axis = 1)

            result = stitched_image
    
    dsize = (video_width, video_height)
    #result = cv2.resize(result, dsize)
    cv2.imwrite("Result.jpg", result)
    return result



if __name__ == '__main__':
    print("**********************")
    print("START")
    print("**********************")

    listOfFrames = scan()
    result = store(listOfFrames)

