
# (Removed stray code before imports)
# Streamlit app for fulfillment rate dashboard
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Fulfillment Rate Dashboard", layout="wide")

st.title("Kettle Studio Fulfillment Rate Dashboard")
st.write("Upload your Excel file to analyze fulfillment rates by PO, city, product, and more.")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

@st.cache_data
def load_data(file):
	xls = pd.ExcelFile(file)
	sheets = xls.sheet_names
	# Try to find the right sheet names
	bulk_sheet = next((s for s in sheets if "bulk" in s.lower()), sheets[0])
	fr_sheet = next((s for s in sheets if "fr" in s.lower()), sheets[-1])
	df_bulk = pd.read_excel(xls, sheet_name=bulk_sheet)
	df_fr = pd.read_excel(xls, sheet_name=fr_sheet)
	return df_bulk, df_fr

def preprocess(df):
	# Standardize column names
	df.columns = [str(c).strip().replace(" ", "_").lower() for c in df.columns]
	return df

def compute_fulfillment_metrics(df):
	# Calculate fulfillment rate per PO, city, product, etc.
	# Fulfillment = (ordered - remaining) / ordered * 100
	df["fr_percent"] = (df["units_ordered"] - df["remaining_quantity"]) / df["units_ordered"] * 100
	return df


if uploaded_file:
	df_bulk, df_fr = load_data(uploaded_file)
	df_bulk = preprocess(df_bulk)
	df_fr = preprocess(df_fr)
	st.write("## Columns in Bulk sheet after preprocessing:")
	st.write(list(df_bulk.columns))
	required_cols = ["units_ordered", "remaining_quantity"]
	missing = [col for col in required_cols if col not in df_bulk.columns]
	if missing:
		st.error(f"Missing required columns: {missing}. Please check your Excel file and column names.")
	else:
		df = df_bulk.copy()
		df = compute_fulfillment_metrics(df)

		st.success(f"Loaded {len(df)} records from Bulk sheet.")

		# Sidebar filters
		st.sidebar.header("Filters")
		# Use available columns for filters
		if "facility_name" in df.columns:
			city = st.sidebar.multiselect("Facility Name", options=sorted(df["facility_name"].dropna().unique()), default=None)
		else:
			city = None
		po_number = st.sidebar.multiselect("PO Number", options=sorted(df["po_number"].dropna().unique()), default=None)
		product = st.sidebar.multiselect("Product Name", options=sorted(df["name"].dropna().unique()), default=None)

		filtered_df = df.copy()
		if city:
			filtered_df = filtered_df[filtered_df["facility_name"].isin(city)]
		if po_number:
			filtered_df = filtered_df[filtered_df["po_number"].isin(po_number)]
		if product:
			filtered_df = filtered_df[filtered_df["name"].isin(product)]

		st.dataframe(filtered_df)

		# Fulfillment rate summary
		st.subheader("Fulfillment Rate Summary")
		summary = filtered_df.groupby(["facility_name"]).agg(
			total_units_ordered=("units_ordered", "sum"),
			total_remaining_quantity=("remaining_quantity", "sum"),
			avg_fr_percent=("fr_percent", "mean")
		).reset_index()
		summary["overall_fr_percent"] = (summary["total_units_ordered"] - summary["total_remaining_quantity"]) / summary["total_units_ordered"] * 100
		st.dataframe(summary)

		# Charts
		st.subheader("Fulfillment Rate by Facility Name")
		st.bar_chart(summary.set_index("facility_name")["overall_fr_percent"])

		st.subheader("Fulfillment Rate by Product")
		prod_summary = filtered_df.groupby(["name"]).agg(
			total_units_ordered=("units_ordered", "sum"),
			total_remaining_quantity=("remaining_quantity", "sum"),
			avg_fr_percent=("fr_percent", "mean")
		).reset_index()
		prod_summary["overall_fr_percent"] = (prod_summary["total_units_ordered"] - prod_summary["total_remaining_quantity"]) / prod_summary["total_units_ordered"] * 100
		st.dataframe(prod_summary)
		st.bar_chart(prod_summary.set_index("name")["overall_fr_percent"])

		# Download filtered data
		st.download_button(
			label="Download filtered data as CSV",
			data=filtered_df.to_csv(index=False),
			file_name="filtered_fulfillment_data.csv",
			mime="text/csv"
		)

		# Show reasons if available
		# No item_status/new_po_status columns in your sample, so skip for now
# (Removed stray code before imports)
else:
	st.info("Please upload an Excel file to begin.")
