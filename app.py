import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Konfigurasi halaman
st.set_page_config(page_title="E-commerce Data Analysis Dashboard", layout="wide")

# Judul utama
st.markdown("# 📊 E-commerce Data Analysis Dashboard")

# ---- LOAD DATA ----
@st.cache_data
def load_data():
    try:
        df_orders = pd.read_csv("orders_dataset.csv")
        df_orders['order_purchase_timestamp'] = pd.to_datetime(df_orders['order_purchase_timestamp'])
        df_orders['order_delivered_customer_date'] = pd.to_datetime(df_orders['order_delivered_customer_date'])
        df_orders['order_estimated_delivery_date'] = pd.to_datetime(df_orders['order_estimated_delivery_date'])
        
        # Hitung waktu pengiriman dan keterlambatan
        df_orders['delivery_time_days'] = (df_orders['order_delivered_customer_date'] - df_orders['order_purchase_timestamp']).dt.days
        df_orders['late_delivery_days'] = (df_orders['order_delivered_customer_date'] - df_orders['order_estimated_delivery_date']).dt.days
        df_orders['late_delivery_days'] = df_orders['late_delivery_days'].apply(lambda x: x if x > 0 else 0)
        
        return df_orders
    except FileNotFoundError:
        st.error("Dataset tidak ditemukan! Pastikan file 'orders_dataset.csv' tersedia di direktori yang benar.")
        return None

df_orders = load_data()

if df_orders is not None:
    # ---- DATASET OVERVIEW ----
    st.subheader("📌 Dataset Overview")
    st.write("Checking missing values and dataset structure:")
    st.write(df_orders.isnull().sum())

    # ---- DATA CLEANING ----
    st.subheader("📌 Data Cleaning")
    df_orders.dropna(inplace=True)
    st.write("Missing values cleaned!")

    # ---- EXPLORATORY DATA ANALYSIS ----
    st.subheader("📊 Exploratory Data Analysis")
    st.markdown("### Summary Statistics")
    st.write(df_orders[['delivery_time_days', 'late_delivery_days']].describe())

    # ---- VISUALIZATION ----
    st.markdown("### ⏳ Distribution of Delivery Time")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df_orders["delivery_time_days"], bins=30, kde=True, color="skyblue", ax=ax)
    ax.axvline(df_orders["delivery_time_days"].mean(), color='red', linestyle='dashed', linewidth=2, label=f"Mean: {df_orders['delivery_time_days'].mean():.2f} days")
    ax.set_xlabel("Delivery Time (days)")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of Delivery Time")
    ax.legend()
    st.pyplot(fig)

    st.markdown("### 🚚 Late Deliveries Analysis")
    delay_percentage = (df_orders["late_delivery_days"] > 0).mean() * 100
    st.metric(label="Percentage of Late Deliveries", value=f"{delay_percentage:.2f}%")

    st.success("Dashboard successfully loaded! 🚀")
else:
    st.warning("Silakan pastikan dataset tersedia untuk memulai analisis.")

dataset_folder = "E-commerce-public-dataset"
file_path = os.path.join(dataset_folder, "orders_dataset.csv")

if os.path.exists(file_path):
    df_orders = pd.read_csv(file_path)
    st.success("Dataset ditemukan! 🚀")

