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
df_frequentation = pd.read_csv('frequentation-gares-netoyé.csv')
df_frequentation.set_index('gare', inplace=True)

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
st.subheader("Tableau des données")
selected_anee = st.selectbox('Sélectionnez une année', dico_annee_df.keys())
st.write("Informations objets trouvés pour l'année :", selected_anee)
# Créer un tableau objet trouvé/semaine
if selected_anee != 'toutes': 
    st.write("Semaine/objet trouvés:")
    dico_annee_df[selected_anee]['nb_objet'] = dico_annee_df[selected_anee]['fields.date']
    st.write(dico_annee_df[selected_anee]['nb_objet'].value_counts().sort_index()) 
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
    
    
####################{PARTIE B : CARTE DE PARIS}#############################################################################################################
import folium
from streamlit_folium import folium_static

st.subheader("Carte gares Paris: objet trouvé/fréquentation")

list_objets_type = ['tous', 'Porte-monnaie / portefeuille, argent, titres',
       'Bagagerie: sacs, valises, cartables', 'Vêtements, chaussures',
       "Pièces d'identités et papiers personnels",
       'Clés, porte-clés, badge magnétique',
       'Appareils électroniques, informatiques, appareils photo',
       'Vélos, trottinettes, accessoires 2 roues', 'Optique',
       'Livres, articles de papéterie', 'Divers', 'Bijoux, montres',
       "Articles d'enfants, de puériculture",
       'Articles de sport, loisirs, camping', 'Instruments de musique',
       'Articles médicaux', 'Parapluies']
selected_objet_type = st.selectbox('Sélectionnez un type ', list_objets_type)

dico_year = {
    2019 : ['frequentation_2019', df1_2019],
    2020 : ['frequentation_2020', df1_2020],
    2021 : ['frequentation_2021', df1_2021]
    }
selected_annee = st.selectbox('Sélectionnez une année', dico_year.keys())

m = folium.Map(location=[ 48.8566, 2.3522], zoom_start=12)

# Ajout des marqueurs pour chaque ville
if selected_objet_type == 'tous':
    for city in df_frequentation.index:
        frequentation = df_frequentation.loc[city][dico_year[selected_annee][0]]
        objets_trouvés = dico_year[selected_annee][1].groupby(['fields.gc_obo_gare_origine_r_name', 'fields.gc_obo_type_c']).count().loc[city].sum()[0]
        coord = df_frequentation.loc[city][['latitude','longitude']].to_list()
        popup = f"{city} <br> frequentation en {selected_annee}: {frequentation} <br> nb d'objets trouvés en {selected_annee} : {objets_trouvés}"
        folium.Marker(location=coord, popup=folium.Popup(popup, max_width=500)).add_to(m)
else:
    for city in df_frequentation.index:
        frequentation = df_frequentation.loc[city][dico_year[selected_annee][0]]
        objets_trouvés = dico_year[selected_annee][1].groupby(['fields.gc_obo_gare_origine_r_name', 'fields.gc_obo_type_c']).count().loc[city].loc[selected_objet_type][0]
        coord = df_frequentation.loc[city][['latitude','longitude']].to_list()
        popup = f"{city} <br> frequentation en {selected_annee}: {frequentation} <br> nb d'objets trouvés en {selected_annee} : {objets_trouvés}"
        folium.Marker(location=coord, popup=folium.Popup(popup, max_width=500)).add_to(m) 
# Affichage de la carte avec Streamlit
folium_static(m)
#################{PARTIE C_1 : Scatterplot temerature/objet perdu}########################################################################################################################
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
#################{PARTIE C_2 : MEDIAN / SAISON}#####################################################################################################
st.subheader("Médiane du nombre d’objets trouvés/saison")
df1 = df1.rename(columns={'fields.date': 'date', 'fields.gc_obo_gare_origine_r_name': 'gare', 'fields.gc_obo_type_c': 'type_objet'})
# retirer les colonnes inutiles
df1 = df1.drop('type_objet', axis=1)
# Conversion de la colonne 'fields.date' en type 'datetime'
df1['date'] = pd.to_datetime(df1['date'])
# Filtrage des données entre les deux dates spécifiées sans modifier le DataFrame d'origine
dico_saison = {
    'hiver 2019'     : ['2019-01-01', '2019-02-28', 'df_hiver_19'],
    'printemps 2019' : ['2019-03-01', '2019-05-31', 'df_printemps_19'],
    'été 2019'       : ['2019-06-01', '2019-08-31', 'df_été_19'],
    'automne 2019'   : ['2019-09-01', '2019-11-30', 'df_automne_19'],
    'hiver 2020'     : ['2019-12-01', '2020-02-29', 'df_hiver_20'],
    'printemps 2020' : ['2020-03-01', '2020-05-31', 'df_printemps_20'],
    'été 2020'       : ['2020-06-01', '2020-08-31', 'df_été_20'],
    'automne 2020'   : ['2020-09-01', '2020-11-30', 'df_automne_20'],
    'hiver 2021'     : ['2020-12-01', '2021-02-28', 'df_hiver_21'],
    'printemps 2021' : ['2021-03-01', '2021-05-31', 'df_printemps_21'],
    'été 2021'       : ['2021-06-01', '2021-08-31', 'df_été_21'],
    'automne 2021'   : ['2021-09-01', '2021-11-30', 'df_automne_21'],
    'hiver 2022'     : ['2021-12-01', '2022-02-28', 'df_hiver_22'],
    'printemps 2022' : ['2022-03-01', '2022-05-31', 'df_printemps_22'],
    'été 2022'       : ['2022-06-01', '2022-08-31', 'df_été_22'],
    'automne 2022'   : ['2022-09-01', '2022-11-30', 'df_automne_22'],
    'hiver 2023'     : ['2022-12-01', '2022-12-31',  'df_hiver_23']             
}
selected_saison = st.selectbox('Sélectionnez une saison', dico_saison.keys())
start_date = pd.to_datetime(dico_saison[selected_saison][0])
end_date = pd.to_datetime(dico_saison[selected_saison][1])
dico_saison[selected_saison][2] = df1[(df1['date'] >= start_date) & (df1['date'] <= end_date)]
st.write(f"la médiane du nombre d’objets trouvés en fonction de la saison {selected_saison} est {dico_saison[selected_saison][2].groupby('date')['gare'].count().median()}")
######################################################################################
st.subheader("Histogramme nb objet trouvé/saison")
# je cree une colonne pour de saisons
# def f(x):
#     for cle, valeur in dico_saison.items():
#         start_date = pd.to_datetime(valeur[0])
#         end_date = pd.to_datetime(valeur[1])
#         if start_date <= x <= end_date:
#             return cle
#     return None

# df1['saison'] = df1['date'].apply(f)
df1 = pd.read_csv('objets-trouves-saison.csv')
import plotly.express as px
# Créer l'application Streamlit
selected_annneee = st.selectbox('Sélectionnez une saison', [2019 , 2020, 2021 , 2022])
df1['date'] = pd.to_datetime(df1['date'])
df1 = df1[((df1['date'].dt.year == selected_annee-1) & (df1['date'].dt.month == 12)) | ((df1['date'].dt.year == selected_annneee) & (df1['date'].dt.month != 12))]
fig = px.box(x=df1.groupby(['saison','date']).count().reset_index()['saison'], y= df1.groupby(['saison','date']).count().reset_index()['gare'], points='all')
st.plotly_chart(fig)
# ((df1['date'].dt.month == 12) | (df1['date'].dt.year == selected_annneee-1))

