# Purpose: Streamlit app for testing
import streamlit as st
from  pyairtable  import Table
from streamlit import components
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
from st_aggrid import AgGrid

st.set_page_config(layout='wide')

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
    #AgGrid(df)
    AgGrid(
        df,
        editable=True,
        sortable=True,
        filter=True,
        resizable=True,
        height=600,  # Set a custom height
        fit_columns_on_grid_load=True
    )

    delete_index = st.number_input('Index to Delete', value=-1)
    if delete_index >= 0 and delete_index < len(df):
        st.write('You are about to delete the following record:')
        st.table(df.loc[delete_index])
        if st.button('Confirm Delete'):
            # Delete the row from the DataFrame
            df = df.drop(delete_index)

            # Delete the row from the Airtable
            record_id = table[delete_index]['id']
            at.delete(record_id)


    edit_index = st.number_input('Index to Edit', value=-1)
    if edit_index >= 0 and edit_index < len(df):
        # Get new values from the user
        question = st.text_input('New Question:')
        quantity_required = st.text_input('New Quantity Required:')
        ai_equivalent = st.text_input('New AI Equivalent:')
        resulting_query = st.text_input('New Resulting Query:')

        if st.button('Submit Edits'):
            # Update the DataFrame
            df.loc[edit_index, 'Question'] = question
            df.loc[edit_index, 'Quantity Required'] = int(quantity_required)
            df.loc[edit_index, 'AI Equivalent'] = ai_equivalent
            df.loc[edit_index, 'Resulting Query'] = resulting_query

            # Update the Airtable
            record_id = table[edit_index]['id']
            fields = {
                "Question": question,
                "Quantity Required": int(quantity_required),
                "AI Equivalent": ai_equivalent,
                "Resulting Query": resulting_query
            }
            at.update(record_id, fields)

if __name__ == "__main__":
    main()
