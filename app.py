import streamlit as st
import pickle
import requests
import random

# -----------------------------------
# Page setup
# -----------------------------------
st.set_page_config(
    page_title="CineMatch AI",
    layout="wide"
)

# -----------------------------------
# Load data
# -----------------------------------
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

movies["title"] = movies["title"].str.strip()
movies["title_lower"] = movies["title"].str.lower()

# -----------------------------------
# TMDB API Key
# -----------------------------------
API_KEY = "b7f0fe7d1cc03a07a6bb95248bc105f8"

# -----------------------------------
# Session state
# -----------------------------------
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# -----------------------------------
# Custom styling
# -----------------------------------
st.markdown("""
<style>
.main-title {
    text-align:center;
    font-size:50px;
    font-weight:bold;
    color:#ff4b4b;
}

.sub-title {
    text-align:center;
    color:gray;
    font-size:18px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# Fetch movie poster
# -----------------------------------
@st.cache_data
def fetch_poster(movie_title):
    try:
        # Remove year if present
        cleaned_title = movie_title.split("(")[0].strip()

        response = requests.get(
            "https://api.themoviedb.org/3/search/movie",
            params={
                "api_key": API_KEY,
                "query": cleaned_title
            },
            timeout=10
        )

        data = response.json()

        if data.get("results"):
            for movie in data["results"]:
                poster_path = movie.get("poster_path")

                if poster_path:
                    return f"https://image.tmdb.org/t/p/w500{poster_path}"

        return "https://via.placeholder.com/300x450?text=No+Poster"

    except:
        return "https://via.placeholder.com/300x450?text=Error"

# -----------------------------------
# Recommendation function
# -----------------------------------
def recommend(movie_name):
    movie_name = movie_name.lower()

    if movie_name not in movies["title_lower"].values:
        return []

    index = movies[movies["title_lower"] == movie_name].index[0]
    distances = similarity[index]

    recommended_movies = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    results = []

    for movie in recommended_movies:
        title = movies.iloc[movie[0]].title
        poster = fetch_poster(title)
        results.append((title, poster))

    return results

# -----------------------------------
# Sidebar
# -----------------------------------
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Recommend", "Explore", "Favorites"]
)

# -----------------------------------
# Home Page
# -----------------------------------
if page == "Home":

    st.markdown('<p class="main-title">🎬 CineMatch AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Find your next favorite movie</p>', unsafe_allow_html=True)

    st.image(
        "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba",
        use_container_width=True
    )

    st.markdown("## Features")
    st.write("🎯 Smart Recommendations")
    st.write("🖼 Live Posters")
    st.write("❤️ Save Favorites")
    st.write("🎲 Random Movie Generator")

# -----------------------------------
# Recommend Page
# -----------------------------------
elif page == "Recommend":

    st.title("🎯 Movie Recommendations")

    selected_movie = st.selectbox(
        "Choose a movie",
        movies["title"].values
    )

    if st.button("Recommend"):

        recommendations = recommend(selected_movie)

        cols = st.columns(5)

        for i, (title, poster) in enumerate(recommendations):

            with cols[i]:
                st.image(poster)
                st.write(f"**{title}**")

                if title in st.session_state.favorites:
                    if st.button("❤️ Remove", key=f"remove{i}"):
                        st.session_state.favorites.remove(title)
                        st.rerun()
                else:
                    if st.button("🤍 Add", key=f"add{i}"):
                        st.session_state.favorites.append(title)
                        st.rerun()

    if st.button("🎲 Surprise Me"):
        random_movie = random.choice(movies["title"].values)
        st.success(f"Try watching: {random_movie}")

# -----------------------------------
# Explore Page
# -----------------------------------
elif page == "Explore":

    st.title("🔍 Explore Movies")

    search = st.text_input("Search movie")

    if search:
        result = movies[
            movies["title"].str.contains(search, case=False, na=False)
        ]
        st.dataframe(result[["title"]].head(20))
    else:
        st.dataframe(movies[["title"]].head(20))

# -----------------------------------
# Favorites Page
# -----------------------------------
elif page == "Favorites":

    st.title("❤️ Favorite Movies")

    if not st.session_state.favorites:
        st.warning("No favorite movies yet")
    else:
        for movie in st.session_state.favorites:
            st.write(f"🎬 {movie}")

        if st.button("Clear All"):
            st.session_state.favorites = []
            st.rerun()