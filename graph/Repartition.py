import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

from ..Dashborad_Valeurs_Foncieres import get_data 


def repartition():

    df = get_data
    
    st.subheader(":red[Répartition du nombre des ventes par régions :]")

    total_ventes_reg = df.groupby("nom_region").size()

    fig_region = px.pie(total_ventes_reg, total_ventes_reg.index, total_ventes_reg.values,hole=0.35)

    plt.gcf().set_facecolor('none')

    
    st.plotly_chart(fig_region)