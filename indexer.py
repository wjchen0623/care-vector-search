from llama_index import VectorStoreIndex
from llama_index import SimpleDirectoryReader
import os

PERSIST_DIR = "data/ALTY"
FAQ_DIR = os.path.join(PERSIST_DIR, "faq_content")
WEB_CONTENT_DIR = os.path.join(PERSIST_DIR, "web_content")

faq_documents = SimpleDirectoryReader(FAQ_DIR).load_data()
web_documents = SimpleDirectoryReader(WEB_CONTENT_DIR).load_data()

INDEX_DIR = os.path.join(PERSIST_DIR, "index_dir")
if not os.path.exists(INDEX_DIR):
    os.mkdir(INDEX_DIR)

FAQ_INDEX_DIR = os.path.join(INDEX_DIR, "faq_index")
faq_index = VectorStoreIndex.from_documents(faq_documents)
faq_index.storage_context.persist(persist_dir=FAQ_INDEX_DIR)

WEB_CONTENT_INDEX_DIR = os.path.join(INDEX_DIR, "web_content_index")
web_content_index = VectorStoreIndex.from_documents(web_documents)
web_content_index.storage_context.persist(persist_dir=WEB_CONTENT_INDEX_DIR)