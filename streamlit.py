# Purpose: Streamlit app for testing
import streamlit as st
from  pyairtable  import Table
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
from st_aggrid import AgGrid



def main():
    load_dotenv()
    if 'STREAMLIT_SHARING' in os.environ:
        airtable_api_key = st.secrets["AIRTABLE_API_KEY"] | os.getenv("AIRTABLE_API_KEY")
        airtable_base_id = st.secrets["AIRTABLE_BASE_ID"] | os.getenv("AIRTABLE_BASE_ID")
        airtable_table_name = os.getenv("AIRTABLE_TABLE_NAME")    
    else:
        airtable_api_key = os.getenv("AIRTABLE_API_TOKEN")
        airtable_base_id = os.getenv("AIRTABLE_BASE_ID")
        airtable_table_name = os.getenv("AIRTABLE_TABLE_NAME")    
    
    # print (airtable_api_key)
    # print (airtable_base_id)
    # print (airtable_table_name)

    # airtable_api_key = "patHs2G0VbeTXOxvW.4be741a1854bb51641a04a0990f95404b08dafa06441eb5211e35eb59e13fff3"
    # airtable_base_id = "app4IZo9AHBqykAEr"
    # airtable_table_name = "tblMHZA4IP4Ay4AM7"

    #at = airtable.Airtable(airtable_base_id, airtable_table_name, airtable_api_key)
    at = Table(airtable_api_key, airtable_base_id,  airtable_table_name)
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
            at.create(fields)

    table = at.all()
    df = pd.DataFrame([record.get('fields') for record in table])

    # Use Ag-Grid to display the data in a table that allows sorting, filtering and paging
    AgGrid(df)

if __name__ == "__main__":
    main()
