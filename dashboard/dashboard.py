import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


all_df = pd.read_csv("dashboard/all_df.csv")

min_date= all_df["order_purchase_timestamp"].min()
max_date= all_df["order_purchase_timestamp"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

orders_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & (all_df["order_purchase_timestamp"] <= str(end_date))]

def create_top_category_products_df(df):
    top_category_products_df = df.groupby(by="product_category_name_english").order_item_id.count().reset_index().sort_values(by="order_item_id", ascending=False).rename(columns={"order_item_id": "jumlah_produk_terjual"}).head()
    return top_category_products_df

def create_bottom_category_products_df(df):
    bottom_category_products_df = df.groupby(by="product_category_name_english").order_item_id.count().reset_index().sort_values(by="order_item_id", ascending=True).rename(columns={"order_item_id": "jumlah_produk_terjual"}).head()
    return bottom_category_products_df

def create_jumlah_pesanan_berdasarkan_ketepatan_waktu_pengiriman_df(df):
    jumlah_pesanan_berdasarkan_ketepatan_waktu_pengiriman_df = df.groupby(by="ketepatan_waktu").order_id.count().reset_index().rename(columns={"order_id": "jumlah_pesanan"})
    return jumlah_pesanan_berdasarkan_ketepatan_waktu_pengiriman_df

def create_rata_rata_rating_pesanan_berdasarkan_ketepatan_waktu_pengiriman_df(df):
    rata_rata_rating_pesanan_berdasarkan_ketepatan_waktu_pengiriman_df = df.groupby(by="ketepatan_waktu").review_score.mean().reset_index().rename(columns={"review_score": "rata_rata_rating"})
    rata_rata_rating_pesanan_berdasarkan_ketepatan_waktu_pengiriman_df["rata_rata_rating"] = round(rata_rata_rating_pesanan_berdasarkan_ketepatan_waktu_pengiriman_df["rata_rata_rating"], 1)
    return rata_rata_rating_pesanan_berdasarkan_ketepatan_waktu_pengiriman_df


st.header('Ecommerce Dashboard :sparkles:')
st.subheader("5 kategori produk paling laku dan tidak laku")


fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="jumlah_produk_terjual", y="product_category_name_english", data=create_top_category_products_df(orders_df), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("jumlah penjualan(item)", fontsize=30)
ax[0].set_title("Kategori produk paling laku", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="jumlah_produk_terjual", y="product_category_name_english", data=create_bottom_category_products_df(orders_df), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("jumlah penjualan(item)", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.tick_right()
ax[1].set_title("Kategori produk paling tidak laku", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.subheader("Jumlah pesanan berdasarkan ketepatan waktu pengiriman")

fig, ax = plt.subplots(figsize=(16,8))

colors = ["#72BCD4", "#D3D3D3"]

sns.barplot(
    y="jumlah_pesanan",
    x="ketepatan_waktu",
    data=create_jumlah_pesanan_berdasarkan_ketepatan_waktu_pengiriman_df(orders_df),
    palette=colors,
    ax=ax
)
ax.set_title("Banyak pesanan berdasarkan ketepatan waktu pengiriman", loc="center", fontsize=20)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)

st.pyplot(fig)

st.subheader("Rata-rata rating pesanan berdasarkan ketepatan waktu pengiriman")
 
fig, ax = plt.subplots(figsize=(16,8))

colors = ["#72BCD4", "#D3D3D3"]

sns.barplot(
    y="rata_rata_rating",
    x="ketepatan_waktu",
    data=create_rata_rata_rating_pesanan_berdasarkan_ketepatan_waktu_pengiriman_df(orders_df),
    palette=colors,
    ax=ax
)
ax.set_title("Rata-rata rating pesanan berdasarkan ketepatan waktu pengiriman", loc="center", fontsize=20)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)

st.pyplot(fig)


st.subheader("Total produk terjual") 
total_products_sold = orders_df.product_id.count()
st.metric("Total produk terjual", value=total_products_sold)



