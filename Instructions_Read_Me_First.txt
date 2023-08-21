First you need to download following packages to your Python Interpreter

pip install opencv-python  ///This package only work with CPU If you want to work with GPU you need to download openCV from Opencv page

pip install spacy          ///NER package (after install you need to download "en_core_web_sm" package by uncomment this line in the code ==> #spacy.cli.download("en_core_web_sm") 

pip install easyocr        ///OCR package
pip install streamlit      ///package for build Python application
pip install spacy-streamlit ///Package for enable spacy features in streamlit


Note:::::: !!!!!!!!!!!!!!
1. If you use VScode, you need to run that external launch.json file to launch the app. Before launch that app you need to connect that json file with streamlit program by mentioning path where streamlit program installed (mentioned in the screenshot(77)).

2. Initially Spacy package didn't work in the Python3.11 interpreter and I change it in to Python3.08 interpreter, then worked really well.

3. This app is basic python application which extract the frames from given video and perform OCR and NER on tha t extracted Frame.( Sorry my computer haven't GPU to run video and perform OCR and NER at same time :D)

And Thanks for Learn this...
(Let's create Something....)
Rubee...