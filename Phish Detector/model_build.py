import os
import matplotlib.pyplot as plt
import numpy as np
import pickle
import argparse
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from xgboost import XGBClassifier
from catboost import CatBoostClassifier

parser = argparse.ArgumentParser()
parser.add_argument('-algorithm', choices=['xgb', 'cat'], required=True)
parser.add_argument('-embeddingfile', required=True)
args = parser.parse_args()

file_path = os.path.join(os.getcwd(), args.embeddingfile)

# Read the embeddings file
with open(file_path, "rb") as f:
    dataset = pickle.load(f)

# Convert the dataset to a numpy array
dataset = np.array(dataset)

X = dataset[:, 1:]  # Embeddings with target value removed
y = dataset[:, 0]   # Target value phishing = 1, legitimate = 0

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

if args.algorithm == "xgb":
    classifier = XGBClassifier()
elif args.algorithm == "cat":
    classifier = CatBoostClassifier()

classifier.fit(X_train, y_train)
predictions = classifier.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)


# Print evaluation metrics
print("Accuracy: ", accuracy)
print("Precision: ", precision)
print(f"Recall: ", recall)

# Save the model
model_folder = 'model'
os.makedirs(model_folder, exist_ok=True)
if "sbert" in args.embeddingfile:
    embeddingtype = "sbert"
else:
    embeddingtype = "xlmroberta"
# Save the model as a pickle file in the 'model' folder
model_filename = os.path.join(model_folder, f"{embeddingtype}_{args.algorithm}boost_model.pkl")
with open(model_filename, 'wb') as model_file:
    pickle.dump(classifier, model_file)

print(f"Model saved as {model_filename}")
