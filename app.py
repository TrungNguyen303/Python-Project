import streamlit as st

# Title for the app
st.title("Coffee Point Data Analysis")

# Simple introduction
st.write("Welcome to the Coffee Point Analysis App! Upload your data and get insights.")

# Sidebar for file upload
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type="csv")

if uploaded_file:
    st.write("Here is the uploaded data:")
    st.write(uploaded_file.name)  # Display the name of the file

st.write("This is the starting point of your app!")

import streamlit as st
import pandas as pd

# Title for the app
st.title("Coffee Point Data Analysis")

# File upload in the sidebar
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type="csv")

if uploaded_file:
    # Load the file using pandas
    data = pd.read_csv(uploaded_file)

    # Display the first 5 rows of the data
    st.write("Here is the uploaded data:")
    st.write(data.head())

def abc_analysis(data):
    # Add a 'TotalSales' column
    data['TotalSales'] = data['Quantity'] * data['Price']

    # Sort by TotalSales
    data = data.sort_values(by='TotalSales', ascending=False)

    # Calculate cumulative percentage of total sales
    data['CumulativePercentage'] = data['TotalSales'].cumsum() / data['TotalSales'].sum()

    # Categorize as A, B, or C
    data['Category'] = 'C'  # Default to C
    data.loc[data['CumulativePercentage'] <= 0.8, 'Category'] = 'A'
    data.loc[(data['CumulativePercentage'] > 0.8) & (data['CumulativePercentage'] <= 0.95), 'Category'] = 'B'

    return data

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("Uploaded Data:")
    st.write(data.head())

    # Perform ABC analysis
    abc_result = abc_analysis(data)
    st.subheader("ABC Analysis Results")
    st.write(abc_result)

import matplotlib.pyplot as plt

def plot_abc_distribution(data):
    category_counts = data['Category'].value_counts()
    plt.bar(category_counts.index, category_counts.values)
    plt.title("ABC Category Distribution")
    plt.xlabel("Category")
    plt.ylabel("Number of Products")
    st.pyplot(plt)

if uploaded_file:
    st.subheader("ABC Analysis Chart")
    plot_abc_distribution(abc_result)

def frm_analysis(data):
    now = pd.Timestamp.now()

    # Recency: Days since last purchase
    data['Recency'] = (now - pd.to_datetime(data['LastPurchaseDate'])).dt.days

    # Frequency: Count of purchases
    data['Frequency'] = data.groupby('CustomerID')['OrderID'].transform('count')

    # Monetary: Total spent
    data['Monetary'] = data.groupby('CustomerID')['TotalSales'].transform('sum')

    return data

# Perform FRM analysis
if uploaded_file:
    frm_result = frm_analysis(data)
    st.subheader("FRM Analysis Results")
    st.write(frm_result
