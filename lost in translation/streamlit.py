import requests
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

df1_2019 = pd.read_csv('objets-trouves_2019.csv')

# Créer l'interface Streamlit
st.title("Histogramme avec Streamlit")
st.write("Exemple d'un histogramme avec deux variables")

# Afficher les données X et Y
st.subheader("Données")
st.write("Variable X:")
st.write(df1_2019['fields.date'].unique())
st.write("Variable Y:")
st.write(df1_2019['fields.date'].value_counts())

# # Créer l'histogramme
# fig, ax = plt.subplots()
# ax.hist(df1_2019['fields.date'].unique(), alpha=0.5, label='Variable X')
# ax.hist(df1_2019['fields.date'].value_counts(), alpha=0.5, label='Variable Y')
# ax.legend()
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_title('Histogramme X et Y')
# st.pyplot(fig)
#########################################################################
fig = go.Figure()

# Ajouter l'histogramme à la figure
fig.add_trace(go.Histogram(x=df1_2019['fields.date'], nbinsx=len(df1_2019['fields.date'].unique())))

# Mettre en forme le graphique
fig.update_layout(
    title="Histogramme avec Plotly",
    xaxis_title="Date",
    yaxis_title="Fréquence",
)
# Afficher le graphique avec Streamlit
st.plotly_chart(fig)