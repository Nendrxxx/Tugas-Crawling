import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Dashboard Sentimen Pestapora",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === FUNGSI UNTUK KONVERSI ANGKA (K, M) ===
def convert_to_int(value):
    """Mengubah string seperti '4.4k' atau '1.2m' menjadi integer."""
    try:
        if isinstance(value, (int, float)):
            return int(value)

        value_str = str(value).strip().lower()
        if 'k' in value_str:
            return int(float(value_str.replace('k', '')) * 1_000)
        if 'm' in value_str:
            return int(float(value_str.replace('m', '')) * 1_000_000)

        return int(float(value_str))
    except (ValueError, TypeError):
        return 0

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
        df = df.dropna(subset=["timestamp"])

    if 'sentiment' in df.columns:
        df['sentiment'] = df['sentiment'].astype(str).str.strip().str.lower()

    if 'verified' in df.columns:
        df['verified'] = df['verified'].apply(lambda x: str(x).lower() == 'true')
        
    for col in ['likes', 'retweets', 'comments']:
        if col in df.columns:
            df[col] = df[col].apply(convert_to_int)

    return df

df = load_data("data/Pestapora_sentiment.csv")

# === SIDEBAR ===
with st.sidebar:
    st.header("⚙️ Filter & Kontrol")
    sentiment_filter = st.selectbox("Filter Berdasarkan Sentimen", ["All", "positif", "negatif", "netral"])
    verified_filter = st.selectbox("Filter Tipe Akun", ["Semua Akun", "Verified", "Tidak Verified"])
    sort_option = st.selectbox("Urutkan Berdasarkan", ["Waktu Terbaru", "Waktu Terlama", "Likes Terbanyak", "Retweets Terbanyak"])
    search_text = st.text_input("Cari Tweet (handle / kata kunci)")

# === Judul Utama ===
st.title("📊 Dashboard Analisis Sentimen: Pestapora x Freeport")
st.markdown("Dashboard ini menganalisis sentimen publik di Twitter mengenai kolaborasi Pestapora dengan Freeport.")

# === KPI UTAMA / METRICS ===
st.subheader("KPI Utama")
total_tweets = len(df)
positive_tweets = len(df[df['sentiment'] == 'positif'])
neutral_tweets = len(df[df['sentiment'] == 'netral'])
negative_tweets = len(df[df['sentiment'] == 'negatif'])

positive_percentage = (positive_tweets / total_tweets * 100) if total_tweets > 0 else 0
neutral_percentage = (neutral_tweets / total_tweets * 100) if total_tweets > 0 else 0
negative_percentage = (negative_tweets / total_tweets * 100) if total_tweets > 0 else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Tweet Dianalisis", value=f"{total_tweets:,}")
with col2:
    st.metric(label="Sentimen Positif", value=f"{positive_percentage:.1f}%")
with col3:
    st.metric(label="Sentimen Netral", value=f"{neutral_percentage:.1f}%")
with col4:
    st.metric(label="Sentimen Negatif", value=f"{negative_percentage:.1f}%")


st.divider()

# === Distribusi Sentimen ===
st.subheader("Distribusi Sentimen")

with st.container(border=True):
    sentiment_counts_df = df['sentiment'].value_counts().reset_index()
    sentiment_counts_df.columns = ['Sentiment', 'Jumlah']
    
    st.write("") 
    _, mid_col, _ = st.columns([0.5, 1.5, 0.5])
    with mid_col:
        fig_donut = px.pie(
            sentiment_counts_df,
            values="Jumlah",
            names="Sentiment",
            hole=0.6,
            color="Sentiment",
            color_discrete_map={"positif": "#2ecc71", "negatif": "#e74c3c", "netral": "#3498db"}
        )
        fig_donut.update_traces(
            textinfo='value',
            textfont_size=16,
            marker=dict(line=dict(color='#0E1117', width=4)),
            hovertemplate='<b>%{label}</b><extra></extra>'
        )
        fig_donut.update_layout(
            title={'text': 'Proporsi Sentimen', 'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
            showlegend=True,
            annotations=[dict(text=f'Total<br>{total_tweets}', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        st.plotly_chart(fig_donut, use_container_width=True)

st.write("")
positif_count = sentiment_counts_df[sentiment_counts_df['Sentiment'] == 'positif']['Jumlah'].sum()
netral_count = sentiment_counts_df[sentiment_counts_df['Sentiment'] == 'netral']['Jumlah'].sum()
negatif_count = sentiment_counts_df[sentiment_counts_df['Sentiment'] == 'negatif']['Jumlah'].sum()

card_col1, card_col2, card_col3 = st.columns(3)
with card_col1:
    st.markdown(f"""
    <div style="background-color: #1e1e1e; border-radius: 10px; padding: 20px; text-align: center; border: 1px solid #2ecc71;">
        <h3 style="color: #2ecc71;">👍 Positif</h3>
        <p style="font-size: 2.5em; color: white; font-weight: bold; margin: 0;">{positif_count:,}</p>
        <p style="color: #aaa;">({(positif_count/total_tweets*100):.1f}%)</p>
    </div>
    """, unsafe_allow_html=True)
with card_col2:
    st.markdown(f"""
    <div style="background-color: #1e1e1e; border-radius: 10px; padding: 20px; text-align: center; border: 1px solid #3498db;">
        <h3 style="color: #3498db;">😐 Netral</h3>
        <p style="font-size: 2.5em; color: white; font-weight: bold; margin: 0;">{netral_count:,}</p>
        <p style="color: #aaa;">({(netral_count/total_tweets*100):.1f}%)</p>
    </div>
    """, unsafe_allow_html=True)
with card_col3:
    st.markdown(f"""
    <div style="background-color: #1e1e1e; border-radius: 10px; padding: 20px; text-align: center; border: 1px solid #e74c3c;">
        <h3 style="color: #e74c3c;">👎 Negatif</h3>
        <p style="font-size: 2.5em; color: white; font-weight: bold; margin: 0;">{negatif_count:,}</p>
        <p style="color: #aaa;">({(negatif_count/total_tweets*100):.1f}%)</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# === TREN WAKTU ===
with st.container(border=True):
    st.write("")
    st.subheader("Tren Sentimen dari Waktu ke Waktu")
    df["tanggal"] = df["timestamp"].dt.date
    trend = df.groupby(["tanggal", "sentiment"]).size().reset_index(name="Jumlah")
    fig_trend = px.line(
        trend, x="tanggal", y="Jumlah", color="sentiment",
        title="Fluktuasi Sentimen Harian", markers=True,
        color_discrete_map={"positif": "#2ecc71", "negatif": "#e74c3c", "netral": "#3498db"},
        line_shape='linear'
    )
    st.plotly_chart(fig_trend, use_container_width=True)


# === WORDCLOUD ===
with st.container(border=True):
    st.subheader("Kata yang Sering Muncul (Wordcloud)")
    all_text = " ".join(df["content"].astype(str).tolist())
    wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="viridis", collocations=False).generate(all_text)
    fig_wc, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig_wc)

st.divider()

# === BROWSER TWEET DENGAN NAVIGASI ===
st.subheader("📝 Jelajahi Tweet")

# --- Logika Filtering ---
filtered_df = df.copy()

if sentiment_filter != "All":
    filtered_df = filtered_df[filtered_df['sentiment'] == sentiment_filter.lower()]

if verified_filter == "Verified":
    filtered_df = filtered_df[filtered_df['verified'] == True]
elif verified_filter == "Tidak Verified":
    filtered_df = filtered_df[filtered_df['verified'] == False]

if search_text:
    mask = filtered_df["content"].str.contains(search_text, case=False, na=False) | \
           filtered_df["handle"].str.contains(search_text, case=False, na=False)
    filtered_df = filtered_df[mask]

if sort_option == "Waktu Terbaru":
    filtered_df = filtered_df.sort_values(by="timestamp", ascending=False)
elif sort_option == "Waktu Terlama":
    filtered_df = filtered_df.sort_values(by="timestamp", ascending=True)
elif sort_option == "Likes Terbanyak":
    filtered_df = filtered_df.sort_values(by="likes", ascending=False)
elif sort_option == "Retweets Terbanyak":
    filtered_df = filtered_df.sort_values(by="retweets", ascending=False)


# --- Logika Paginasi (Navigasi) ---
if 'page' not in st.session_state:
    st.session_state.page = 0

TWEETS_PER_PAGE = 10
total_filtered = len(filtered_df)
total_pages = (total_filtered // TWEETS_PER_PAGE) + (1 if total_filtered % TWEETS_PER_PAGE > 0 else 0)

if st.session_state.page >= total_pages and total_pages > 0:
    st.session_state.page = 0
elif total_pages == 0:
    st.session_state.page = 0

start_idx = st.session_state.page * TWEETS_PER_PAGE
end_idx = start_idx + TWEETS_PER_PAGE
tweets_to_show = filtered_df.iloc[start_idx:end_idx]

start_num = start_idx + 1
end_num = min(end_idx, total_filtered)

if total_filtered > 0:
    st.write(f"Menampilkan tweet **{start_num} - {end_num}** dari **{total_filtered}** hasil.")
else:
    st.write("Tidak ada tweet yang cocok dengan filter Anda.")


# --- Tampilkan Tweet untuk halaman saat ini ---
num_columns = 2
cols = st.columns(num_columns)
sentiment_colors = {"positif": "#2ecc71", "negatif": "#e74c3c", "netral": "#3498db"}

for i, (_, row) in enumerate(tweets_to_show.iterrows()):
    handle = row.get("handle", "N/A")
    content = row.get("content", "")
    waktu_dt = row.get("timestamp", None)
    waktu = waktu_dt.strftime("%d %b %Y, %H:%M") if pd.notnull(waktu_dt) else "N/A"
    likes = row.get("likes", 0)
    rts = row.get("retweets", 0)
    cmts = row.get("comments", 0)
    link = row.get("tweet link", "#")
    sentiment = row.get("sentiment", "netral")
    
    # --- PERBAIKAN: Menghapus pemotongan teks (truncation) ---
    # Teks sekarang akan ditampilkan penuh.
    full_content = content

    is_verified = row.get('verified', False)
    verified_badge = "✅" if is_verified else ""

    card_html = f"""
    <div style="border: 1px solid #333; border-radius: 10px; padding: 15px; margin-bottom: 15px; background-color: #1e1e1e; box-shadow: 0 4px 8px rgba(0,0,0,0.2); min-height: 280px; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <p style="color:#fff; font-weight:bold; margin:0; font-size: 1.1em; margin-right: 5px;">{handle}</p>
                <p style="margin:0;">{verified_badge}</p>
            </div>
            <p style="color:#aaa; font-size: 0.8em; margin-top: -10px;">{waktu}</p>
            <p style="color:#e0e0e0; margin:5px 0 15px 0; overflow-wrap: break-word;">{full_content}</p>
        </div>
        <div>
            <p style="color:{sentiment_colors.get(sentiment, '#aaaaaa')}; margin:0;"><b>Sentimen: {sentiment.capitalize()}</b></p>
            <div style="color:#aaaaaa; margin-top: 10px; display: flex; align-items: center; justify-content: space-between;">
                <span>
                    ❤️ {likes:,} &nbsp; 🔁 {rts:,} &nbsp; 💬 {cmts:,}
                </span>
                <a href="{link}" target="_blank" style="color:#1DA1F2; text-decoration:none; font-weight:bold;">Lihat Tweet 🔗</a>
            </div>
        </div>
    </div>
    """

    target_col = cols[i % num_columns]
    with target_col:
        st.markdown(card_html, unsafe_allow_html=True)

# --- Tombol Navigasi ---
st.write("")
nav_cols = st.columns([1, 2, 1])

with nav_cols[0]:
    if st.session_state.page > 0:
        if st.button("⬅️ Sebelumnya"):
            st.session_state.page -= 1
            st.rerun()

with nav_cols[1]:
    if total_pages > 0:
        st.markdown(f"<p style='text-align: center; color: #aaa;'>Halaman {st.session_state.page + 1} dari {total_pages}</p>", unsafe_allow_html=True)

with nav_cols[2]:
    if st.session_state.page < total_pages - 1:
        if st.button("Berikutnya ➡️", use_container_width=True):
            st.session_state.page += 1
            st.rerun()