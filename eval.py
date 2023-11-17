from dotenv import load_dotenv
load_dotenv()
import os
import pandas as pd
import json
from faq_parser import parse_and_generate, parse_and_generate_one
from faq_vector_search import faq_query_engine

PERSIST_DIR = "data/ALTY"
FAQ_PATH = "data/ALTY/faq"
FAQ_CSV_PATH = os.path.join(FAQ_PATH, "Dialogues (Eliza)-ALTY Ortho WhatsApp (1).csv")

with open("data/ALTY/faq/faq_dict_new.json", "r") as file:
    new_dict = json.load(file)

faq_df = pd.read_csv(FAQ_CSV_PATH)
faq_df = faq_df[faq_df['Tags'] == "cleo:alty"].reset_index(drop=True)

faq_df['Trigger Phrases'] = faq_df['Triggers'].apply(lambda x: parse_and_generate(x))

eval_dict = []
for i in range(faq_df.shape[0]):
    for trigger_phrase in faq_df["Trigger Phrases"][i]:
        try:
            vector_search_response = faq_query_engine.query(trigger_phrase)
            if len(vector_search_response.source_nodes) > 0:
                answer = new_dict.get(vector_search_response.source_nodes[0].metadata['file_path'])
            else:
                answer = "Sorry Bot"
        except:
            answer = "Error"
            
        eval_dict.append({
            "Phrase": trigger_phrase,
            "Ground Truth": faq_df["Response"][i],
            "Predicted": answer
        })

eval_df = pd.DataFrame(eval_dict)
eval_df.to_csv("data/ALTY/eval.csv")