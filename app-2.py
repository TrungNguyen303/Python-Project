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
    st.subheader("ABC Analysis: Product Classification")
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

    # Display results
    st.write("ABC Analysis Results:")
    st.dataframe(abc_result)

    # Plotting the results
    fig = px.bar(abc_result, x='Product', y='Sales', color='Category', title="ABC Analysis")
    st.plotly_chart(fig)

    # Explanation and Recommendations
    st.markdown("""
        ### Recommendations:
        - **Category A**: High-priority products. Ensure sufficient stock and focus on marketing these products.
        - **Category B**: Medium-priority products. Monitor stock and consider targeted promotions.
        - **Category C**: Low-priority products. Minimize investment and evaluate their profitability.
    """)

# Define FRM Analysis function with segmentation, pie chart, and benchmarks
def frm_analysis(orders):
    st.subheader("FRM Analysis: Customer Behavior")
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

    # Classify customers into segments based on FRM Score
    frm_data['Segment'] = frm_data['FRM_Score'].apply(classify_customer_segment)

    st.write("FRM Analysis Results:")
    st.dataframe(frm_data)

    # Plotting FRM results: Scatter Plot
    fig = px.scatter(frm_data, x='Recency', y='Monetary', size='Frequency', color='Segment',
                     title="FRM Customer Segmentation",
                     labels={'Recency': 'Recency (Days)', 'Monetary': 'Monetary Value', 'Frequency': 'Order Frequency'})
    st.plotly_chart(fig)

    # Adding a Pie Chart for Segment Distribution
    segment_counts = frm_data['Segment'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Count']
    fig_pie = px.pie(segment_counts, values='Count', names='Segment', title='Customer Segment Distribution')
    st.plotly_chart(fig_pie)

    # Conclusions and Recommendations with Benchmarks
    st.markdown("""
        ### Conclusions and Recommendations with Benchmarks:

        - **Champions** (Recency: 4, Frequency: 3-4, Monetary: 3-4):
          - These are your most valuable customers who purchase frequently, recently, and spend the most.
          - **Recommendations**:
            - Reward them with VIP programs, exclusive discounts, and personalized offers.
            - Engage them further to encourage advocacy and word-of-mouth referrals.

        - **Loyal Customers** (Recency: 3-4, Frequency: 3-4, Monetary: 2-3):
          - These customers are regular buyers but may not spend as much as Champions.
          - **Recommendations**:
            - Promote cross-sell and upsell opportunities to increase their spending.
            - Keep them engaged with loyalty rewards and updates on new products.

        - **Potential Loyalists** (Recency: 3-4, Frequency: 2-3, Monetary: 2-3):
          - These are relatively new customers who show potential to become loyal.
          - **Recommendations**:
            - Nurture them with targeted discounts, welcome offers, or loyalty programs.
            - Monitor their purchasing behavior to transition them into Loyal Customers or Champions.

        - **Need Attention** (Recency: 2, Frequency: 2-3, Monetary: 1-2):
          - These customers haven't purchased recently and are at risk of disengaging.
          - **Recommendations**:
            - Re-engage them with personalized offers or reminders.
            - Address any issues they might have faced during previous purchases.

        - **At Risk** (Recency: 1, Frequency: 2-3, Monetary: 1-2):
          - These customers have low recent activity and could be close to churning.
          - **Recommendations**:
            - Use win-back campaigns, such as discounts or reactivation emails.
            - Offer incentives to bring them back to the purchasing cycle.

        - **Lost Customers** (Recency: 1, Frequency: 1-2, Monetary: 1-2):
          - These customers haven't purchased in a long time and may no longer be active.
          - **Recommendations**:
            - Evaluate if it's worth re-engaging them or focus resources on acquiring new customers.
            - If attempting re-engagement, target them with significant offers or new product launches.
    """)
    
# Helper function to classify customer segments
def classify_customer_segment(frm_score):
    """Classify customers based on FRM score."""
    recency = int(frm_score[0])
    frequency = int(frm_score[1])
    monetary = int(frm_score[2])

    if recency == 4 and frequency >= 3 and monetary >= 3:
        return "Champions"
    elif recency >= 3 and frequency >= 3:
        return "Loyal Customers"
    elif recency >= 3 and frequency >= 2:
        return "Potential Loyalists"
    elif recency == 2 and frequency >= 2:
        return "Need Attention"
    elif recency == 1 and frequency >= 2:
        return "At Risk"
    else:
        return "Lost Customers"


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

    # Product-level inventory chart
    fig_product = px.bar(
        inventory,
        x="Product_Name",
        y="Stock",
        title="Inventory Levels by Product",
        labels={"Stock": "Inventory", "Product_Name": "Product"},
    )
    st.plotly_chart(fig_product)

    # Category-level inventory chart
    category_inventory = inventory.groupby("Category")["Stock"].sum().reset_index()
    fig_category = px.bar(
        category_inventory,
        x="Category",
        y="Stock",
        title="Inventory Levels by Category",
        labels={"Stock": "Inventory", "Category": "Product Category"},
    )
    st.plotly_chart(fig_category)

# Streamlit App
st.title("Coffee Point Data Analysis App")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a page:",
    ["Home", "ABC Analysis", "FRM Analysis", "Sales Trends", "Inventory Status", "Customer Behavior"]
)

# File upload for primary dataset
uploaded_file = st.file_uploader("Upload your Coffee Point data file (Excel format)", type=["xlsx"])

if uploaded_file:
    # Load primary data
    data = pd.ExcelFile(uploaded_file)
    orders = data.parse("Orders")
    inventory = data.parse("Inventory")
    customers = data.parse("Customers")

    # Navigation Logic
    if page == "Home":
        st.write("Welcome to the Coffee Point Data Analysis App!")
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
    st.info("Please upload a valid Excel file to proceed.")
