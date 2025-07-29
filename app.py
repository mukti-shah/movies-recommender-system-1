import streamlit as st
import pickle
import pandas as pd
import requests

# 8265bd1679663a7ea12ac168da84d2e8
# https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    response = requests.get(f'http://www.omdbapi.com/?apikey=5c04493e&t={movie_id}')
    data = response.json()
    return data['Poster']

def recomend(movie_name):
    movie_ind = movies[movies['title']== movie_name].index[0]
    # movie_name_fetch = movies[movies['title']== movie_name].index[1]
    distances = similarity[movie_ind]
    movies_list = sorted(enumerate(distances),reverse=True, key= lambda x: x[1])[1:6]

    recomended_movies = []
    recomended_movies_posters = []
    for i in movies_list:
        movie_id = i[0]
        recomended_movies.append(movies.iloc[i[0]].title)
        recomended_movies_posters.append(fetch_poster(movies.iloc[i[0]].title))

    return recomended_movies, recomended_movies_posters

st.title("Movie Recommendation System")

selected_movie_name = st.selectbox(
    "Select a movie:",
    movies['title'].values)

if st.button('Recommend'):
    recommended_movies, recommended_movies_posters = recomend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movies[0])
        st.image(recommended_movies_posters[0])
    with col2:
        st.text(recommended_movies[1])
        st.image(recommended_movies_posters[1])
    with col3:
        st.text(recommended_movies[2])
        st.image(recommended_movies_posters[2])
    with col4:
        st.text(recommended_movies[3])
        st.image(recommended_movies_posters[3])
    with col5:
        st.text(recommended_movies[4])
        st.image(recommended_movies_posters[4])

    # st.write("Recommended Movies:")
    # for movie in recommended_movies:
    #     st.write(movie)
    # st.write("Posters:")
    # for poster in recommended_movies_posters:
    #     st.image(poster)
else:
    st.write("Select a movie to get recommendations.")
    st.write("This app recommends movies based on your selection.")
    st.write("Enjoy your movie time!")