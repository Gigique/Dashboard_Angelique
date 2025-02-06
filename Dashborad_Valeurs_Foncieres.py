import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
import matplotlib.pyplot as plt



#importer le df dans un cache à court terme (et éviter de l'importer à chaque fois)
@st.cache_data
def get_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    geojson_path = os.path.join(base_dir, "librairy", "departements.geojson")
    # Chemin vers le cvs
    csv_path = os.path.join(base_dir, "librairy", "clean_df_analysis.csv")
    df_valeursfoncieres = pd.read_csv(csv_path, low_memory=False)
    return df_valeursfoncieres, geojson_path
    
#import des fichiers
df_valeursfoncieres, geojson_path = get_data()


def app_dashboard():
    st.markdown("""<h1 style="color:#A53131;">Valeurs Foncières 2024</h1>""", unsafe_allow_html=True)

    # #téléchargement des données géographiques des départements fr
    with open(geojson_path, "r") as file:
        geojson_dept = json.load(file)

    st.markdown("""<h3 style="color:#E77866;">Dashboard des Valeurs Foncières en France en 2024</h3>""", unsafe_allow_html=True)
    
    st.markdown("""
    **Projet réalisé par un groupe de 4 étudiants dans le cadre du cours de Data Management.**  
    
    **🎯 Objectifs du projet**

   Ce projet vise à explorer et analyser des données sur les valeurs foncières en France afin d'offrir une carte interractive sur le marché immobilier dans un temps donné. 
   Il a été réalisé sur Visual Code avec Python (en utilisant des libraries telles que Seaborn, Matplotlib, Pandas ou encore Plotly) puis déployé sur Streamlit
               
   **✔️ Compétences acquises**
   
   Nous avons analysé, transformé et visualisé les données afin de ne sélectionner que les valeurs intéressantes au projet.
   Puis, nous avons visualisé nos données en réalisant des graphiques dynamiques que nous avons déployés sur Streamlit. Ces graphiques hautement interractifs permettent d'avoir des analyses précises selon des emplacements géograhiques
   Enfin, nous avons présenté et expliqué notre projet à un public                
            
   **📊 Dataset**
           
    Ce jeu de données contient des informations sur les valeurs foncières géolocalisées du 01/01/2024 au 30/06/2024, avec des colonnes détaillant les transactions immobilières.
    Cela permet d'analyser les tendances foncières et immobilières sur le territoire français, et nous avons choisi de nous focaliser sur la France métropolitaine.

    **Liens utiles :**
    - Base de données des [valeurs foncières en 2024](https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres-geolocalisees/#/community-reuses)
    - Base de données des [départements et régions](https://www.data.gouv.fr/fr/datasets/departements-de-france/)
    """, unsafe_allow_html=True)

    
    #vue d'ensemble

    st.markdown("""<h3 style="color:#E77866;">Vue d'ensemble :</h3>""", unsafe_allow_html=True)

    left_column, right_column = st.columns(2)

    #Map prix moyens m²
    fig = px.choropleth_mapbox(df_valeursfoncieres, geojson=geojson_dept, locations="code_departement", featureidkey="properties.code", color="prix_m²", color_continuous_scale="Blues", range_color=(0, 10000), 
    mapbox_style="carto-darkmatter",
    zoom=4,
    center={"lat": 46.60, "lon": 1.88},
    opacity=0.8, title ="moyenne des prix au m²")

    #Pie charte du nombre de vente tous bien confondus (régions puis départements)
    total_ventes_reg = df_valeursfoncieres.groupby("nom_region").size()

    fig_region = px.pie(total_ventes_reg, total_ventes_reg.index, total_ventes_reg.values,hole=0.3, title="Nombre total des ventes selon la région")

    plt.gcf().set_facecolor('none')
    fig_region.update_layout(showlegend=False)


    left_column.plotly_chart(fig)
    right_column.plotly_chart(fig_region)


    #répartition des ventes selon le type de bien par département selon la région
    df_region = df_valeursfoncieres[df_valeursfoncieres["nom_region"] == "Hauts-de-France"]
    df_moyenne_prix = df_region.groupby("nom_departement", as_index=False)["prix_m²"].mean()
    detail_ventes = df_region.groupby(["nom_departement", "type_local"]).size().reset_index(name="nombre_ventes")
    detail_ventes["type_local"] = detail_ventes["type_local"].replace({"Local industriel. commercial ou assimilé": "Locaux industriels<br>ou commerciaux"})

    fig_detail_ventes = px.bar(detail_ventes, x="nom_departement", y="nombre_ventes", color="type_local", title="Nombre de ventes par départements<br>selon la région")

    fig_detail_ventes.update_layout(xaxis=dict(
        tickmode='array',  
        tickvals=df_moyenne_prix["nom_departement"].tolist(),
        ticktext=df_moyenne_prix["nom_departement"].tolist()),
        width=700, height=400)
    
    fig_detail_ventes.update_layout(showlegend=False)

    #répartition des ventes selon les biens
    selected_region = ["Hauts-de-France", "Bretagne", "Grand Est"]
    region_data = df_valeursfoncieres[df_valeursfoncieres["nom_region"].isin(selected_region)]
    detail_ventes = region_data.groupby(["nom_region", "type_local"]).size().reset_index(name="nombre_ventes")
       
        
    fig_detail = px.line(detail_ventes, x="type_local", y="nombre_ventes", color="nom_region", markers=True, title="Nombre de ventes par selon le type de bien")

    fig_detail.update_layout(xaxis=dict(
        tickmode='array',
        tickvals=detail_ventes['type_local'],
        ticktext=['Appartements', 'Dépendances', 'Locaux industriels<br>ou commerciaux', 'Maisons', 'Vente']))
    
    fig_detail.update_layout(showlegend=False)   
        

    left_column.plotly_chart(fig_detail_ventes)
    right_column.plotly_chart(fig_detail)


    st.markdown("""<h6 style="color:#E77866;">Veuillez choisir un graphique dans la barre ci dessous pour plus de détail</h6>""", unsafe_allow_html=True)

    liste_graph = {
        "Moyenne des prix au m²" : prix_m2,
        "Nombre total des ventes selon la région" : vente_region,
        "Nombres de ventes par départements" : vente_dept,
        #"Nombre de ventes selon le type de biens" : vente_biens
        }
    
    graph_chosen = st.selectbox("Sélectionnez un graphique :", options=liste_graph, key = "graph_selectionne")

    if graph_chosen:
        liste_graph[graph_chosen]()
        

def prix_m2():

    # #téléchargement des données géographiques des départements fr
    with open(geojson_path, "r") as file:
        geojson_dept = json.load(file)

    fig = px.choropleth_mapbox(df_valeursfoncieres, geojson=geojson_dept, locations="code_departement", featureidkey="properties.code", color="prix_m²", color_continuous_scale="Blues", range_color=(0, 10000), 
    mapbox_style="carto-darkmatter",
    zoom=4,
    center={"lat": 46.60, "lon": 1.88},
    opacity=0.8, title ="moyenne des prix au m² selon le département")
    st.plotly_chart(fig)


def vente_region():

    #Pie chart du nombre de vente tous bien confondus (régions puis départements)
    total_ventes_reg = df_valeursfoncieres.groupby("nom_region").size()

    fig_region = px.pie(total_ventes_reg, total_ventes_reg.index, total_ventes_reg.values,hole=0.35)

    plt.gcf().set_facecolor('none')

    st.plotly_chart(fig_region)


def vente_dept():
    liste_regions = df_valeursfoncieres["nom_region"].unique()
    region_selectionnee = st.selectbox("Choisissez une région :", options=liste_regions, key = "region_selectionnee")

    df_region = df_valeursfoncieres[df_valeursfoncieres["nom_region"] == region_selectionnee]
    df_moyenne_prix = df_region.groupby("nom_departement", as_index=False)["prix_m²"].mean()

    detail_ventes = df_region.groupby(["nom_departement", "type_local"]).size().reset_index(name="nombre_ventes")
    detail_ventes["type_local"] = detail_ventes["type_local"].replace({"Local industriel. commercial ou assimilé": "Locaux industriels<br>ou commerciaux"})

    fig_detail_ventes = px.bar(detail_ventes, x="nom_departement", y="nombre_ventes", color="type_local", title=f"Nombre de ventes par départements pour {region_selectionnee}")

    fig_detail_ventes.update_layout(xaxis=dict(
        tickmode='array',  
        tickvals=df_moyenne_prix["nom_departement"].tolist(),
        ticktext=df_moyenne_prix["nom_departement"].tolist()),
        width=700, height=400)
    
    st.plotly_chart(fig_detail_ventes)
    


def vente_biens():
    liste_regions = ["Auvergne-Rhône-Alpes", "Bourgogne-Franche-Comté", "Bretagne", "Centre-Val de Loire", "Corse", "Grand Est", "Hauts-de-France", "Île-de-France", "Normandie","Nouvelle-Aquitaine", "Occitanie", "Pays de la Loire", "Provence-Alpes-Côte d'Azur"]
    region_selectionnee = st.selectbox("Région sélectionnée :", options=liste_regions)

    df_region = df_valeursfoncieres[df_valeursfoncieres["nom_region"] == region_selectionnee]
    df_moyenne_prix = df_region.groupby("nom_departement", as_index=False)["prix_m²"].mean()

   
    #répartition des ventes selon le type de bien par département selon la région
    detail_ventes = df_region.groupby(["nom_departement", "type_local"]).size().reset_index(name="nombre_ventes")
    detail_ventes["type_local"] = detail_ventes["type_local"].replace({"Local industriel. commercial ou assimilé": "Locaux industriels<br>ou commerciaux"})

    fig_detail_ventes = px.bar(detail_ventes, x="nom_departement", y="nombre_ventes", color="type_local", title=f"Nombre de ventes par départements pour {region_selectionnee}")

    fig_detail_ventes.update_layout(xaxis=dict(
        tickmode='array',  
        tickvals=df_moyenne_prix["nom_departement"].tolist(),
        ticktext=df_moyenne_prix["nom_departement"].tolist()),
        width=700, height=400)
    
    st.plotly_chart(fig_detail_ventes)

