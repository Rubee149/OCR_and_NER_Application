from PIL import Image
import easyocr
#from wand.image import Image as Img

import numpy as np
import os
import cv2

#name path to image files
image_frames = 'image_frames'
image_frames_OCR = 'image_frames_OCR'

def files():

    try:
        os.remove(image_frames)
        os.remove(image_frames_OCR)
    except OSError:
        pass

    if not os.path.exists(image_frames):
        os.makedirs(image_frames)

    if not os.path.exists(image_frames_OCR):
        os.makedirs(image_frames_OCR)

    #specify the source video path
    src_vid = cv2.VideoCapture("test2.mp4")
    return(src_vid)

def process(src_vid):

    #Use an index to integer name the files
    index = 0
    while src_vid.isOpened():
        ret, frame = src_vid.read()
        if not ret:
            break

        #name each frame and save as png
        name = './image_frames/frame' + str(index) + '.png'

        #save every 100th frame
        if index % 100 == 0:
            print('Extracting frames....'+ name)
            cv2.imwrite(name, frame)
        index = index +1
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    src_vid.release()
    cv2.destroyAllWindows()

def get_text():
    for i in os.listdir(image_frames):
        #print(str(i))
        #my_example = Image.open(image_frames+"/"+i)
        #print(my_example)
        Photo = cv2.imread(os.path.join(image_frames,str(i)))
        #print(Photo)
        #cv2.imshow('',Photo[1])
        #cv2.waitKey(10000)

        reader = easyocr.Reader(['en'],gpu = False)
        #gray = cv2.cvtColor(Photo, cv2.COLOR_RGB2GRAY)
        result = reader.readtext(Photo)
        for detection in result:
            top_left = tuple([int(val) for val in detection[0][0]])
            bottom_right = tuple([int(val) for val in detection[0][2]])
            word = detection[1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            Photo = cv2.rectangle(Photo,top_left, bottom_right, (0,255,0), 5)
            Photo = cv2.putText(Photo,word, top_left, font, 1, (0,255,255),2,cv2.LINE_AA)
        #print(result)
        result_name = './image_frames_OCR/OCR' + str(i)
        print('Saving results....'+ result_name)
        cv2.imwrite(result_name, Photo)

        text =""

        for res in result:
            text += res[1] + " "
        print(text)

#main driver
if __name__=='__main__':
    vid = files()
    process(vid)
    get_text()