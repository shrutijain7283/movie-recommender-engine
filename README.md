# 🎬 Movie Recommender Engine

An intelligent Movie Recommendation System built using Machine Learning and Streamlit that suggests similar movies based on content similarity. The application provides an interactive user experience with real-time movie posters, search functionality, and personalized favorites management.

## 🚀 Features

- Personalized movie recommendations using content-based filtering
- Real-time movie poster retrieval through TMDB API
- Search movies from the dataset
- Add and manage favorite movies
- Interactive and user-friendly Streamlit interface
- Fast recommendation generation using precomputed similarity scores

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- Scikit-learn
- Pickle
- Requests
- TMDB API
- Git & GitHub

## ⚙️ How It Works

1. Movie metadata is preprocessed and transformed into feature vectors.
2. Cosine similarity is calculated between movies.
3. When a user selects a movie, the system identifies the most similar movies.
4. Recommended movies are displayed along with their posters fetched from TMDB API.

## 📂 Project Structure

```text
movie-recommender-engine/
│
├── app.py
├── movies.pkl
├── similarity.pkl
├── requirements.txt
└── README.md
```

## ▶️ Run Locally

```bash
git clone https://github.com/shrutijain7283/movie-recommender-engine.git

cd movie-recommender-engine

pip install -r requirements.txt

streamlit run app.py
```

## 🎯 Key Highlights

- Implemented Content-Based Recommendation System
- Integrated External APIs for Dynamic Content
- Developed Interactive Web Application using Streamlit
- Applied Machine Learning Similarity Techniques
- Enhanced User Experience with Favorites and Search Features

## 📸 Project Preview

Movie recommendation web application featuring:
- Smart recommendations
- Live movie posters
- Favorites watchlist
- Search functionality
- Modern UI design

## 👩‍💻 Author

**Shruti Jain**

GitHub: https://github.com/shrutijain7283
