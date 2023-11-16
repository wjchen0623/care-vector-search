import streamlit as st
from streamlit.logger import get_logger
import json
import re

LOGGER = get_logger(__name__)

@st.cache_data
def read_json_into_dict(json_path):
   json_dict = json.load(json_path)
   return (json_dict)

def run():
    st.set_page_config(
        page_title="Bot MD Care Vector Search",
        page_icon="👩‍⚕️",
    )

    st.write("## Welcome to Bot MD Care Vector Search")

    st.markdown(
        """
        Demo to showcase what vector search can do for Bot MD Care.
    """
    )

    query = st.text_input('Chat', 'What time are you open?')

    if query is None:
       st.warning("Please enter a query")

    col1, col2, col3 = st.columns(3)

    with col1:
      st.header("Original")
      if query is not None:
         original_dict = read_json_into_dict("data/ALTY/faq/faq_dict_old.json")
         old_query = re.sub(r"\s+", "", query)
         st.write(original_dict[old_query])

    with col2:
      st.header("Vector Search")
      if query is not None:
         st.image("https://static.streamlit.io/examples/cat.jpg")

    with col3:
      st.header("Vector Search + Generative AI")
      if query is not None:
         st.image("https://static.streamlit.io/examples/cat.jpg")


if __name__ == "__main__":
    run()
