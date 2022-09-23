import progressbar
import numpy as np
import matplotlib.pyplot as plt
from sys import platform
import cv2

class ImageMetaData(object):
    def __init__(self):
        self.roi = []
        self.shape = {'width':0, 'height': 0}

    def __str__(self):
        return str(self.__class__) + ": "+ str(self.__dict__)


showframes = True

#######################################################################################
def scanandStore():
    input_dir = '1.mp4'
    video_obj = cv2.VideoCapture(0)
    #totalFrames = int(video_obj.get(cv2.CAP_PROP_FRAME_COUNT))
    totalFrames = 30000
    #bar = progressbar.ProgressBar(maxval=totalFrames).start()
    fig = plt.gcf()
    fig.canvas.set_window_title('Video')
    centroid = {'x': 0, 'y': 0}
    success = True
    count = 0
    list_of_Frames = []

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

        ROi = image_rot[0:rows, int(centroid['x']):int(centroid['x']+3)].copy()
        image_metadata.roi = ROi
        list_of_Frames.append(image_metadata)
        image_t = image_rot.copy()
        image_t = cv2.cvtColor(image_t, cv2.COLOR_BGR2RGB)

        video_height = list_of_Frames[0].shape['height']
        video_width = list_of_Frames[0].shape['width']

        if showframes:
            start_point = (int(centroid['x']), 0)
            end_point = (int(centroid['x']), video_height)
            color = (255, 0, 0)
            thickness = 10
            image_rot_line = cv2.line(image_rot, start_point, end_point, color, thickness)


            if count > 0:
                fig.set_data(image_rot_line)
                plt.title("frame {0}".format(count))
                plt.draw()
                plt.pause(0.0001)
            else:
                fig = plt.imshow(image_t)
                plt.title("frame {0}".format(count))
                plt.draw()
                plt.pause(0.0001)

        count += 1
        #bar.update(count)

    #bar.finish()



    flatImage = np.empty((video_height, len(list_of_Frames), 3), np.uint8)
    result = []

    for n, im in enumerate(list_of_Frames, start=0):
        image1 = list_of_Frames[n].roi
        colROi = image1[:, int(image1.shape[1]/2)]. copy()
        flatImage[:, n] = colROi

        if(n+1 < len(list_of_Frames)):
            image2 = list_of_Frames[n+1].roi
            image1_roi = image1.copy()
            image2_roi = image2.copy()

            if n > 0:
                stitched_image = numpy_horizontal_concat = np.concatenate((result, image2_roi), axis=1)
            else:
                stitched_image = np.concatenate((image1_roi, image2_roi),axis = 1)

            result = stitched_image

    dsize = (video_width, video_height)
    #result = cv2.resize(result, dsize)
    cv2.imwrite("Result.jpg", result)
    return result


#Main Program
if __name__ == '__main__':
    print(" ")
    print("Start")
    print("**********")
    result = scanandStore()