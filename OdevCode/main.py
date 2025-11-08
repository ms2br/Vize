# Importing necessary functions from custom modules
from data_processing import load_data, calculate_statistics, get_movie_stats
from matrix_utils import create_matrix
from similarity import find_similar_movies
from recommendation import recommend_movies_for_user

ratings, movies = load_data()
n_ratings, n_movies, n_users = calculate_statistics(ratings)
print(f"Number of ratings: {n_ratings}")
print(f"Number of movies: {n_movies}")
print(f"Number of users: {n_users}")
mean_rating, lowest_rated, highest_rated = get_movie_stats(ratings)
print(f"Lowest rated movie: {movies.loc[movies['movieId'] == lowest_rated]['title'].values[0]}")
print(f"Highest rated movie: {movies.loc[movies['movieId'] == highest_rated]['title'].values[0]}")
X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper = create_matrix(ratings)
movie_id = 3  # Example movie ID
print("\nFinding similar movies...")
similar_ids = find_similar_movies(movie_id, X, k=10, movie_mapper=movie_mapper, movie_inv_mapper=movie_inv_mapper)
movie_titles = dict(zip(movies['movieId'], movies['title']))
movie_title = movie_titles[movie_id]
print(f"\nSince you watched '{movie_title}', you might also like:")
for i in similar_ids:
  print(movie_titles.get(i, "Movie not found"))
user_id = 1  # Example user ID
print("\nRecommending movies for user...")
recommend_movies_for_user(user_id, ratings, movies, X, user_mapper, movie_mapper, movie_inv_mapper, k=10)
