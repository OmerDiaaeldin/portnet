#CHECKING FOR THE 2ND STEP IN THE FRAUD DETECTION

import pandas as pd
import numpy as np
import string
from sentence_transformers import SentenceTransformer

# Load BERT model for sentence embeddings
bert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# File paths
invoices_file_path = "/home/odaio/dev/portnet/back/data/Invoices.csv"  # Replace with actual file path
hs_codes_file_path = "/home/odaio/dev/portnet/back/data/HS_Codes.csv"  # Replace with actual file path

# Load data
invoices_df = pd.read_csv(invoices_file_path)
hs_codes_df = pd.read_csv(hs_codes_file_path)

# Function to normalize descriptions (lowercase, strip spaces, remove punctuation)
def normalize_text(text):
    if pd.isna(text) or text.strip() == "":
        return ""  # Return empty string if NaN or blank
    text = text.lower().strip().translate(str.maketrans("", "", string.punctuation))
    return text

# Function to compute BERT embeddings for a sentence
def get_bert_embedding(text):
    if text.strip() == "":
        return np.zeros(384)  # Return zero vector if text is empty
    return bert_model.encode([text])[0]

valid_hs_codes = set(hs_codes_df["HS Code"])

# Function to compute cosine similarity between two embeddings
def cosine_similarity(vec1, vec2):
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0  # Return similarity of 0 if either vector is empty
    return np.dot(vec1, vec2) / (norm1 * norm2)

# Function for token-based matching
def token_match(desc1, desc2):
    tokens1 = set(desc1.split())
    tokens2 = set(desc2.split())
    if not tokens1 or not tokens2:
        return 0  # Return 0 if either description is empty
    common_tokens = tokens1.intersection(tokens2)
    return len(common_tokens) / max(len(tokens1), len(tokens2))  # Ratio of common words

# Fraud detection function using BERT for semantic similarity
def fraud_reason(row):
    hs_code = row["HS Code"]
    invoice_desc = normalize_text(row["Description of Goods"])
    invoice_embedding = get_bert_embedding(invoice_desc)

    # If HS Code does not exist in database → Fraud
    if hs_code not in valid_hs_codes:
        return "Invalid HS Code"

    # Get all valid descriptions for this HS Code and their embeddings
    valid_descriptions = hs_codes_df[hs_codes_df["HS Code"] == hs_code]["Normalized_Description"].values
    valid_embeddings = hs_codes_df[hs_codes_df["HS Code"] == hs_code]["BERT_Embedding"].values

    # Step 1: Token-Based Matching (Check for significant overlap)
    if any(token_match(invoice_desc, valid_desc) > 0.8 for valid_desc in valid_descriptions):
        return "Valid"

    # Step 2: BERT-Based Semantic Similarity (Detects meaning-based fraud)
    if any(cosine_similarity(invoice_embedding, valid_emb) > 0.85 for valid_emb in valid_embeddings):
        return "Valid"

    # If HS Code exists but description does not match, it's fraud
    return "Mismatch between HS Code and Description"


def analyze_hs(hs_code, description):
    if(hs_code not in valid_hs_codes):
        return 0
    x = hs_codes_df[hs_codes_df["HS Code"] == hs_code]['Description'].iloc[0]
    # print(x)
    # print(type(hs_codes_df[hs_codes_df["HS Code"] == hs_code]['Description'][0]))
    # print(hs_codes_df[hs_codes_df["HS Code"] == hs_code]['Description'][0])
    hs_code = normalize_text(x)
    # description = normalize_text(description)

    hs_embedding = get_bert_embedding(hs_code)
    description_embedding = get_bert_embedding(description)
    return cosine_similarity(hs_embedding, description_embedding)    
    