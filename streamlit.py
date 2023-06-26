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
# Setup session state
if "question" not in st.session_state:
    st.session_state.question = ""
if "quantity_required" not in st.session_state:
    st.session_state.quantity_required = 1
if "ai_equivalent" not in st.session_state:
    st.session_state.ai_equivalent = ""
if "resulting_query" not in st.session_state:
    st.session_state.resulting_query = ""

search_term = st.sidebar.text_input("Rechercher", value="", max_chars=20, key="search_term")

st.sidebar.markdown("""
    ## Instructions

    Cette application est destinée à être utilisée conjointement avec AIHelperBot. Les données que nous construisons ici seront utilisées pour créer des requêtes textuelles similaires afin d'éliminer les redondances et de réduire les coûts liés à l'IA.
    
    1. Utilisez la boîte de recherche dans la barre latérale pour filtrer les données. Vous pouvez rechercher des termes présents dans n'importe quelle colonne du tableau.
    
    2. Pour ajouter un nouvel enregistrement à la base de données, remplissez les champs sous le titre "Entrez, dans vos propres mots, ce que vous voulez demander à la base de données" et cliquez sur "Soumettre". Le nouvel enregistrement apparaîtra dans le tableau ci-dessous.
    
    3. Vous pouvez trier les données en cliquant sur l'en-tête d'une colonne. Un second clic inversera l'ordre de tri.

    """)

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
    
    at = Table(airtable_api_key, airtable_base_id,  airtable_table_name)
    st.title('Application d\'extraction de requêtes')
    st.write("Entrez, dans vos propres mots, ce que vous voulez demander à la base de données")

    # Add inputs
    with st.form(key='insert_record'):
        question = st.text_input('Question:', key='question', value=st.session_state.question)
        quantity_required = st.number_input('Quantité Requise:', key='quantity_required',value=st.session_state.quantity_required  )
        ai_equivalent = st.text_input('Equivalent IA:', key='ai_equivalent', value=st.session_state.ai_equivalent)
        resulting_query = st.text_area('Requête Résultante:', key='resulting_query', value=st.session_state.resulting_query )
        submit = st.form_submit_button('Soumettre')

        if submit:
            fields = {
                "Question": question,
                "Quantity Required": int(quantity_required),
                "AI Equivalent": ai_equivalent,
                "Resulting Query": resulting_query
            }
            at.create(fields)
           
            # Reset session_state

            

    table = at.all()
    df = pd.DataFrame([record.get('fields') for record in table])
    if search_term:
        df_filtered = df[df.apply(lambda row: search_term.lower() in ' '.join(row.astype(str)).lower(), axis=1)]

    else:
        df_filtered = df

    rename_dict = {
    'Question': 'Question',
    'Quantity Required': 'Quantité Requise',
    'AI Equivalent': 'Équivalent IA',
    'Resulting Query': 'Requête Résultante'
}

# Rename columns.
    df.rename(columns=rename_dict, inplace=True)

    # Use Ag-Grid to display the data in a table that allows sorting, filtering and paging
    #AgGrid(df)
    AgGrid(
        df_filtered,
        editable=True,
        sortable=True,
        filter=True,
        resizable=True,
        height=600,  # Set a custom height
        fit_columns_on_grid_load=True
    )

def resetState():
    st.session_state.question = ""
    st.session_state.quantity_required = 1
    st.session_state.ai_equivalent = ""
    st.session_state.resulting_query = ""
   

if __name__ == "__main__":
    main()
