import requests
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

df1      = pd.read_csv('objets-trouves.csv')
df1_2019 = pd.read_csv('objets-trouves_2019.csv')
df1_2020 = pd.read_csv('objets-trouves_2020.csv')
df1_2021 = pd.read_csv('objets-trouves_2021.csv')
df1_2022 = pd.read_csv('objets-trouves_2022.csv')

df_temperature_jour=pd.read_csv('temperature_jour.csv')

dico_annee_df = {
    2019 : df1_2019,
    2020 : df1_2020,
    2021 : df1_2021,
    2022 : df1_2022,
    'toutes' : None
    }
###############{PARTIE A : tableau + histogramme objet perdu/semaine}#################################################################
st.title("Objet trouvé à paris")
# Creer un boutton des années
selected_anee = st.selectbox('Sélectionnez une année', dico_annee_df.keys())

# Créer un tableau objet trouvé/semaine
if selected_anee != 'toutes': 
    st.subheader("Tableau des données")
    st.write("Informations objets trouvés pour l'année :", selected_anee)
    st.write("Semaine/objet trouvés:")
    dico_annee_df[selected_anee]['date'] = dico_annee_df[selected_anee]['fields.date']
    st.write(dico_annee_df[selected_anee]['date'].value_counts().sort_index()) 
    #########################################################################
    # Faire un histogramme
    st.subheader("Histogramme")
    st.write("Histogramme objets trouvés pour l'année :", selected_anee)
    fig = go.Figure()

    # Ajouter l'histogramme à la figure
    fig.add_trace(go.Histogram(x=dico_annee_df[selected_anee]['fields.date'], nbinsx=len(dico_annee_df[selected_anee]['fields.date'].unique())))

    # Mettre en forme le graphique
    fig.update_layout(
    title="le nb d'objets trouvés par semaine",
    xaxis_title="Semaine",
    yaxis_title="Objets trouvés",
    )
    # Afficher le graphique avec Streamlit
    st.plotly_chart(fig)
    #########################################################################
    # Faire une carte des gares de paris affichant le nb d'objet trouvés et la frequantation par année dans chaque gare. 
else :
    df1_2019['nb_objet_2019'] = df1_2019['fields.date']
    df1_2020['nb_objet_2020'] = df1_2020['fields.date']
    df1_2021['nb_objet_2021'] = df1_2021['fields.date']
    df1_2022['nb_objet_2022'] = df1_2022['fields.date']
    st.subheader("Tableau des données")
    st.write("Informations objets trouvés pour l'année :", selected_anee)
    df = pd.concat([df1_2019['nb_objet_2019'].value_counts().sort_index(), df1_2020['nb_objet_2020'].value_counts().sort_index(), df1_2021['nb_objet_2021'].value_counts().sort_index(), df1_2022['nb_objet_2022'].value_counts().sort_index()], axis=1)
    st.write(df)
    ########################################################################
    dico_annee_df.pop('toutes')
    st.subheader("Histogramme")
    st.write("Histogramme objets trouvés pour l'année :", selected_anee)
    fig = go.Figure()
    # Ajouter l'histogramme à la figure
    for elt in dico_annee_df.keys():
        fig.add_trace(go.Histogram(x=dico_annee_df[elt]['fields.date'], nbinsx=len(dico_annee_df[elt]['fields.date'].unique()), name = elt))   
    # Mettre en forme le graphique
    fig.update_layout(
    title="le nb d'objets trouvés par semaine",
    xaxis_title="Semaine",
    yaxis_title="Objets trouvés")
    # Afficher le graphique avec Streamlit
    st.plotly_chart(fig)
    
    
################{PARTIE B : Scatterplot temerature/objet perdu}########################################################################################################################
st.subheader("Scatterplot objet perdu/température")
df1_jour = pd.read_csv('objet-perdu-jour.csv')
fig = go.Figure()
# Ajouter les données au scatterplot
fig.add_trace(go.Scatter(
    x=df_temperature_jour['temperature_2m (°C)'],
    y=df1_jour['objet_jour'],
    mode='markers',
    marker=dict(color='blue', size=5),
    name='Scatterplot'
))
# Mettre en forme le graphe
fig.update_layout(
    title='Scatterplot interactif',
    xaxis_title='Temperature moyenne par jour',
    yaxis_title='nb objet trouvé par jour',
)
# Afficher le graphe avec Streamlit
st.plotly_chart(fig)

################ MEME CHOSE AVEC MATPLOTLIB###########################################################################################################################
# st.subheader("Scatterplot objet perdu/température")
# df1_jour = pd.read_csv('objet-perdu-jour.csv')
# # Créer un scatterplot interactif avec Matplotlib
# fig, ax = plt.subplots()
# ax.scatter( df_temperature_jour['temperature_2m (°C)'],df1_jour['objet_jour'], c='blue', s=8)
# ax.set_title('Scatterplot interactif')
# ax.set_xlabel('temperature moyenne par jour')
# ax.set_ylabel('nb objet toruvé par jour ')

# # Afficher le graphe avec Streamlit
# st.pyplot(fig)
#################################################################################################################################
