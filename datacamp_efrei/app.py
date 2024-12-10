import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from nltk.corpus import stopwords
import nltk

# Télécharger les stopwords
nltk.download('stopwords')

# Fonction pour nettoyer le texte
def nettoyer_texte(texte):
    texte = str(texte).lower()  # Mettre en minuscule
    texte = re.sub(r'\s+', ' ', texte)  # Supprimer les espaces excessifs
    texte = re.sub(r'[^\w\s]', '', texte)  # Supprimer les caractères non alphanumériques
    return texte

# Titre de l'application
st.title("Nuage de mots - Analyse des Avis Clients")

# Télécharger un fichier CSV
uploaded_file = st.file_uploader("Téléchargez votre fichier CSV", type=["csv"])

if uploaded_file is not None:
    # Charger les données
    df = pd.read_csv(uploaded_file)

    # Afficher les premières lignes du fichier
    st.subheader("Aperçu des données")
    st.dataframe(df.head())

    # Nettoyer la colonne des avis (supposons que la colonne s'appelle 'Contenu de l\'avis')
    if 'Contenu de l\'avis' in df.columns:
        df['Contenu de l\'avis'] = df['Contenu de l\'avis'].apply(nettoyer_texte)

        # Fusionner tous les avis
        text = ' '.join(df['Contenu de l\'avis'].dropna())

        # Exclure les mots vides
        stop_words = set(stopwords.words('english'))
        filtered_text = ' '.join([word for word in text.split() if word not in stop_words])

        # Générer le nuage de mots
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(filtered_text)

        # Afficher le nuage de mots
        st.subheader("Nuage de mots")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

    else:
        st.error("La colonne 'Contenu de l'avis' n'existe pas dans le fichier.")
else:
    st.info("Veuillez télécharger un fichier CSV pour commencer.")
