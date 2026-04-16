import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import os

st.set_page_config(page_title="Personal Finance Tracker", layout="wide")

FILE = "expenses.csv"

# Create CSV if not exists
if not os.path.exists(FILE):
    pd.DataFrame(columns=["Date", "Type", "Category", "Amount"]).to_csv(FILE, index=False)

st.title("💰 Personal Finance Tracker")

# Input Form
with st.form("finance_form"):
    trans_date = st.date_input("Date", date.today())
    trans_type = st.selectbox("Type", ["Income", "Expense"])
    category = st.text_input("Category")
    amount = st.number_input("Amount", min_value=0.0)
    submitted = st.form_submit_button("Add Transaction")

if submitted:
    new_data = pd.DataFrame([[trans_date, trans_type, category, amount]],
                            columns=["Date", "Type", "Category", "Amount"])
    new_data.to_csv(FILE, mode='a', header=False, index=False)
    st.success("Transaction Added Successfully!")

# Load Data
df = pd.read_csv(FILE)

st.subheader("📋 All Transactions")
st.dataframe(df)

# Summary
income = df[df["Type"]=="Income"]["Amount"].sum()
expense = df[df["Type"]=="Expense"]["Amount"].sum()
balance = income - expense

col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"₹{income}")
col2.metric("Total Expense", f"₹{expense}")
col3.metric("Balance", f"₹{balance}")

# Expense Chart
expense_df = df[df["Type"]=="Expense"]

if not expense_df.empty:
    st.subheader("📊 Expense by Category")
    category_sum = expense_df.groupby("Category")["Amount"].sum()

    fig, ax = plt.subplots()
    ax.pie(category_sum, labels=category_sum.index, autopct='%1.1f%%')
    st.pyplot(fig)
    