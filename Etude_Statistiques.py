import streamlit as st
import pandas as pd


import os

#importer le df dans un cache à court terme (et éviter de l'importer à chaque fois)
@st.cache_data
def get_data():
   base_dir = os.path.dirname(os.path.abspath(__file__))
    
   # Chemin vers le cvs
   csv_path = os.path.join(base_dir, "librairy", "df_final.csv")
   df = pd.read_csv(csv_path, low_memory=False)
   return df

df = get_data()

selected_features = [
"Taux d’insertion",
"Part des emplois stables",
"Part des emplois de niveau cadre ou profession intermédiaire",
"Part des femmes",
"Part des diplômés boursiers dans la discipline",
"Domaine_encoded",
"Taux de chômage national"
]


# Préparation des variables X et y
y = df["Taux d’insertion"]
X = df[selected_features]

# Fonction pour réduire la longueur des noms de colonnes
def shorten_column_names(column_name):
    
   return column_name[:20] + '...' if len(column_name) > 20 else column_name

# Renommer les colonnes avec des noms raccourcis
shortened_columns = {col: shorten_column_names(col) for col in X.columns}
df_shortened = X.rename(columns=shortened_columns)



def etude_stat():
   st.markdown("""<h1 style="color:#A53131;">Etude statistique</h1>""", unsafe_allow_html=True)
   st.markdown("""<h3 style="color:#E77866;">étude statistique du taux d'insertion</h3>""", unsafe_allow_html=True)
    
   st.markdown("""
   **Projet réalisé par un groupe de 4 étudiants dans le cadre du cours de Statistiques.**  
    
   Ce jeu de données provient du Ministère de l'Enseignement Supérieur et de la Recherche, et contient des informations sur l'insertion professionnelle des diplômés de Master en universités et établissements assimilés. 
   
   
   Après une rapide analyse, un nettoyage et une sélection des données les plus intéressantes, nous avons réalisé notre analyse statistique. 
   

   **Liens utiles :**
   - Base de données utilisée [ici](https://explore.data.gouv.fr/fr/datasets/586dae65a3a7290df6f4be90/?Genre__exact=hommes#/resources/c7c9642b-9fa1-40a0-83d5-1615c15b4178)
   """, unsafe_allow_html=True)



   st.markdown("""<h6 style="color:#E77866;">Veuillez choisir une analyse statistique : </h6>""", unsafe_allow_html=True)


   page = st.selectbox("Sélectionnez un test statistique :", ["", "Test de corrélation", "Régression linéaire"])

   if page == "":
      st.write("Veuillez électionner un test statistique ci dessus")


   if page == "Test de corrélation":
      import Test_Correlation
      Test_Correlation.correlation(df_shortened)

   if page == "Régression linéaire":
      import Regression_Lineaire
      Regression_Lineaire.regression(df_shortened)
   
        
   