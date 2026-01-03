# Kettle Studio Fulfillment Rate Dashboard

This Streamlit app lets you upload an Excel file (with Bulk and FR sheets) and interactively analyze fulfillment rates by PO, city, product, and more.

## Features
- Upload Excel file (monthly, flexible)
- Filter by city, PO number, product
- See fulfillment rates and reasons
- Download filtered data as CSV
- Visual charts for city/product

## How to Run

1. Install requirements:
   ```
   pip install -r requirements.txt
   ```
2. Start the app:
   ```
   streamlit run app.py
   ```
3. Open the browser link shown in the terminal.

## File Format
- The Excel file should have at least one sheet with PO data (Bulk) and optionally a second sheet (FR).
- The app auto-detects sheet names containing 'bulk' and 'fr'.

## Test
- To check import and core logic:
   ```
   python -m tests.test_app_import
   ```
