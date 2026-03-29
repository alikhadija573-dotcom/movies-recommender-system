import streamlit as st
import pickle
import pandas as pd
import requests
import os


# similarity.pkl download
if not os.path.exists("similarity.pkl"):
    url = "https://drive.google.com/uc?export=download&id=1DfC-t_YOUOC9nTJLEEhVtddHzJyKw4_u"
    r = requests.get(url)
    with open("similarity.pkl", "wb") as f:
        f.write(r.content)
    print("Downloaded similarity.pkl")

# movies_dict.pkl download
if not os.path.exists("movies_dict.pkl"):
    url = "https://drive.google.com/uc?export=download&id=<YOUR_MOVIES_DICT_FILE_ID>"
    r = requests.get(url)
    with open("movies_dict.pkl", "wb") as f:
        f.write(r.content)
    print("Downloaded movies_dict.pkl")
# Function to fetch poster using TMDB API
def fetch(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')  # safe get
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"  # fallback

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        # fallback if poster not found
        return "https://via.placeholder.com/500x750?text=No+Image"

# -------------------------------------
# Function to recommend similar movies
# -------------------------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recomended_movies = []
    recomended_movies_posters = []  # ✅ initialize before using

    for i in movies_list:
        movie_id = i[0]  
        recomended_movies.append(movies.iloc[i[0]]['title'])
        recomended_movies_posters.append(fetch(movie_id))
    
    return recomended_movies, recomended_movies_posters
# Load data
movies_dict = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

# Streamlit UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)


# ✅ fixed button
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])