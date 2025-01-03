#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# Define ABC Analysis function
def abc_analysis(data):
    st.write("Running ABC Analysis...")
    # Group by product and calculate total sales
    product_sales = data.groupby('product')['sales'].sum().sort_values(ascending=False)
    total_sales = product_sales.sum()
    product_sales_percentage = (product_sales / total_sales).cumsum()

    # Classify products into A, B, and C categories
    abc_classification = pd.cut(product_sales_percentage, bins=[0, 0.7, 0.9, 1], labels=['A', 'B', 'C'])
    abc_result = pd.DataFrame({
        'Product': product_sales.index,
        'Sales': product_sales.values,
        'Percentage': product_sales_percentage.values,
        'Category': abc_classification
    })
    return abc_result

# Define FRM Analysis function
def frm_analysis(data):
    st.write("Running FRM Analysis...")
    # Group by customer and calculate metrics
    frm_data = data.groupby('customer_id').agg({
        'order_date': lambda x: (data['order_date'].max() - x.max()).days,  # Recency
        'order_id': 'count',  # Frequency
        'sales': 'sum'  # Monetary
    }).rename(columns={'order_date': 'Recency', 'order_id': 'Frequency', 'sales': 'Monetary'})

    # Segment customers using quantiles
    frm_data['Recency_Score'] = pd.qcut(frm_data['Recency'], q=4, labels=[4, 3, 2, 1])
    frm_data['Frequency_Score'] = pd.qcut(frm_data['Frequency'], q=4, labels=[1, 2, 3, 4])
    frm_data['Monetary_Score'] = pd.qcut(frm_data['Monetary'], q=4, labels=[1, 2, 3, 4])
    frm_data['FRM_Score'] = frm_data['Recency_Score'].astype(str) + frm_data['Frequency_Score'].astype(str) + frm_data['Monetary_Score'].astype(str)

    return frm_data

# Streamlit App
st.title("Coffee Point Data Analysis App")
st.subheader("Analyze sales data to improve Coffee Point's operational efficiency.")

# File upload
uploaded_file = st.file_uploader("Upload your sales data file (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # Load data
    try:
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)
        st.write("Data loaded successfully!")
        st.write("Preview of the data:")
        st.dataframe(data.head())

        # Ensure required columns are present
        required_columns = ['product', 'sales', 'customer_id', 'order_date', 'order_id']
        if all(col in data.columns for col in required_columns):
            # ABC Analysis
            st.subheader("ABC Analysis")
            if st.button("Run ABC Analysis"):
                abc_results = abc_analysis(data)
                st.write("ABC Analysis Results:")
                st.dataframe(abc_results)
                fig = px.bar(abc_results, x='Product', y='Sales', color='Category', title="ABC Analysis")
                st.plotly_chart(fig)

            # FRM Analysis
            st.subheader("FRM Analysis")
            if st.button("Run FRM Analysis"):
                frm_results = frm_analysis(data)
                st.write("FRM Analysis Results:")
                st.dataframe(frm_results)
                fig = px.scatter(frm_results, x='Recency', y='Monetary', size='Frequency', color='FRM_Score',
                                 title="FRM Customer Segmentation")
                st.plotly_chart(fig)

        else:
            st.error(f"Missing required columns: {set(required_columns) - set(data.columns)}")
    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.info("Please upload a CSV or Excel file to proceed.")

# Automation Section
st.subheader("Automate Reports")
if st.button("Generate Reports"):
    st.write("Report generated successfully!")
    # Add logic to save reports to a file or email them.


# In[ ]:




