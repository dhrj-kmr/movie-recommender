import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    try:
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=e3a3c01ed6312da1d32ea77a8480e057&language=en-US'.format(movie_id))
        data = response.json()

        if response.status_code == 200 and 'poster_path' in data:
            return 'http://image.tmdb.org/t/p/w500/' + data['poster_path']
        else:
            return 'https://via.placeholder.com/500'  # Placeholder image if no poster found
    except requests.exceptions.RequestException as e:
        # Handle other network errors
        st.error(f"Error fetching poster: {e}")
        return 'https://via.placeholder.com/500'  # Return a placeholder image in case of error

    st.text('https://api.themoviedb.org/3/movie/{}?api_key=e3a3c01ed6312da1d32ea77a8480e057&language=en-US')
    return 'http://image.tmdb.org/t/p/w500/' + data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity_matrix[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies = pickle.load(open('movies.pkl','rb'))
movies_list = movies['title'].values
similarity_matrix = pickle.load(open('similarity_matrix.pkl','rb'))

st.title('Movie Recommender System')


selected_movie_title = st.selectbox(
    "How would you like to be contacted?",
    (movies_list)
)
if st.button("Recommend"):
    names, posters = recommend(selected_movie_title)

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




