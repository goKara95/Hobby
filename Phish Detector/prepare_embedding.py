import time
from googletrans import Translator
import os
import trafilatura
import numpy as np
import pickle
import argparse
from sentence_transformers import SentenceTransformer
import torch


def process_htmls():
    # We saved parsed htmls and translated htmls since embedding could take a while
    cwd = os.path.dirname(__file__)
    legit_path = os.path.join(cwd, "Legitimate")
    phish_path = os.path.join(cwd, "Phishing")
    legitimate_file = os.path.join(cwd, 'legitimate_arrays.npy')
    phish_file = os.path.join(cwd, 'phishing_arrays.npy')
    # Check if legitimate and phishing arrays exist(parsed and saved version of html.txt's)
    if os.path.exists(legitimate_file) and os.path.exists(phish_file):
        legitimate_array = np.load(legitimate_file, allow_pickle=True)
        phish_array = np.load(phish_file, allow_pickle=True)

    else:
        legitimate_array = parsing(legit_path)
        np.save(legitimate_file, legitimate_array)
        phish_array = parsing(phish_path)
        np.save(phish_file, phish_array)
    return [legitimate_array, phish_array]


def parsing(folder_path):
    # Empty array with 30k elements created to eliminate memory allocation when the array gets too big
    arr = np.empty(30000, dtype=object)
    i = 0
    for filename in os.listdir(folder_path):
        if filename.endswith("_html.txt"):
            file_path = os.path.join(folder_path, filename)
            # Some files can only be read with windows-1254 so a try except block is added
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    html_content = file.read()
            except UnicodeError:
                with open(file_path, "r", encoding="windows-1254") as file:
                    html_content = file.read()
            try:
                result = trafilatura.extract(html_content, include_comments=False,
                                             include_tables=False, no_fallback=True)
                if result is not None:
                    arr[i] = result

            except Exception as e:
                # Print the error message and continue with the next iteration
                print(f"Error processing {filename}: {e}")
                continue
            print("ITERATION: ", i)
            i += 1
    # drop nones before returning
    filtered_array = arr[arr != None]
    return filtered_array


def translate(array, html_type):
    cwd = os.path.dirname(__file__)
    translated_path = os.path.join(cwd, f"translated{html_type}.npy")
    if os.path.exists(translated_path):
        return np.load(translated_path, allow_pickle=True)
    translator = Translator()
    for i in range(0, len(array)):
        sentence = array[i]
        if len(sentence) > 10000:
            # Split the sentence into chunks of 10,000 characters since google translate api's char limit
            chunks = [sentence[k:k + 10000] for k in range(0, len(sentence), 10000)]
            translated_chunks = []
            for chunk in chunks:
                try:
                    chunk_trans = translator.translate(chunk)
                    translated_chunks.append(chunk_trans.text)
                except:
                    time.sleep(0.35) # Since the API can sometimes throw connection timeout, sleep function is called after each translation
                    pass
            translation = ''.join(translated_chunks)
            array[i] = translation
        else:
            try:
                translation = translator.translate(sentence)
                array[i] = translation.text
            except:
                time.sleep(0.35)
                pass
        if i == (len(array)-1):
            np.save(f"translated{html_type}.npy", array)
    return array


parser = argparse.ArgumentParser()
parser.add_argument('-transformer', choices=['xlm-roberta', 'sbert'], required=True)
args = parser.parse_args()

parsed_htmls = process_htmls()
parsed_legit = parsed_htmls[0]
parsed_phish = parsed_htmls[1]
translated_legit = translate(parsed_legit, "Legit")
translated_phish = translate(parsed_phish, "Phish")

if torch.cuda.is_available():
    device = torch.cuda.current_device()
    print("Current GPU:", torch.cuda.get_device_name(device))
else:
    print("CUDA is not available")
    device = None

# iterate through parsed htmls, store legit and phish html's in different arrays
# add 1(phish) or 0(legit) in each embedded html ie: [1.45, .... 0.07] will become [1, 1.45, ..... 0.07]
# concatenate both arrays and save it
if args.transformer == "xlm-roberta":
    embeddings_folder = 'embeddings'
    os.makedirs(embeddings_folder, exist_ok=True)
    e_f_name = os.path.join(embeddings_folder, "embeddings-xml-roberta.pkl")
    model = SentenceTransformer('aditeyabaral/sentencetransformer-xlm-roberta-base', device=device)
    embeddings_legit = []
    embeddings_phish = []
    for num, each_sentence in enumerate(parsed_legit, start=1):
        print(f"Processing sentence {num}")
        sentence_embedding = model.encode(each_sentence)
        embeddings_legit.append(sentence_embedding)

    for num, each_sentence in enumerate(parsed_phish, start=1):
        print(f"Processing sentence {num}")
        sentence_embedding = model.encode(each_sentence)
        embeddings_phish.append(sentence_embedding)
    embeddings_legit = np.insert(embeddings_legit, 0, 0, axis=1)
    embeddings_phish = np.insert(embeddings_phish, 0, 1, axis=1)
    embeddings = np.concatenate((embeddings_legit, embeddings_phish), axis=0)
    with open(e_f_name, 'wb') as f:
        pickle.dump(embeddings, f)

elif args.transformer == "sbert":
    embeddings_folder = 'embeddings'
    os.makedirs(embeddings_folder, exist_ok=True)
    e_f_name = os.path.join(embeddings_folder, "embeddings-sbert.pkl")
    model = SentenceTransformer('sentence-transformers/bert-base-nli-mean-tokens', device=device)
    embeddings_legit = []
    embeddings_phish = []
    for num, each_sentence in enumerate(translated_legit, start=1):
        print(f"Processing sentence {num}")
        sentence_embedding = model.encode(each_sentence)
        embeddings_legit.append(sentence_embedding)

    for num, each_sentence in enumerate(translated_phish, start=1):
        print(f"Processing sentence {num}")
        sentence_embedding = model.encode(each_sentence)
        embeddings_phish.append(sentence_embedding)
    embeddings_legit = np.insert(embeddings_legit, 0, 0, axis=1)
    embeddings_phish = np.insert(embeddings_phish, 0, 1, axis=1)
    embeddings = np.concatenate((embeddings_legit, embeddings_phish), axis=0)
    with open(e_f_name, 'wb') as f:
        pickle.dump(embeddings, f)
