# 2. Import library
import pandas as pd
from transformers import pipeline

# 3. Load dataset (ganti sesuai path file kamu)
df = pd.read_csv("Pestapora_cleaned.csv")

# 4. Load model sentiment
sentiment_model = pipeline(
    "sentiment-analysis",
    model="taufiqdp/indonesian-sentiment"
)

# 5. Terapkan sentiment analysis ke kolom Content
df["Sentiment"] = df["Content"].astype(str).apply(lambda x: sentiment_model(x)[0]["label"])
df["Confidence"] = df["Content"].astype(str).apply(lambda x: sentiment_model(x)[0]["score"])

# 6. Simpan hasil ke file CSV baru
df.to_csv("Pestapora_sentiment.csv", index=False)

print("Analisis selesai! File hasil tersimpan di Pestapora_sentiment.csv")
print(df[["Content", "Sentiment", "Confidence"]].head(10))
