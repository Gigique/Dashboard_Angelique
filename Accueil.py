import streamlit as st



def app():
    
    st.title("Accueil")
    st.write("WIP tatata")


    
#customiser le rendu
hide_st_style = """
<style>
#MainMenu {visibility : hidden;}
footer {visibility : hidden;}
header {visibility : hidden;}
<style>"""

st.markdown(hide_st_style, unsafe_allow_html=True)
