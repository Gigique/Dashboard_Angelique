import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant




#étude de corrélation
def correlation(df):

   st.markdown("""<h6 style="color:#E77866;">Test de corrélation avec le taux d'insertion</h6>""", unsafe_allow_html=True)

   # Création de la heatmap avec Plotly Express
   fig = px.imshow(
      df.corr(), 
      text_auto=".2f", 
      color_continuous_scale='RdBu_r', 
      zmin=-1, zmax=1,  # Pour centrer la couleur sur zéro
      labels=dict(color="Corrélation")  # Légende personnalisée
   )

    # Mise à jour de la mise en page pour ajuster la taille
   fig.update_layout(
      title="Heatmap des corrélations",
      title_x=0.3,
      title_font=dict(size=20),  # Taille du titre
      width=800,  # Largeur de la figure
      height=800,  # Hauteur de la figure
      coloraxis_colorbar=dict(
         title="Corrélation avec le taux d'insertion",
         title_side="right",
         ticks="outside",
         ticklen=5,
         tickfont=dict(size=12),  # Taille des ticks de la légende
      )
   )

    # Affichage de la figure dans Streamlit
   st.plotly_chart(fig)


   st.markdown("""<h6 style="color:#E77866;">Analyse de la multicolinéarité</h6>""", unsafe_allow_html=True)

   # Calcul des VIF
   vif_df = calculate_vif(df)

   df_vif_filtered = vif_df[vif_df['Variable'] != 'const']

   # Création du Bar Plot avec Plotly
   fig = px.bar(df_vif_filtered, x='Variable', y='VIF', text='VIF', color='VIF',
             color_continuous_scale='Viridis', title="Variance Inflation Factors (VIF)")
   fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
   fig.add_hline(y=10, line_dash="dash", line_color="red", annotation_text="Seuil (VIF=10)", annotation_position="top left")

   # Affichage dans Streamlit
   st.plotly_chart(fig)

   #analyse de la corrélation

   st.markdown("""<h6 style="color:#E77866;">Analyse de l'étude</h6>""", unsafe_allow_html=True)

   st.markdown(""" Les variables choisies sont intéressantes au niveau de leur corrélation avec le taux d'insertion mais aussi par leur intérêt social.
               

   Si certains n'ont pas une corrélation significative avec notre variable cible, il était néanmoins nécessaire de les ajouter pour les étudier. C'est par exemple le cas de la Part des femmes ou bien le domaine.
               

   Nous observons aussi un VIF relativement bas, indicant une absence de multicolinéarité, nécessaire pour notre étude statistique.
   """, unsafe_allow_html=True)


def calculate_vif(df):

   X=df.drop(columns = ["Taux d’insertion"])
   X= add_constant(df)

   vif_data = pd.DataFrame()
   vif_data["Variable"] = X.columns
   vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

   return vif_data

