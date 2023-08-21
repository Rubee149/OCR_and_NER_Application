import streamlit as st
import os

import spacy
from spacy import displacy

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""


nlp = spacy.load("en_core_web_sm")


def main():
    """ NLP Based App with Streamlit """

    # Title
    st.title("NLPiffy with Streamlit")
    st.subheader("Natural Language Processing On the Go..")

    # Entity Extraction
    if st.checkbox("Show Named Entities"):
        st.subheader("Analyze Your Text")

        message = st.text_area("Enter Text","Type Here ..")

        if st.button("Extract"):
            sen = nlp(message)
            html = displacy.render(sen,style="ent")
            st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)

    st.sidebar.subheader("About App")
    st.sidebar.text("NLPiffy App with Streamlit")
    st.sidebar.info("Cudos to the Streamlit Team")

    st.sidebar.subheader("By")
    st.sidebar.text("Jesse E.Agbe(JCharis)")
    st.sidebar.text("Jesus saves@JCharisTech")

if __name__ == '__main__':
    main()
