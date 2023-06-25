# Purpose: Streamlit app for testing
import streamlit as st
from airtable import airtable
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
from st_aggrid import AgGrid


if 'STREAMLIT_SHARING' in os.environ:
    airtable_api_key = st.secrets["AIRTABLE_API_KEY"]
    airtable_base_id = st.secrets["AIRTABLE_BASE_ID"]
else:
    load_dotenv()
    airtable_api_key = os.getenv("AIRTABLE_API_KEY")
    airtable_base_id = os.getenv("AIRTABLE_BASE_ID")    
def main():

    
    at = airtable.Airtable(airtable_base_id, airtable_api_key)

    st.title('Query Extraction App')

    st.write("Enter, in your own words, what you want to ask the database")

    # Add inputs
    with st.form(key='insert_record'):
        question = st.text_input('Question:')
        quantity_required = st.text_input('Quantity Required:')
        ai_equivalent = st.text_input('AI Equivalent:')
        resulting_query = st.text_input('Resulting Query:')
        submit = st.form_submit_button('Submit')

        if submit:
            fields = {
                "Question": question,
                "Quantity Required": int(quantity_required),
                "AI Equivalent": ai_equivalent,
                "Resulting Query": resulting_query
            }
            at.create("tblMHZA4IP4Ay4AM7", fields)

    table = at.get("tblMHZA4IP4Ay4AM7").get('records')
    df = pd.DataFrame([record.get('fields') for record in table])

    # Use Ag-Grid to display the data in a table that allows sorting, filtering and paging
    AgGrid(df)

if __name__ == "__main__":
    main()
