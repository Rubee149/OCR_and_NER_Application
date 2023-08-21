import easyocr
import matplotlib.pyplot as plt
import cv2
import time
import numpy as np
#from google.colab.patches import cv2_imshow

reader = easyocr.Reader(['en'],gpu = False)
vid = cv2.VideoCapture("test2.mp4")
#vid = cv2.VideoCapture(0)
skip_frame = True

while(True):
    a = time.time()
    ret, img = vid.read()
    print(img)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    result = reader.readtext(gray)
    text =""

    for res in result:
        text += res[1] + " "
    cv2.putText(img, text, (50,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (50,50,255), 2)

    ##FPS
    b = time.time()
    fps = 1/(b-a)
    cv2.line(img, (20,25), (127,25), [85,45,255], 30)
    cv2.putText(img, f'FPS : {int(fps)}', (11,35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, lineType= cv2.LINE_AA)

    #cv2.imshow("result", img)
    #cv2_imshow(img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    print(fps)
    print(text)




