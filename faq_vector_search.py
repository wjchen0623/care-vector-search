from llama_index import StorageContext, load_index_from_storage, get_response_synthesizer
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.indices.postprocessor import SimilarityPostprocessor
from llama_index.callbacks import CallbackManager, TokenCountingHandler
import tiktoken

FAQ_INDEX_PATH = "data/ALTY/index_dir/faq_index"
WEB_CONTENT_INDEX_PATH = "data/ALTY/index_dir/web_content_index"

faq_token_counter = TokenCountingHandler(
    tokenizer=tiktoken.encoding_for_model("gpt-3.5-turbo-1106").encode
)

faq_callback_manager = CallbackManager([faq_token_counter])

# load index
faq_storage_context = StorageContext.from_defaults(persist_dir=FAQ_INDEX_PATH)
faq_index = load_index_from_storage(faq_storage_context)

faq_retriever = VectorIndexRetriever(
    index=faq_index,
    similarity_top_k=1,
)

faq_query_engine = RetrieverQueryEngine.from_args(
    retriever=faq_retriever,
    response_mode="no_text",
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.75)],
    CallbackManager=faq_callback_manager
)

## web content
web_content_storage_context = StorageContext.from_defaults(persist_dir=WEB_CONTENT_INDEX_PATH)
web_content_index = load_index_from_storage(web_content_storage_context)

web_content_retriever = VectorIndexRetriever(
    index=web_content_index,
    similarity_top_k=5,
)

response_synthesizer = get_response_synthesizer()

web_content_retriever_engine = RetrieverQueryEngine.from_args(
    retriever=web_content_retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.75)]
)
