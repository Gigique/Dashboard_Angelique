import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

from scipy.stats import shapiro, normaltest, skew, kurtosis, kstest
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_goldfeldquandt
from statsmodels.stats.stattools import durbin_watson


#étude de corrélation
def regression(df):

   st.markdown("""<h6 style="color:#E77866;">Regression Linéaire</h6>""", unsafe_allow_html=True)

   # Préparation des variables X et y
   y = df["Taux d’insertion"]
   X = df.drop(columns = ["Taux d’insertion"])


   """Analyse complète du modèle"""
   try:
      # Ajustement du modèle
      model = sm.OLS(y, X).fit()
      y_pred = model.predict(X)
      residuals = y - y_pred


      # 1. Distribution des résidus
      fig = px.histogram(residuals, nbins=50, title="Distribution des résidus")
      fig.update_layout(bargap=0.05)
      st.plotly_chart(fig)

      

      """# 2. Q-Q Plot
      fig = plt.figure(figsize=(10, 6))  
      sm.graphics.qqplot(residuals, line='45', ax=fig.add_subplot(111))  
      plt.title("Q-Q Plot des résidus")
      fig.patch.set_visible(False)  
      fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
      st.pyplot(fig)"""

      # 3. Résidus vs Valeurs prédites
      fig, ax = plt.subplots(figsize=(10, 6))  
      ax.scatter(y_pred, residuals, alpha=0.5)
      ax.axhline(y=0, color='r', linestyle='--')
      ax.set_xlabel("Valeurs prédites")
      ax.set_ylabel("Résidus")
      ax.set_title("Résidus vs Valeurs prédites_niv1")
      fig.patch.set_visible(False)
      ax.patch.set_visible(False)
      ax.grid(True, linestyle='--', color='gray', alpha=0.7)
      st.pyplot(fig)

      # Homoscédasticité
      gq_result = het_goldfeldquandt(residuals, X)
      st.write(f"Test de Goldfeld-Quandt : F-stat = {gq_result[0]:.4f}, p-value = {gq_result[1]:.4f}\n")

      # Autocorrélation
      dw_stat = durbin_watson(residuals)
      st.write(f"Statistique de Durbin-Watson : {dw_stat:.4f}\n\n")

   except Exception as e:
      print(f"Erreur lors de l'analyse du modèle : {str(e)}")
      raise
        
           

            


   