import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

print("🔍 Debug: Starting script...")

# Load the datasets
try:
    invoices_df = pd.read_csv('valid_invoices.csv')
    price_thresholds_df = pd.read_csv('price_thresholds.csv')
    print(f"✅ Debug: Loaded invoices ({len(invoices_df)}) and price thresholds ({len(price_thresholds_df)}) successfully.")
except Exception as e:
    print(f"❌ Error loading files: {e}")
    exit()

# Exchange rates (Example: Replace with real-time rates if needed)
exchange_rates = {
    "USD": 1,        # Base currency
    "EUR": 1.08,     # 1 EUR = 1.08 USD
    "GBP": 1.30,     # 1 GBP = 1.30 USD
    "MAD": 0.10,     # 1 Moroccan Dirham = 0.10 USD
    "CNY": 0.14,     # 1 Chinese Yuan = 0.14 USD
    "JPY": 0.007,    # 1 Japanese Yen = 0.007 USD
    # Add more currencies if needed
}

# Initialize BERT model for embeddings
print("🔍 Debug: Loading BERT model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Debug: BERT model loaded.")

# Generate embeddings for product descriptions in the price database
print("🔍 Debug: Generating product embeddings...")
price_thresholds_df['Product_Embedding'] = price_thresholds_df['Product'].apply(
    lambda x: model.encode(x) if isinstance(x, str) else np.zeros(384)
)
print("✅ Debug: Product embeddings generated.")

# Function to convert prices to USD
def convert_to_usd(price, currency):
    if currency in exchange_rates:
        return price * exchange_rates[currency]
    else:
        return None  # Unknown currency

# Function to find the best match using BERT embeddings
def find_best_match(invoice_description, price_embeddings, price_products):
    if not isinstance(invoice_description, str) or invoice_description.strip() == "":
        return None, 0.0

    invoice_embedding = model.encode(invoice_description)
    similarities = cosine_similarity([invoice_embedding], price_embeddings)[0]
    best_match_index = np.argmax(similarities)
    best_match_score = similarities[best_match_index]

    if best_match_score > 0.7:
        return price_products[best_match_index], best_match_score
    else:
        return None, best_match_score

# Lists to store results
flagged_invoices = []
missing_products = []
valid_invoices = []

print("🔍 Debug: Processing invoices...")

# Iterate through each invoice
for index, row in tqdm(invoices_df.iterrows(), total=len(invoices_df)):
    invoice_description = row.get('Description of Goods', '').strip()
    invoice_price = row.get('Price (per unit)', None)
    invoice_currency = row.get('Currency', '').strip()

    if invoice_price is None or invoice_currency == "":
        flagged_invoices.append({**row.to_dict(), "Reason": "Missing price or currency information."})
        continue  # Skip processing

    # Convert price to USD
    invoice_price_usd = convert_to_usd(invoice_price, invoice_currency)
    
    if invoice_price_usd is None:
        flagged_invoices.append({**row.to_dict(), "Reason": f"Currency '{invoice_currency}' is not recognized."})
        continue  # Skip processing

    # Find the best match
    best_match, similarity_score = find_best_match(
        invoice_description,
        list(price_thresholds_df['Product_Embedding']),
        list(price_thresholds_df['Product'])
    )

    if best_match:
        matched_product_row = price_thresholds_df[price_thresholds_df['Product'] == best_match].iloc[0]
        lower_bound = matched_product_row['Lower Threshold']
        upper_bound = matched_product_row['Upper Threshold']

        # Check if the price is within bounds
        if invoice_price_usd < lower_bound:
            flagged_invoices.append({
                **row.to_dict(),
                'Converted Price (USD)': invoice_price_usd,
                'Matched_Product': best_match,
                'Lower_Bound': lower_bound,
                'Upper_Bound': upper_bound,
                'Reason': f"Price ({invoice_price_usd} USD) is below the lower bound of {lower_bound} USD."
            })
        elif invoice_price_usd > upper_bound:
            flagged_invoices.append({
                **row.to_dict(),
                'Converted Price (USD)': invoice_price_usd,
                'Matched_Product': best_match,
                'Lower_Bound': lower_bound,
                'Upper_Bound': upper_bound,
                'Reason': f"Price ({invoice_price_usd} USD) is above the upper bound of {upper_bound} USD."
            })
        else:
            row['Converted Price (USD)'] = invoice_price_usd
            valid_invoices.append(row)
    else:
        missing_products.append({
            **row.to_dict(),
            "Converted Price (USD)": invoice_price_usd,
            'Reason': f"Product '{invoice_description}' not found in the price database."
        })

print(f"✅ Debug: Processing complete. Flagged: {len(flagged_invoices)}, Missing: {len(missing_products)}, Valid: {len(valid_invoices)}")

# Convert lists to DataFrames
flagged_invoices_df = pd.DataFrame(flagged_invoices)
missing_products_df = pd.DataFrame(missing_products)
valid_invoices_df = pd.DataFrame(valid_invoices)

# Save results (only if data exists)
if not flagged_invoices_df.empty:
    flagged_invoices_df.to_csv(r'C:\Users\hiba\OneDrive - Al Akhawayn University in Ifrane\Competition_PORTNET\flagged_invoices.csv', index=False)
    print("📁 Debug: Saved 'flagged_invoices.csv'")

if not missing_products_df.empty:
    missing_products_df.to_csv(r'C:\Users\hiba\OneDrive - Al Akhawayn University in Ifrane\Competition_PORTNET\missing_products.csv', index=False)
    print("📁 Debug: Saved 'missing_products.csv'")

if not valid_invoices_df.empty:
    valid_invoices_df.to_excel(r'C:\Users\hiba\OneDrive - Al Akhawayn University in Ifrane\Competition_PORTNET\price_valid_invoices.xlsx', index=False)
    print("📁 Debug: Saved 'price_valid_invoices.xlsx'")

print("✅ All tasks completed successfully!")