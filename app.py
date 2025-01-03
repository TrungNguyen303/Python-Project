import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# Helper function to calculate Sales_Amount
def calculate_sales_amount(orders):
    orders["Sales_Amount"] = orders["Quantity"] * orders["Price"]
    return orders


# Define ABC Analysis function
def abc_analysis(orders, inventory):
    st.subheader("ABC Analysis")
    # Merge orders with inventory to get product names
    orders = orders.merge(inventory, on="Product_ID")

    # Calculate Sales_Amount
    orders = calculate_sales_amount(orders)

    # Group by product and calculate total sales
    product_sales = orders.groupby('Product_Name')['Sales_Amount'].sum().sort_values(ascending=False)
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

    st.write("ABC Analysis Results:")
    st.dataframe(abc_result)
    fig = px.bar(abc_result, x='Product', y='Sales', color='Category', title="ABC Analysis")
    st.plotly_chart(fig)


# Define FRM Analysis function
def frm_analysis(orders):
    st.subheader("FRM Analysis")
    # Calculate Sales_Amount
    orders = calculate_sales_amount(orders)

    # Group by customer and calculate metrics
    frm_data = orders.groupby('Customer_ID').agg({
        'Order_Date': lambda x: (orders['Order_Date'].max() - x.max()).days,  # Recency
        'Order_ID': 'count',  # Frequency
        'Sales_Amount': 'sum'  # Monetary
    }).rename(columns={'Order_Date': 'Recency', 'Order_ID': 'Frequency', 'Sales_Amount': 'Monetary'})

    # Segment customers using quantiles
    frm_data['Recency_Score'] = pd.qcut(frm_data['Recency'], q=4, labels=[4, 3, 2, 1])
    frm_data['Frequency_Score'] = pd.qcut(frm_data['Frequency'], q=4, labels=[1, 2, 3, 4])
    frm_data['Monetary_Score'] = pd.qcut(frm_data['Monetary'], q=4, labels=[1, 2, 3, 4])
    frm_data['FRM_Score'] = frm_data['Recency_Score'].astype(str) + frm_data['Frequency_Score'].astype(str) + frm_data['Monetary_Score'].astype(str)

    st.write("FRM Analysis Results:")
    st.dataframe(frm_data)
    fig = px.scatter(frm_data, x='Recency', y='Monetary', size='Frequency', color='FRM_Score',
                     title="FRM Customer Segmentation")
    st.plotly_chart(fig)


# Define Customer Behavior Analysis
def customer_behavior(customers):
    st.subheader("Customer Behavior Analysis")
    # Visualize total spending
    fig = px.bar(customers, x="Customer_ID", y="Total_Spent", title="Total Spending per Customer")
    st.plotly_chart(fig)

    # Recent Purchase Dates
    recent_purchases = customers.sort_values("Last_Purchase_Date", ascending=False)
    st.write("Recent Purchase Dates:")
    st.dataframe(recent_purchases)


# Define function to visualize sales trends
def sales_trends(orders):
    st.subheader("Sales Trends")
    # Calculate daily sales
    orders = calculate_sales_amount(orders)
    daily_sales = orders.groupby("Order_Date")["Sales_Amount"].sum().reset_index()

    # Line chart for sales trends
    fig = px.line(daily_sales, x="Order_Date", y="Sales_Amount", title="Daily Sales Trends")
    st.plotly_chart(fig)


# Define function to visualize inventory status
def inventory_status(inventory):
    st.subheader("Inventory Status")
    # Bar chart for inventory levels
    fig = px.bar(
        inventory,
        x="Product_Name",
        y="Stock",
        title="Inventory Levels",
        labels={"Stock": "Inventory", "Product_Name": "Product"},
    )
    st.plotly_chart(fig)


# Streamlit App
st.title("Coffee Point Data Analysis App")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a page:",
    ["Home", "ABC Analysis", "FRM Analysis", "Sales Trends", "Inventory Status", "Customer Behavior"]
)

# File upload (applicable to all pages)
uploaded_file = st.file_uploader("Upload your Coffee Point data file (Excel format)", type=["xlsx"])

if uploaded_file:
    # Load data from Excel file
    try:
        data = pd.ExcelFile(uploaded_file)
        orders = data.parse("Orders")
        inventory = data.parse("Inventory")
        customers = data.parse("Customers")

        # Ensure required columns are present in the datasets
        required_orders_columns = ["Order_ID", "Order_Date", "Customer_ID", "Product_ID", "Quantity", "Price"]
        required_inventory_columns = ["Product_ID", "Product_Name", "Category", "Stock"]
        required_customers_columns = ["Customer_ID", "Last_Purchase_Date", "Total_Spent"]

        if (
            all(col in orders.columns for col in required_orders_columns)
            and all(col in inventory.columns for col in required_inventory_columns)
            and all(col in customers.columns for col in required_customers_columns)
        ):
            # Navigation Logic
            if page == "Home":
                st.write("Welcome to the Coffee Point Data Analysis App!")
                st.write("Upload a valid Excel file to begin analysis.")
                st.write("Preview of Orders data:")
                st.dataframe(orders.head())
                st.write("Preview of Inventory data:")
                st.dataframe(inventory.head())
                st.write("Preview of Customers data:")
                st.dataframe(customers.head())

            elif page == "ABC Analysis":
                abc_analysis(orders, inventory)

            elif page == "FRM Analysis":
                frm_analysis(orders)

            elif page == "Sales Trends":
                sales_trends(orders)

            elif page == "Inventory Status":
                inventory_status(inventory)

            elif page == "Customer Behavior":
                customer_behavior(customers)

        else:
            st.error("One or more required columns are missing in the dataset.")
    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.info("Please upload a valid Excel file to proceed.")
