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
