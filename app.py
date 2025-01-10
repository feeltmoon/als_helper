import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

def main():
    st.title("Upload ALS Excel and Save to SQLite")

    # File uploader
    uploaded_file = st.file_uploader("Upload XLSX file named ALS", type="xlsx")
    if uploaded_file is not None:
        # Read all sheets into a dictionary of DataFrames
        all_sheets = pd.read_excel(uploaded_file, sheet_name=None, engine='openpyxl')

        # Define which sheets we actually care about
        required_sheets = [
            "Forms",
            "Fields",
            "Folders",
            "DataDictionaries",
            "DataDictionaryEntries",
            "Checks",
            "CheckSteps",
            "CheckActions",
            "Derivations",
            "DerivationSteps",
            "CustomFunctions"
        ]

        # Create or connect to an SQLite database
        engine = create_engine("sqlite:///local_data.db")

        st.write("All sheets found in the uploaded file:")
        st.write(list(all_sheets.keys()))

        # Dictionary to store successfully processed DataFrames
        processed_dfs = {}

        # Iterate through the list of required_sheets, process only if present
        for sheet_name in required_sheets:
            if sheet_name in all_sheets:
                df = all_sheets[sheet_name]
                # Save the DataFrame to SQLite
                df.to_sql(sheet_name, con=engine, if_exists="replace", index=False)
                st.success(f"Sheet '{sheet_name}' has been written to the SQLite database!")
                processed_dfs[sheet_name] = df  # Save DataFrame for later display
            else:
                st.warning(f"'{sheet_name}' not found in the uploaded file; skipping.")

        st.write("Done processing all required sheets.")

        # Display radio buttons for each sheet and show corresponding DataFrame
        if processed_dfs:
            selected_sheet = st.radio(
                "Select a sheet to view its content:",
                horizontal=True,
                options=list(processed_dfs.keys())
            )
            if selected_sheet:
                st.write(f"Displaying first 5 rows of the '{selected_sheet}' sheet:")
                st.dataframe(processed_dfs[selected_sheet].head())

if __name__ == "__main__":
    main()
