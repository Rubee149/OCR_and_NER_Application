# Core Pkgs
import streamlit as st
import tempfile

# NLP Pkgs
import spacy_streamlit
import spacy
#spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')

import os
from PIL import Image
import easyocr
import numpy as np
import cv2



HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""

#name path to image files
image_frames = 'image_frames'
image_frames_OCR = 'image_frames_OCR'


def process(src_vid,frame_iteration):

    #Use an index to integer name the files
    index = 0
    while src_vid.isOpened():
        ret, frame = src_vid.read()
        if not ret:
            break

        #name each frame and save as png
        name = './image_frames/frame' + str(index) + '.png'


        #save every 100th frame
        if index % frame_iteration == 0:
                print('Extracting frames....'+ name)
                cv2.imwrite(name, frame)
        index = index +1
        if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    src_vid.release()
    cv2.destroyAllWindows()

def get_text(Frame_output):
    #for i in os.listdir(image_frames):
        #if st.sidebar.button(str(i)):
             #print(str(i))
             #my_example = Image.open(image_frames+"/"+i)
             #print(my_example)
             Photo = cv2.imread(os.path.join(image_frames,Frame_output))
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
             result_name = './image_frames_OCR/OCR' + Frame_output
             print('Saving results....'+ result_name)
             cv2.imwrite(result_name, Photo)
             image = Image.open(result_name)
             st.image(image, caption = 'OCR Results')
             st.subheader('Extracted Text from Image')
             text =""

             for res in result:
                 text += res[1] + " "
             st.write(HTML_WRAPPER.format(text),unsafe_allow_html=True)
             return(text)


def main():

    st.title("Can I Read?")

    menu = ["OCR","NER","OCR+NER"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "OCR":
        st.header("Optical Character Recognition")
        
        ###Upload or use available video for OCR
        video_file_buffer = st.sidebar.file_uploader("Upload a video", type=["mp4","mov","avi","asf","m4v"])
        DEMO_VIDEO = 'test1.mp4'
        tfile = tempfile.NamedTemporaryFile(suffix='.mp4',delete=False)

        if not video_file_buffer:
            vid = cv2.VideoCapture(DEMO_VIDEO)
            tfile.name = DEMO_VIDEO
            dem_vid = open(tfile.name, 'rb')
            demo_bytes = dem_vid.read()

            st.sidebar.text('Input Video')
            st.sidebar.video(demo_bytes)
        else:
            vid_byte = video_file_buffer.read()
            tfile.write(vid_byte)
            vid = cv2.VideoCapture(tfile.name)
            dem_vid = open(tfile.name, 'rb')
            demo_bytes = dem_vid.read()

            st.sidebar.text('Input Video')
            st.sidebar.video(demo_bytes)



        saved_frames = st.sidebar.number_input('Enter the frame number, you need to iterate (for better performance, Use 100 or above value)',min_value=1,max_value=500)

        if st.sidebar.button('Submit',key='1'):

              if not os.path.exists(image_frames):
                 os.makedirs(image_frames)
              files_in_dir = os.listdir(image_frames)

              for file in files_in_dir:             
                 os.remove(f'{image_frames}/{file}')

              if not os.path.exists(image_frames_OCR):
                 os.makedirs(image_frames_OCR)

              files_in_dir = os.listdir(image_frames_OCR)

              for file in files_in_dir:             
                 os.remove(f'{image_frames_OCR}/{file}')

              process(vid,saved_frames)
              st.sidebar.write('Frames saved......')
              st.sidebar.write('You can Perform OCR on newly generated frames...')


        st.sidebar.write('OCR Model')
        output = []
        for i in os.listdir(image_frames):
            output.append(str(i))
        fra = st.sidebar.selectbox('Select Frame',output)

        if st.sidebar.button('Generate OCR Results',key='2'):
            st.subheader(fra)
            Extracted_frame = Image.open(os.path.join(image_frames,fra))
            st.image(Extracted_frame,'Extracted Frame')
            get_text(fra)

    elif choice == "NER":
         st.header("Named Entity Recognition")
         raw_text = st.text_area("Your Text","Enter Text Here")
         docx = nlp(raw_text)

         spacy_streamlit.visualize_ner(docx,labels=nlp.get_pipe('ner').labels)

    elif choice == "OCR+NER":
         st.header("Optical Character Recognition & Named Entity Recognition")
         ###Upload or use available video for OCR
         video_file_buffer = st.sidebar.file_uploader("Upload a video", type=["mp4","mov","avi","asf","m4v"])
         DEMO_VIDEO = 'test1.mp4'
         tfile = tempfile.NamedTemporaryFile(suffix='.mp4',delete=False)

         if not video_file_buffer:
            vid = cv2.VideoCapture(DEMO_VIDEO)
            tfile.name = DEMO_VIDEO
            dem_vid = open(tfile.name, 'rb')
            demo_bytes = dem_vid.read()

            st.sidebar.text('Input Video')
            st.sidebar.video(demo_bytes)
         else:
            vid_byte = video_file_buffer.read()
            tfile.write(vid_byte)
            vid = cv2.VideoCapture(tfile.name)
            dem_vid = open(tfile.name, 'rb')
            demo_bytes = dem_vid.read()

            st.sidebar.text('Input Video')
            st.sidebar.video(demo_bytes)



         saved_frames = st.sidebar.number_input('Enter the frame number, you need to iterate (for better performance, Use 100 or above value)',min_value=1,max_value=500)
         if st.sidebar.button('Submit',key='1'):
              
              if not os.path.exists(image_frames):
                 os.makedirs(image_frames)
              files_in_dir = os.listdir(image_frames)

              for file in files_in_dir:             
                 os.remove(f'{image_frames}/{file}')

              if not os.path.exists(image_frames_OCR):
                 os.makedirs(image_frames_OCR)

              files_in_dir = os.listdir(image_frames_OCR)

              for file in files_in_dir:             
                 os.remove(f'{image_frames_OCR}/{file}')

              process(vid,saved_frames)
              st.sidebar.write('Frames saved......')
              st.sidebar.write('You can Perform OCR on newly generated frames...')


         st.sidebar.write('OCR Model')
         output = []
         for i in os.listdir(image_frames):
            output.append(str(i))
         fra = st.sidebar.selectbox('Select Frame',output)
         if st.sidebar.button('Generate OCR & NER Results',key='2'):
            st.subheader(fra)
            Extracted_frame = Image.open(os.path.join(image_frames,fra))
            st.image(Extracted_frame,'Extracted Frame')
            OCR_text = get_text(fra)
            st.header("Named Entity Recognition")
            docx = nlp(OCR_text)

            spacy_streamlit.visualize_ner(docx,labels=nlp.get_pipe('ner').labels)

if __name__ == '__main__':
    main()