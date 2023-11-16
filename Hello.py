import streamlit as st
from streamlit.logger import get_logger
import json
import re
import os
from faq_vector_search import faq_query_engine, web_content_retriever_engine

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Bot MD Care Vector Search",
        page_icon="👩‍⚕️",
    )

    if "OPENAI_API_KEY" not in os.environ:
       os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

    @st.cache_data
    def read_json_into_dict(json_path):
      json_dict = json.load(json_path)
      return (json_dict)

    with open("data/ALTY/faq/faq_dict_old.json", "r") as file:
      original_dict = read_json_into_dict(file)

    with open("data/ALTY/faq/faq_dict_new.json", "r") as file:
      new_dict = read_json_into_dict(file)
    
    with open("data/ALTY/web_content_mapping.json", "r") as file:
       file2source = read_json_into_dict(file)

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
      st.subheader("Original")
      if query is not None:
         old_query = re.sub(r"\s+", "", query)
         old_reply = original_dict.get(old_query, "")
         if old_reply == "":
            st.write("Sorry Bot")
         else:
            st.write(original_dict[old_query])

    with col2:
      st.subheader("Vector Search")
      if query is not None:
         vector_search_response = faq_query_engine.query(query)
         if len(vector_search_response.source_nodes) == 0:
            st.write("Sorry Bot")
         else:
            st.write(new_dict[vector_search_response.source_nodes[0].metadata['file_path']])

    with col3:
      st.subheader("Vector Search + Generative AI")
      if query is not None:
         if len(vector_search_response.source_nodes) == 1:
            st.write(new_dict[vector_search_response.source_nodes[0].metadata['file_path']])
         else:
            web_content_search_result = web_content_retriever_engine.query(query)
            st.write(web_content_search_result.response)
            st.write("\nSources:\n")
            for node in web_content_search_result.source_nodes:
               st.write(file2source.get(node.metadata['file_path']))


if __name__ == "__main__":
    run()
