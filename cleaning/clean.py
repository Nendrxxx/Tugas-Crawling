import pandas as pd
import re

# Reload the dataset after reset
file_path = "Pestapora.csv"
df = pd.read_csv(file_path)

# --- 1. Define inclusion and exclusion keywords ---
include_keywords = [
    "freeport", "pestapora", "papua", "sponsor", "kerjasama",
    "kontroversi", "boikot", "musik", "festival"
]

exclude_keywords = [
    "cuan", "promo", "diskon", "giveaway", "klik link", "jualan",
    "gudang garam", "softex", "marceng"
]

# --- 2. Function to check relevance ---
def is_relevant(text):
    if not isinstance(text, str):
        return False
    text_lower = text.lower()
    # include: must contain at least one inclusion keyword
    if not any(word in text_lower for word in include_keywords):
        return False
    # exclude: must not contain exclusion keywords
    if any(word in text_lower for word in exclude_keywords):
        return False
    return True

# --- 3. Apply filter ---
df_clean = df[df["Content"].apply(is_relevant)].copy()

# --- 4. Save cleaned data to CSV ---
output_path = "Pestapora_cleaned.csv"
df_clean.to_csv(output_path, index=False)

df_clean.shape, output_path
