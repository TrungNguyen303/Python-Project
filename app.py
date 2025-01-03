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
