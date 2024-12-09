import streamlit as st
import pandas as pd
import json

def app():
    st.write("WIP_DataManagement")

    #import des fichiers
    # #téléchargement des données géographiques des départements fr
    with open("C:/Users/PC/Desktop/Projet_Datamanagement/departements.geojson", "r") as file:
        geojson_dept = json.load(file)

    st.title("Dashboard des Valeurs Foncières en France en 2024")

    #importer le df dans un cache à court terme (et éviter de l'importer à chaque fois)
    @st.cache_data
    def get_data():
        # Chemin vers le cvs
        df_valeursfoncieres = pd.read_csv("clean_df_analysis.csv", low_memory=False)
        return df_valeursfoncieres
    
    df_valeursfoncieres = get_data()