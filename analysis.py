import pandas as pd
df=pd.read_csv("Ecommerce_Transactions_Data.csv")
print(df.head())
print("\nDataset Shape:")
print(df.shape)
print("\nColumns Names:")
print(df.columns.tolist())
print("\nData Types")
print(df.dtypes)
print("\nMissing Values:")
print(df.isnull().sum())
df_clean = df.copy()
df_clean["Date"] = pd.to_datetime(
    df_clean["Date"],
    errors="coerce"
)
df_clean["CustomerNo"] = df_clean["CustomerNo"].astype("string")
text_columns = ["TransactionNo", "Product", "Country", "Category"]
for col in text_columns:
    df_clean[col] = df_clean[col].str.strip()
print("\nDuplicate rows:", df_clean.duplicated().sum())
print(
    "Cancelled transactions:",
    df_clean["TransactionNo"].str.startswith("C", na=False).sum()
)
print(
    "Negative quantities:",
    (df_clean["Quantity"] < 0).sum()
)
print(
    "Zero quantities:",
    (df_clean["Quantity"] == 0).sum()
)
print(
    "Negative prices:",
    (df_clean["Price"] < 0).sum()
)
print(
    "Zero prices:",
    (df_clean["Price"] == 0).sum()
)
print("\nMissing values:")
print(df_clean.isnull().sum())
df_clean["TransactionAmount"] = (
    df_clean["Price"] * df_clean["Quantity"]
)
print("\nTransaction Amount Preview:")
print(
    df_clean[
        ["TransactionNo", "Price", "Quantity", "TransactionAmount"]
    ].head(10)
)
print("\nTotal Transaction Amount:")
print(df_clean["TransactionAmount"].sum())
print("\nTransaction Amount Statistics:")
print(df_clean["TransactionAmount"].describe())
cancelled_mask = (
    df_clean["TransactionNo"]
    .astype("string")
    .str.startswith("C", na=False)
)

cancelled = df_clean.loc[cancelled_mask].copy()
print("\nCancelled Transaction Samples:")
print(
    cancelled[
        ["TransactionNo", "Product", "Quantity", "Price"]
    ].head(10)
)
print("\nCancellation and Quantity Check:")
print(
    "Cancellation records:",
    len(cancelled)
)
print(
    "Cancelled records with negative quantity:",
    (cancelled["Quantity"] < 0).sum()
)
print(
    "Negative quantity records without C prefix:",
    (
        (df_clean["Quantity"] < 0)
        & ~df_clean["TransactionNo"].str.startswith("C", na=False)
    ).sum()
)
print(
    "C-prefixed records with positive quantity:",
    (cancelled["Quantity"] > 0).sum()
)
df_sales = df_clean[
    ~df_clean["TransactionNo"].str.startswith("C", na=False)
].copy()
df_sales = df_sales[
    (df_sales["Quantity"] > 0) &
    (df_sales["Price"] > 0)
].copy()
print("\nSales Dataset Shape:")
print(df_sales.shape)
print("\nTotal Sales Amount:")
print(round(df_sales["TransactionAmount"].sum(), 2))
print("\nSales Transaction Amount Statistics:")
print(df_sales["TransactionAmount"].describe())
print("\nRemaining Negative Quantities:")
print((df_sales["Quantity"] < 0).sum())
print("\nRemaining Cancelled Transactions:")
print(
    df_sales["TransactionNo"]
    .str.startswith("C", na=False)
    .sum()
)
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.hist(
    df_sales["TransactionAmount"],
    bins=30,
    edgecolor="black"
)
plt.title("Distribution of Transaction Amounts")
plt.xlabel("Transaction Amount")
plt.ylabel("Number of Transactions")
plt.tight_layout()
plt.savefig("transaction_amount_distribution.png", dpi=300)
plt.show()
daily_sales = (
    df_sales.groupby(df_sales["Date"].dt.date)["TransactionAmount"]
    .sum()
)
plt.figure(figsize=(12, 6))
plt.plot(daily_sales.index, daily_sales.values)
plt.title("Transaction Amount Over Time")
plt.xlabel("Date")
plt.ylabel("Total Transaction Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("transaction_amount_over_time.png", dpi=300)
plt.show()
category_revenue = (
    df_sales.groupby("Category")["TransactionAmount"]
    .sum()
    .sort_values(ascending=False)
)
print("\nRevenue by Product Category:")
print(category_revenue)
plt.figure(figsize=(10, 6))
category_revenue.plot(kind="bar", edgecolor="black")
plt.title("Revenue by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("revenue_by_category.png", dpi=300)
plt.show()
df_customers = df_sales.dropna(subset=["CustomerNo"]).copy()
customer_spending = (
    df_customers.groupby("CustomerNo")["TransactionAmount"]
    .sum()
    .sort_values(ascending=False)
)
print("\nCustomer Purchasing Behaviour:")
print("\nTotal Unique Customers:")
print(df_customers["CustomerNo"].nunique())
print("\nTop 10 Customers by Spending:")
print(customer_spending.head(10))
top_customers = customer_spending.head(10)
plt.figure(figsize=(12, 6))
top_customers.plot(kind="bar", edgecolor="black")
plt.title("Top 10 Customers by Total Spending")
plt.xlabel("Customer ID")
plt.ylabel("Total Spending")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("top_10_customers.png", dpi=300)
plt.show()