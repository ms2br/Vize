import pandas as pd

def load_data():
    ratings = pd.read_csv("https://s3-us-west-2.amazonaws.com/recommender-tutorial/ratings.csv")
    movies = pd.read_csv("https://s3-us-west-2.amazonaws.com/recommender-tutorial/movies.csv")
    return ratings, movies

def calculate_statistics(ratings):
    n_ratings = len(ratings)
    n_movies = len(ratings['movieId'].unique())
    n_users = len(ratings['userId'].unique())
    return n_ratings, n_movies, n_users

def get_movie_stats(ratings):
    mean_rating = ratings.groupby('movieId')[['rating']].mean()
    lowest_rated = mean_rating['rating'].idxmin()
    highest_rated = mean_rating['rating'].idxmax()
    return mean_rating, lowest_rated, highest_rated
