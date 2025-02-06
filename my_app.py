import streamlit as st
import os

from Accueil import home_page
from Dashborad_Valeurs_Foncieres import app_dashboard, get_data
from Etude_Statistiques import etude_stat
from Dashborad_Course_Sportive import dashboard_sportif


base_dir = os.path.dirname(os.path.abspath(__file__))

# Affichage du logo
#logo_path = os.path.join(base_dir, "librairy", "Logo_AB_blanc_baniere_2.png")
#st.logo(logo_path, size="large", link=None, icon_image=None)
#st.image(logo_path, caption="Logo", use_column_width=True)


def main():
    
    accueil = st.Page(home_page, title = "Home Page")
    projet1 = st.Page(app_dashboard, title = "Projet Valeurs Foncieres") 
    projet2 = st.Page(etude_stat, title = "Etude Statistique")
    #projet3 = st.Page(dashboard_sportif, title = "Projets Course Sportive") 
    
    # Navigation des pages
    pg = st.navigation([accueil, projet1, projet2])
    # Démarrage de la page sélectionnée
    pg.run()

    
if __name__ == "__main__":
    main()


#customiser le rendu
hide_st_style = """
<style>
#MainMenu {visibility : hidden;}
footer {visibility : hidden;}
header {visibility : hidden;}
<style>"""

st.markdown(hide_st_style, unsafe_allow_html=True)
