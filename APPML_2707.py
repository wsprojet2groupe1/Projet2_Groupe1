import streamlit as st
import pickle
import pandas as pd

# Configuration de la page (doit être la première commande Streamlit)
# la barre latérale est affichée en totalité dès que l'application est ouverte
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Mise en cache du chargement des données pour éviter de les recharger à chaque exécution du script
# '''
#  @st.cache_resource permet de stocker en cache les résultats de la fonction load_data() 
#  pour améliorer les performances de l'application. Ainsi, les données chargées depuis 
#  les fichiers movies_list3.pkl et similarity.pkl ne sont lues qu'une seule fois, 
#  et sont réutilisées pour les appels suivants sans avoir à être rechargées depuis les fichiers.
#  movies = pickle.load(open('movies_list3.pkl', 'rb')) : Cette ligne ouvre le fichier movies_list3.pkl 
#  en mode binaire de lecture ('rb'), le décharge (ou désérialise) en utilisant pickle, 
#  et stocke le résultat dans la variable movies.
#  movies contient les données films
#  similarity contient la matrice qui mesure à quel point les films sont similaires les uns aux autres
# movies['primaryTitle'].values extrait tous les titres des films du DataFrame movies et les stocke dans movies_list.
# '''
@st.cache_resource
def load_data():
    movies = pickle.load(open('movies_list3.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

movies, similarity = load_data()
movies_list = movies['primaryTitle'].values

# '''
# movies[movies['primaryTitle'] == title] : Filtre le DataFrame pour obtenir la 
# ligne où le titre du film (primaryTitle) correspond à title.
# .index[0] : Obtient l'index de cette ligne. Il suppose qu'il n'y a qu'un seul film 
# avec ce titre dans le DataFrame, et il prend le premier index.

# cosine_sim[idx] : Extrait les scores de similarité pour le film avec l'index idx 
# depuis la matrice de similarité. Cela donne une liste de similarités entre ce film 
# et tous les autres films.

# enumerate(sim_scores) : Crée une liste de tuples (index, score) pour chaque score dans sim_scores.
# sorted(..., key=lambda x: x[1], reverse=True) : Trie ces tuples en fonction des scores 
# (de plus élevé à plus bas). Le key=lambda x: x[1] indique que le tri doit être effectué 
# en utilisant la valeur du score (qui est le deuxième élément du tuple).
# sim_scores = [score for score in sim_scores if score[0] != idx] : Cette ligne filtre les scores pour exclure le film lui-même. 

# recommendations['poster_path'].apply(...) : Pour chaque chemin d'affiche (poster_path), 
# construit l'URL complète en ajoutant le base_url. Si le chemin est vide, utilise 
# une URL par défaut pour une image de remplacement.
# '''

def recommend_movies(title, movies, cosine_sim):
    idx = movies[movies['primaryTitle'] == title].index[0]
    sim_scores = cosine_sim[idx]
    sim_scores = sorted(enumerate(sim_scores), key=lambda x: x[1], reverse=True)
    sim_scores = [score for score in sim_scores if score[0] != idx]
    movie_indices = [i[0] for i in sim_scores[:5]]

    recommendations = movies.iloc[movie_indices]
    base_url = "https://image.tmdb.org/t/p/original/"
    recommendations['poster_urls'] = recommendations['poster_path'].apply(lambda path: base_url + path.lstrip('/') if path else "https://via.placeholder.com/300x450")

    return recommendations

# CSS personnalisé
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #e0e0e0;
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        text-align: center;
    }
    .container {
        width: 100%;
        max-width: 100vw;
        padding: 0 20px;
    }
    .custom-title {
        font-family: 'Impact', sans-serif;
        color: #FFD700;
        font-size: 60px;
        margin: 40px 0 20px 0;
        text-transform: uppercase;
    }
    .custom-subtitle {
        font-family: 'Arial', sans-serif;
        color: #f0f0f0;
        font-size: 30px;
        margin-bottom: 40px;
    }
    .custom-subtitle span {
        font-size: 32px;
    }
    .custom-selectbox {
        display: flex;
        justify-content: center;
        margin-bottom: 40px;
    }
    .custom-selectbox select {
        font-size: 22px;
        padding: 12px;
        border-radius: 8px;
        border: 2px solid #FFD700;
        background-color: #333;
        color: #FFD700;
        transition: all 0.3s ease;
    }
    .custom-selectbox select:hover {
        background-color: #444;
    }
    .recommendation-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
        width: 100%;
    }
    .recommendation {
        display: flex;
        align-items: flex-start;
        border: 2px solid #FFD700;
        border-radius: 10px;
        background-color: #333;
        padding: 20px;
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .recommendation:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
    }
    .recommendation img {
        border-radius: 10px;
        width: 250px;
        height: auto;
        margin-right: 20px;
    }
    .recommendation .info {
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: left;
    }
    .recommendation h3 {
        color: #FFD700;
        font-size: 24px;
        margin: 0;
    }
    .recommendation .rating,
    .recommendation .year,
    .recommendation .actors,
    .recommendation .overview-text {
        color: #f0f0f0;
        font-size: 20px;
        margin: 5px 0;
    }
    .recommendation .year-title,
    .recommendation .actors-title,
    .recommendation .overview-title {
        color: #FFD700;
        font-size: 24px;
        margin: 10px 0 5px;
    }
    .stButton button {
        background-color: #6e00c7;
        color: #ffffff;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #b10000;
    }
    </style>
    <div class="container">
        <div class="custom-title">HELLO CINÉ</div>
        <div class="custom-subtitle">Find your next favorite Movie, and Enjoy! <span>🍿</span></div>
    </div>
    """, unsafe_allow_html=True)

# Sélection des films
st.markdown('<div class="custom-selectbox">', unsafe_allow_html=True)
selectvalues = st.multiselect("Select Movies", movies_list, label_visibility='collapsed')
st.markdown('</div>', unsafe_allow_html=True)

# Bouton de recommandation
if st.button("Show Recommend", key="recommend_button", help="Click to get recommendations", use_container_width=True):
    if selectvalues:
        st.markdown('<div class="recommendation-container">', unsafe_allow_html=True)
        for selectvalue in selectvalues:
            st.markdown(f"<h2>Recommendations for {selectvalue}:</h2>", unsafe_allow_html=True)
            recommendations = recommend_movies(selectvalue, movies, similarity)
            if not recommendations.empty:
                for _, row in recommendations.iterrows():
                    imdb_url = f"https://www.imdb.com/title/{row['tconst']}/"
                    st.markdown(f"""
                        <div class="recommendation">
                            <img src="{row['poster_urls']}" alt="{row['primaryTitle']}">
                            <div class="info">
                                <a href="{imdb_url}" target="_blank"><h3>{row['primaryTitle']}</h3></a>
                                <div class="rating">⭐ {row['averageRating']}</div>
                                <div class="year-title">Year</div>
                                <div class="year">{row['startYear']}</div>
                                <div class="actors-title">Actors</div>
                                <div class="actors">{row['primaryName']}</div>
                                <div class="overview-title">Overview</div>
                                <div class="overview-text">{row['overview']}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.markdown("<p>No recommendations available.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("<p>Please select at least one movie.</p>", unsafe_allow_html=True)
