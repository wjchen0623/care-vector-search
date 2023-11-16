import streamlit as st
from streamlit.logger import get_logger
import json

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Bot MD Care Vector Search",
        page_icon="👩‍⚕️",
    )

    st.write("# Welcome to Bot MD Care Vector Search")
    
    st.markdown(
        """
        Demo to showcase what vector search can do for Bot MD Care.
    """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
      st.header("Original")
      st.image("https://static.streamlit.io/examples/cat.jpg")

    with col2:
      st.header("Enhanced")
      st.image("https://static.streamlit.io/examples/dog.jpg")

    with col3:
      st.header("Generative AI")
      st.image("https://static.streamlit.io/examples/owl.jpg")


if __name__ == "__main__":
    run()
