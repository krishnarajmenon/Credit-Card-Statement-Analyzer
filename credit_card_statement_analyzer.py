import camelot # or tabula-py, or pdfplumber
import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import calendar # To convert month number to month name for plotting
# If statements are password protected, you might also need pypdf (formerly PyPDF2)
import plotly.graph_objects as go

def analyze_credit_card_statement(pdf_path, password=None):
    """
    Reads a credit card credit card statement PDF, extracts transactions,
    and calculates total spends for Swiggy, Zomato, and Blinkit.

    Args:
        pdf_path (str): The path to the PDF credit card statement.
        password (str, optional): The password for the PDF, if it's protected.

    Returns:
        dict: A dictionary with the total spends for Swiggy, Zomato, and Blinkit.
              Returns None if parsing fails.
    """
    all_transactions_df = pd.DataFrame()

    try:
        # Step 1: Read the PDF and extract tables
        # For Camelot:
        # 'lattice' mode is good for statements with clear lines separating cells
        # 'stream' mode is good for statements with less defined lines
        # Adjust pages as needed, e.g., pages='1-end' or specific page numbers
        tables = camelot.read_pdf(pdf_path, pages='1-2', flavor='lattice', password=password)

        if not tables:
            print(f"No tables found in {pdf_path}. Check PDF format or parsing mode.")
            return None

        # Concatenate all tables into a single DataFrame
        for table in tables:
            # Assuming the first row is the header, but you might need to adjust
            # based on how your Credit card statement is formatted.
            # You might need to inspect tables[0].df to identify header rows and remove them.
            all_transactions_df = pd.concat([all_transactions_df, table.df], ignore_index=True)

        # Step 2: Clean and process the DataFrame
        # Credit card statements typically have columns like 'Date', 'Transaction Description', 'Amount' (or 'Debit/Credit')
        # You'll need to identify the correct column names from your actual statement.
        # Let's assume for now they are 'Transaction Description' and 'Amount'.
        # You might need to rename columns if Camelot extracts them differently.

        # Example of column renaming (adjust to your actual statement):
        # all_transactions_df.columns = ['Date', 'Description', 'Ref No', 'Debit', 'Credit', 'Balance', ...]
        # You'll need to figure out which column contains the transaction description and amount.

        # A common issue is that amounts might be strings with commas or currency symbols.
        # Convert the 'Amount' column to numeric, handling potential non-numeric values.
        # You'll likely have separate Debit and Credit columns or a single Amount column with signs.
        # Let's assume a single 'Amount' column that is negative for debits (spends) and positive for credits.
        # If your statement has separate Debit/Credit columns, you'll need to combine them.

        # For demonstration, let's assume 'Description' and 'Amount' columns exist.
        # You MUST inspect your actual statement's extracted data to get the correct column names.
        # For example, if it extracts as df[0], df[1], df[2], etc., you'll need to map them.

        # **IMPORTANT: You need to inspect your actual credit card statement's raw output
        # to correctly identify the columns for transaction description and amount.**
        # Print tables[0].df to see the raw extracted data.

        # Let's assume after inspecting, you find the description in column 'Description' and amount in 'Amount'
        # Or, if they're not explicitly named, use index like all_transactions_df.iloc[:, X]
        # For example:
        # transaction_description_col_index = 2 # Example index
        # amount_col_index = 4 # Example index

        # For this example, let's just clean common issues
        # (This part is highly dependent on your statement's exact format)
        # Assuming you've loaded it into a DataFrame with columns that contain relevant data.

        # Let's assume a simplified scenario where you have a 'Description' and 'Amount' column
        # You might need to clean the 'Amount' column (remove commas, currency symbols, convert to numeric)
        # You might also need to handle credit vs. debit amounts if they are in separate columns or negative.

        # Filter out rows that are likely not transaction line items (e.g., summary rows, headers repeated)
        # This is a generic example; you might need more specific filters
        # Remove rows where the description or amount is empty, or clearly a header.
        all_transactions_df.dropna(subset=[all_transactions_df.columns[0]], inplace=True) # Drop rows with empty first column

        # If your statement has a 'Description' and 'Amount' column
        # Replace 'Description_Col_Name' and 'Amount_Col_Name' with actual names
        # You will need to inspect the `tables[0].df` output to find the correct column indices or names.
        # For example:
        # description_col = all_transactions_df.columns[2] # Example: 3rd column is description
        # amount_col = all_transactions_df.columns[4]    # Example: 5th column is amount

        # Let's assume after initial extraction and inspection, your DataFrame has columns that roughly correspond
        # to 'Transaction_Description' and 'Transaction_Amount' (adjust column names based on your actual statement)
        # A common pattern is to have 'Debit' and 'Credit' columns or a single 'Amount' column.
        # If it's a single 'Amount' column, debits are usually positive, credits negative, or vice-versa.
        # Let's assume debits are positive in a column we'll call 'Amount'.
        
        # This is a placeholder for actual column identification.
        # You will need to adjust these based on your statement.
        # For example, if your statement has columns 'Date', 'Particulars', 'Amount (DR)', 'Amount (CR)'
        # You'd need to combine 'Amount (DR)' and 'Amount (CR)' into a single 'Amount' column.
        # Example for a simple case:
        
        # Example of how to find relevant columns - you might need to manually check
        # for col in all_transactions_df.columns:
        #     print(f"Column: {col}, Sample Data: {all_transactions_df[col].head()}")

        # Let's assume a 'Description' and 'Amount' column are identified after cleaning and re-indexing.
        # For robust parsing, you might need to set column headers explicitly after extraction.
        # E.g., all_transactions_df.columns = ['col1', 'Date', 'Description', 'Debit', 'Credit', ...]

        # For the sake of this example, let's simulate the columns you'd eventually get:
        # Assuming your DataFrame has a 'Description' and 'Amount' column (after renaming/processing)
        # You might need to implement logic to identify these columns dynamically or hardcode after analysis.

        # Let's assume the relevant columns are `Description` and `Amount`
        # First, ensure 'Amount' is numeric.
        # Try to convert to numeric, coercing errors to NaN. Then fill NaN with 0.
        
        # THIS IS THE MOST CRITICAL PART - IDENTIFYING THE CORRECT COLUMNS.
        # You will likely have to run the `camelot.read_pdf` part and print `tables[0].df`
        # to understand the exact column structure from your credit card statement.
        # Once you know the column indices or names, you can uncomment and adapt the following:

        # Example of cleaning and preparing data (Highly dependent on actual statement format)
        # This is a generic approach; actual implementation will vary.
        # transactions = []
        # for _, row in all_transactions_df.iterrows():
        #     # Heuristics to find description and amount columns
        #     # This is a very simplistic example. You'll need more robust logic.
        #     description = ""
        #     amount = 0.0
        #     for item in row.values:
        #         if isinstance(item, str) and (("SWIGGY" in item.upper()) or ("ZOMATO" in item.upper()) or ("BLINKIT" in item.upper())):
        #             description = item
        #         try:
        #             # Try to parse as float, handling commas and currency symbols
        #             clean_amount = float(str(item).replace(',', '').replace('INR', '').strip())
        #             amount = clean_amount
        #         except ValueError:
        #             pass
        #     if description and amount:
        #         transactions.append({'Description': description, 'Amount': amount})
        # processed_df = pd.DataFrame(transactions)

        # A more robust approach for cleaning the DataFrame after extraction:
        # Assuming tables[0].df is the main table and it has transaction data.
        # You'll need to carefully inspect the columns after `camelot.read_pdf`.
        # For example, if transactions are in column 2 (description) and column 4 (amount):
        
        # Let's assume for this example, after initial extraction, you have a DataFrame
        # where the transaction description is in a column that contains text like "SWIGGY"
        # and the amount is in a column that contains numerical values for transactions.
        
        # Let's try to infer columns if not explicitly named by Camelot
        description_col = all_transactions_df.columns[1]
        amount_col = all_transactions_df.columns[6]
        date_col = all_transactions_df.columns[0]  # Default to first column

        # Try to find date column (format: dd/mm/yyyy or dd-mm-yyyy)
        date_pattern = re.compile(r'\d{2}[-/]\d{2}[-/]\d{4}')
        for col_name in all_transactions_df.columns:
            sample_data = all_transactions_df[col_name].astype(str).str.strip()
            date_matches = sample_data.apply(lambda x: bool(date_pattern.match(x)))
            if date_matches.sum() / len(sample_data) > 0.5:
                date_col = col_name
                break

        # Heuristic: Find a column that contains text that looks like a description (mix of letters and numbers)
        # and another that looks like an amount (mostly numbers, potentially with decimal/comma)
        for col_name in all_transactions_df.columns:
            sample_data = all_transactions_df[col_name].astype(str).str.upper().str.strip()
            if any("SWIGGY" in s or "ZOMATO" in s or "BLINKIT" in s for s in sample_data):
                description_col = col_name
            # Heuristic for amount column: try converting to numeric and check if successful for most
            try:
                numeric_series = all_transactions_df[col_name].astype(str).str.replace(',', '').apply(pd.to_numeric, errors='coerce')
                if numeric_series.count() / len(numeric_series) > 0.7: # If more than 70% can be numeric
                    amount_col = col_name
            except Exception:
                pass

        if not description_col or not amount_col:
            print("Could not identify description or amount columns automatically. Manual inspection needed.")
            print("Extracted DataFrame head:")
            print(all_transactions_df.head())
            print("Please identify the correct column names/indices for transaction description and amount.")
            return None
        
        # Clean the amount column
        all_transactions_df[amount_col] = all_transactions_df[amount_col].astype(str).str.replace(',', '').apply(pd.to_numeric, errors='coerce')
        all_transactions_df.dropna(subset=[amount_col], inplace=True) # Drop rows where amount couldn't be parsed

        # Credit Card statements often have separate debit and credit columns,
        # or a single amount column where debits are positive.
        # You'll need to verify how your statement presents spending (debits).
        # Assuming for now that the extracted 'Amount' column directly represents debits (spends).
        # If your statement has 'Debit' and 'Credit' columns, you'd combine them:
        # df['Amount'] = df['Debit'].fillna(0) - df['Credit'].fillna(0) # or just df['Debit'] for spends

        # Step 3: Identify Swiggy, Zomato, and Blinkit spends
        swiggy_spends = 0.0
        zomato_spends = 0.0
        blinkit_spends = 0.0

        for index, row in all_transactions_df.iterrows():
            description = str(row[description_col]).upper() # Ensure string and uppercase for consistent matching
            amount = float(row[amount_col])

            # Assuming spends are positive amounts in the 'Amount' column.
            # If your statement has separate debit/credit columns, ensure you're using the debit amount.
            # If the amount is negative for debits, adjust accordingly (e.g., amount = abs(amount))

            if "SWIGGY" in description:
                swiggy_spends += amount
            elif "ZOMATO" in description:
                zomato_spends += amount
            elif "BLINKIT" in description:
                blinkit_spends += amount

        return {
            "Swiggy": round(swiggy_spends, 2),
            "Zomato": round(zomato_spends, 2),
            "Blinkit": round(blinkit_spends, 2)
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# --- How to use the program ---
if __name__ == "__main__":
    statements_folder = os.path.abspath(os.path.join('..', 'statements1')) # Folder containing your PDF statements
    pdf_password = None # Set to None if not password protected

    monthly_spends_data = {} # To store {month_name: {category: spend}}

    # Regular expression to extract month (3-letter abbr) and year from filenames
    # Assumes format like "Jan_2025_StandardChartered.pdf"
    filename_pattern = re.compile(r'([A-Za-z]{3})_(\d{4})_.*\.pdf')

    # Get a sorted list of files to ensure chronological processing
    pdf_files = sorted([f for f in os.listdir(statements_folder) if f.endswith('.pdf')])

    for filename in pdf_files:
        match = filename_pattern.match(filename)
        if match:
            month_abbr = match.group(1)
            year = match.group(2)
            
            # Convert month abbreviation to month number (1-12)
            try:
                month_number = list(calendar.month_abbr).index(month_abbr.capitalize())
            except ValueError:
                print(f"Could not parse month from filename: {filename}. Skipping.")
                continue

            # Create a sortable key for months (e.g., "2025-01", "2025-02")
            month_key = f"{year}-{month_number:02d}" 
            month_name_full = calendar.month_name[month_number] # Full month name for display

            pdf_file_path = os.path.join(statements_folder, filename)
            print(f"\n--- Analyzing {filename} ---")
            spends = analyze_credit_card_statement(pdf_file_path, pdf_password)

            print(f"Spends for {month_name_full} {year}: {spends}")

            if spends:
                monthly_spends_data[month_key] = spends
            else:
                print(f"Failed to analyze {filename}.")

            print(monthly_spends_data)
        else:
            print(f"Filename '{filename}' does not match the expected pattern. Skipping.")

    if not monthly_spends_data:
        print("No valid monthly spend data found to plot.")
    else:
        # Sort data by month key (e.g., "2025-01", "2025-02")
        sorted_months = sorted(monthly_spends_data.keys())
        
        # Prepare data for plotting
        categories = ["Swiggy", "Zomato", "Blinkit"] # The keys returned by analyze_credit_card_statement
        
        # Initialize dictionaries to hold spend data for each category across months
        category_spends_for_plotting = {category: [] for category in categories}
        display_months = [] # To store month names for x-axis labels

                # ...existing code up to...
        for month_key in sorted_months:
            spends_for_month = monthly_spends_data[month_key]
            print(f"Processing month: {month_key} with spends: {spends_for_month}")
            year, month_num_str = month_key.split('-')
            month_name = calendar.month_abbr[int(month_num_str)]
            display_months.append(f"{month_name} {year}")
            for category in categories:
                category_spends_for_plotting[category].append(spends_for_month.get(category, 0))
        
        # --- Plotly Interactive Line Chart ---
        fig = go.Figure()
        for category in categories:
            spends_list = category_spends_for_plotting[category]
            if any(s > 0 for s in spends_list):
                fig.add_trace(go.Scatter(
                    x=display_months,
                    y=spends_list,
                    mode='lines+markers',
                    name=category
                ))
            else:
                print(f"No spends found for {category} across the analyzed months. Not including in combined plot.")
        
        fig.update_layout(
            title='Monthly Spends by Category (Swiggy, Zomato, Blinkit)',
            xaxis_title='Month',
            yaxis_title='Spend (INR)',
            legend_title='Category',
            xaxis_tickangle=-45,
            template='plotly_white',
            width=1000,
            height=600
        )
        fig.show()
        
        # --- Show Top 15 Spends of the Last Month in a Grid (Plotly Table) ---
        if sorted_months:
            last_month_key = sorted_months[-1]
            last_month_filename = None
            for filename in pdf_files:
                match = filename_pattern.match(filename)
                if match:
                    month_abbr = match.group(1)
                    year = match.group(2)
                    month_number = list(calendar.month_abbr).index(month_abbr.capitalize())
                    month_key = f"{year}-{month_number:02d}"
                    if month_key == last_month_key:
                        last_month_filename = filename
                        break
        
            if last_month_filename:
                pdf_file_path = os.path.join(statements_folder, last_month_filename)
                tables = camelot.read_pdf(pdf_file_path, pages='1-2', flavor='lattice', password=pdf_password)
                all_transactions_df = pd.DataFrame()
                for table in tables:
                    all_transactions_df = pd.concat([all_transactions_df, table.df], ignore_index=True)
                all_transactions_df.dropna(subset=[all_transactions_df.columns[0]], inplace=True)
        
                # Infer columns as before
                description_col = all_transactions_df.columns[1]
                amount_col = all_transactions_df.columns[6]
                date_col = all_transactions_df.columns[0]
                date_pattern = re.compile(r'\d{2}[-/]\d{2}[-/]\d{4}')
                
                for col_name in all_transactions_df.columns:
                    sample_data = all_transactions_df[col_name].astype(str).str.strip()
                    date_matches = sample_data.apply(lambda x: bool(date_pattern.match(x)))
                    if date_matches.sum() / len(sample_data) > 0.5:
                        date_col = col_name
                        break
                
                for col_name in all_transactions_df.columns:
                    sample_data = all_transactions_df[col_name].astype(str).str.upper().str.strip()
                    if any("SWIGGY" in s or "ZOMATO" in s or "BLINKIT" in s for s in sample_data):
                        description_col = col_name
                    try:
                        numeric_series = all_transactions_df[col_name].astype(str).str.replace(',', '').apply(pd.to_numeric, errors='coerce')
                        if numeric_series.count() / len(numeric_series) > 0.7:
                            amount_col = col_name
                    except Exception:
                        pass
        
                all_transactions_df[amount_col] = all_transactions_df[amount_col].astype(str).str.replace(',', '').apply(pd.to_numeric, errors='coerce')
                all_transactions_df.dropna(subset=[amount_col], inplace=True)
        
                # Sort by amount descending and get top 15
                top_spends = all_transactions_df.sort_values(by=amount_col, ascending=False).head(15)

                # Before preparing data for the table, format the date column
                top_spends[date_col] = pd.to_datetime(
                    top_spends[date_col], errors='coerce', dayfirst=True
                ).dt.strftime('%d %b %Y')

                # Prepare data for table
                table_data = []
                for _, row in top_spends.iterrows():
                    desc = str(row[description_col])[:50]
                    amt = f"{row[amount_col]:,.2f}"
                    table_data.append([desc, amt])
        
                fig = go.Figure(data=[go.Table(
                    header=dict(values=["Date", "Description", "Amount (INR)"], fill_color='paleturquoise', align='left'),
                    cells=dict(values=[
                        top_spends[date_col].astype(str),
                        top_spends[description_col].astype(str).str[:50],
                        top_spends[amount_col].map('{:,.2f}'.format)
                    ],
                    fill_color='lavender', align='left'))
                ])
                fig.update_layout(width=1000, height=40*len(top_spends)+100, title="Top 15 Spends")
                fig.show()
            else:
                print("Could not find the PDF file for the last month.")
        
        print("\n--- Monthly Spends Summary ---")
        print(f"{'Month':<15} | {'Swiggy':<10} | {'Zomato':<10} | {'Blinkit':<10}")
        print("-" * 55)
        for month_key in sorted_months:
            year, month_num_str = month_key.split('-')
            month_name = calendar.month_abbr[int(month_num_str)]
            spends = monthly_spends_data[month_key]
            print(f"{month_name} {year:<9} | {spends.get('Swiggy', 0):<10.2f} | {spends.get('Zomato', 0):<10.2f} | {spends.get('Blinkit', 0):<10.2f}")
        