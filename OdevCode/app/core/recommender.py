import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from collections import Counter  # <-- sayaç için

# Verileri yükle
ratings = pd.read_csv("ratings.csv")
movies = pd.read_csv("movies.csv")

if 'url' not in movies.columns:
    movies['url'] = (
        "https://via.placeholder.com/150x220.png?text="
        + movies['title'].str.replace(' ', '+')
    )

all_users = ratings['userId'].unique()

recommended_movies_counter = Counter()

def create_matrix(df):
    users = df['userId'].unique()
    movies_ = df['movieId'].unique()

    user_mapper = {uid: i for i, uid in enumerate(users)}
    movie_mapper = {mid: i for i, mid in enumerate(movies_)}
    user_inv_mapper = {i: uid for i, uid in enumerate(users)}
    movie_inv_mapper = {i: mid for i, mid in enumerate(movies_)}

    rows = [movie_mapper[mid] for mid in df['movieId']]
    cols = [user_mapper[uid] for uid in df['userId']]

    X = csr_matrix(
        (df['rating'], (rows, cols)),
        shape=(len(movies_), len(users))
    )

    return X, movie_mapper, movie_inv_mapper

X, movie_mapper, movie_inv_mapper = create_matrix(ratings)


def find_similar_movies(movie_id, k=10):
    movie_ind = movie_mapper[movie_id]
    movie_vec = X[movie_ind]

    knn = NearestNeighbors(
        n_neighbors=k + 1,
        metric="cosine",
        algorithm="brute"
    )
    knn.fit(X)

    neighbour_idx = knn.kneighbors(
        movie_vec.reshape(1, -1),
        return_distance=False
    )[0]

    return [
        movie_inv_mapper[i]
        for i in neighbour_idx
        if i != movie_ind
    ][:k]

def recommend_for_user(user_id, k=10):
    df_user = ratings[ratings['userId'] == user_id]
    if df_user.empty:
        return []

    top_movie_id = df_user.loc[df_user['rating'].idxmax(), 'movieId']
    similar_ids = find_similar_movies(top_movie_id, k)

    recommended_movies = movies[movies['movieId'].isin(similar_ids)][['title', 'url']].to_dict(orient='records')

    for movie in recommended_movies:
        movies.loc[movies['title'] == movie['title'], 'counter'] += 1

    movies.to_csv("movies.csv", index=False)

    return recommended_movies
