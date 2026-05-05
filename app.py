import streamlit as st
import pickle
import requests
import random

st.set_page_config(page_title="Movie Recommender", layout="wide")

movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

movies["title_lower"] = movies["title"].str.lower()

API_KEY = "b7f0fe7d1cc03a07a6bb95248bc105f8"

if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []

st.markdown("""
<style>
header {visibility:hidden;}
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

.block-container {
    padding-top:1rem;
}

.stApp {
    background:#0b0f19;
    color:white;
}

.main-title{
text-align:center;
font-size:65px;
font-weight:bold;
color:#e50914;
}

.sub-title{
text-align:center;
font-size:22px;
color:#ddd;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def fetch_poster(title):
    try:
        response = requests.get(
            "https://api.themoviedb.org/3/search/movie",
            params={"api_key": API_KEY, "query": title},
            timeout=10
        )

        data = response.json()

        if data.get("results"):
            poster = data["results"][0].get("poster_path")

            if poster:
                return f"https://image.tmdb.org/t/p/w500{poster}"

    except:
        pass

    return "https://via.placeholder.com/300x450?text=No+Poster"


def recommend(movie):
    idx = movies[movies["title_lower"] == movie.lower()].index[0]
    distances = similarity[idx]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    result = []

    for i in movie_list:
        title = movies.iloc[i[0]].title
        result.append((title, fetch_poster(title)))

    return result


page = st.sidebar.radio(
    "Navigation",
    ["Home", "Recommend", "Explore", "Favorites"]
)

if page == "Home":
    st.markdown('<p class="main-title">🎬 Movie Recommender</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Your AI Movie Partner</p>', unsafe_allow_html=True)

    st.image(
        "https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c",
        use_container_width=True
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Movies", len(movies))
    c2.metric("Favorites", len(st.session_state.favorites))
    c3.metric("Recommendations", "Unlimited")

elif page == "Recommend":

    st.title("🎯 Find Similar Movies")

    selected = st.selectbox("Choose a movie", movies["title"])

    if st.button("Recommend"):
        st.session_state.recommendations = recommend(selected)

    if st.session_state.recommendations:

        cols = st.columns(5)

        for i, (title, poster) in enumerate(st.session_state.recommendations):
            with cols[i]:
                st.image(poster)
                st.write(title)

                if title not in st.session_state.favorites:
                    if st.button("❤️ Add", key=i):
                        st.session_state.favorites.append(title)
                        st.rerun()
                else:
                    st.success("Added")

elif page == "Explore":
    st.title("🔍 Search Movies")

    search = st.text_input("Search")

    if search:
        result = movies[movies["title"].str.contains(search, case=False)]
        st.dataframe(result[["title"]])

elif page == "Favorites":
    st.title("❤️ Your Watchlist")

    if not st.session_state.favorites:
        st.warning("No favorites yet")
    else:
        cols = st.columns(3)

        for i, movie in enumerate(st.session_state.favorites):
            with cols[i % 3]:
                st.image(fetch_poster(movie))
                st.write(movie)
