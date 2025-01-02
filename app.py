pip install streamlit pandas matplotlib
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title for the app
st.title("Coffee Point Data Analysis")

# Sidebar for file upload
st.sidebar.title("Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type="csv")

# If a file is uploaded
if uploaded_file:
    # Load the file using pandas
    try:
        data = pd.read_csv(uploaded_file)
        st.write("Uploaded Data (First 5 rows):")
        st.write(data.head())

        # Check for necessary columns
        if not all(col in data.columns for col in ["Quantity", "Price", "LastPurchaseDate", "CustomerID", "OrderID"]):
            st.error("The uploaded CSV file must contain the columns: Quantity, Price, LastPurchaseDate, CustomerID, and OrderID.")
        else:
            # Perform ABC analysis
            def abc_analysis(data):
                data['TotalSales'] = data['Quantity'] * data['Price']
                data = data.sort_values(by='TotalSales', ascending=False)
                data['CumulativePercentage'] = data['TotalSales'].cumsum() / data['TotalSales'].sum()
                data['Category'] = 'C'
                data.loc[data['CumulativePercentage'] <= 0.8, 'Category'] = 'A'
                data.loc[(data['CumulativePercentage'] > 0.8) & (data['CumulativePercentage'] <= 0.95), 'Category'] = 'B'
                return data

            abc_result = abc_analysis(data)
            st.subheader("ABC Analysis Results")
            st.write(abc_result)

            # Plot ABC Analysis distribution
            def plot_abc_distribution(data):
                category_counts = data['Category'].value_counts()
                plt.bar(category_counts.index, category_counts.values)
                plt.title("ABC Category Distribution")
                plt.xlabel("Category")
                plt.ylabel("Number of Products")
                st.pyplot(plt)

            st.subheader("ABC Analysis Chart")
            plot_abc_distribution(abc_result)

            # Perform FRM analysis
            def frm_analysis(data):
                now = pd.Timestamp.now()
                data['Recency'] = (now - pd.to_datetime(data['LastPurchaseDate'])).dt.days
                data['Frequency'] = data.groupby('CustomerID')['OrderID'].transform('count')
                data['Monetary'] = data.groupby('CustomerID')['TotalSales'].transform('sum')
                return data

            frm_result = frm_analysis(data)
            st.subheader("FRM Analysis Results")
            st.write(frm_result)

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload a CSV file to start analysis.")

