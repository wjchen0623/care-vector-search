import re
import os
import pandas as pd
from itertools import product, chain
from utils import create_safe_filename
import json

PERSIST_DIR = "data/ALTY"
FAQ_DIR = os.path.join(PERSIST_DIR, "faq_content")
FAQ_PATH = "data/ALTY/faq"
FAQ_CSV_PATH = os.path.join(FAQ_PATH, "Dialogues (Eliza)-ALTY Ortho WhatsApp (1).csv")

def generate_options_from_str(given_str: str) -> list:
    # Step 1: Extract options
    option_lists = re.findall(r'\[(.*?)\]', given_str)  # Find all bracketed strings
    options = [opt.split(", ") for opt in option_lists]  # Split each string by ', ' to get individual options

    # Step 2: Generate permutations
    permutations = list(product(*options))

    # Step 3: Replace options in the original string
    result = list()
    for perm in permutations:
        temp_str = given_str
        for opt in perm:
            temp_str = re.sub(r'\[(.*?)\]', opt, temp_str, 1)
        result.append(temp_str)

    return result

def parse_and_generate(given_str: str) -> list:
    opts = given_str.split("\n")
    result = [generate_options_from_str(o) for o in opts]
    result = list(chain.from_iterable(result))
    return (result)

def parse_and_generate_one(given_str: str) -> list:
    opts = [given_str.split("\n")[0]]
    result = [generate_options_from_str(o) for o in opts]
    result = list(chain.from_iterable(result))
    return (result)

if not os.path.exists(FAQ_DIR):
    os.mkdir(FAQ_DIR)

faq_df = pd.read_csv(FAQ_CSV_PATH)
faq_df = faq_df[faq_df['Tags'] == "cleo:alty"].reset_index(drop=True)

faq_df['Trigger Phrases One'] = faq_df['Triggers'].apply(lambda x: parse_and_generate_one(x))
faq_df['Trigger Phrases'] = faq_df['Triggers'].apply(lambda x: parse_and_generate(x))

new_faq_dict = {}
faq_dict = {}

for i in range(faq_df.shape[0]):
    file_name = create_safe_filename(faq_df["Tags"][i] + faq_df["Trigger Phrases One"][i][0])
    output_str = "\n".join(faq_df["Trigger Phrases One"][i])
    file_path = os.path.join(FAQ_DIR, file_name)
    with open(file_path, "w") as f:
        f.write(output_str)
    new_faq_dict[file_path] = faq_df['Response'][i]
    for trigger_phrase in faq_df["Trigger Phrases"][i]:
        trigger_phrase_no_space = re.sub(r"\s+", "", trigger_phrase)
        faq_dict[trigger_phrase_no_space] = faq_df['Response'][i]

with open(os.path.join(FAQ_PATH, "faq_dict_old.json"), 'w') as f:
    json.dump(faq_dict, f, indent=4)

with open(os.path.join(FAQ_PATH, "faq_dict_new.json"), "w") as f:
    json.dump(new_faq_dict, f, indent=4)
