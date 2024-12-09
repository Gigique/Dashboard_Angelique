import streamlit as st
import pandas as pd
import json
import os




def app_dashboard():
    st.title("Valeurs Foncières 2024")
    st.write("WIP_DataManagement")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    geojson_path = os.path.join(base_dir, "librairy", "departements.geojson")

    #import des fichiers
    # #téléchargement des données géographiques des départements fr
    with open(geojson_path, "r") as file:
        geojson_dept = json.load(file)

    st.title("Dashboard des Valeurs Foncières en France en 2024")

    #importer le df dans un cache à court terme (et éviter de l'importer à chaque fois)
    @st.cache_data
    def get_data():
        # Chemin vers le cvs
        csv_path = os.path.join(base_dir, "librairy", "clean_df_analysis.csv")
        df_valeursfoncieres = pd.read_csv(csv_path, low_memory=False)
        return df_valeursfoncieres
    
    df_valeursfoncieres = get_data()

    