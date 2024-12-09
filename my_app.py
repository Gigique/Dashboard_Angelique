import streamlit as st



st.set_page_config(page_title="Home", layout="wide")
pages = {
    "Accueil": [
        st.Page("Accueil.py", title="Accueil")
    ],
    "Projets": [
        st.Page("Dashborad_Valeurs_Foncieres.py", title="Valeurs Foncières 2024",),
        st.Page("Dashborad_Course_Sportive.py", title="Course de rameur"),
    ],
}


def main():
    # Affichage du logo
    logo_path = "C:/Users/PC/Desktop/CV_Angelique_Bidot/librairy/Logo_AB_blanc_baniere_2.png"
    st.logo(logo_path, size="large", link=None, icon_image=logo_path)


# Navigation des pages
pg = st.navigation(pages)

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
