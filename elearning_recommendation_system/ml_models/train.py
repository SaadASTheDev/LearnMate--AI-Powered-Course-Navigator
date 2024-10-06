# File: ml_models/train.py

import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import pickle

# Load data from CSV
data_path = 'elearning_recommendation_system/data/user_course_interactions.csv'  # Updated CSV filename for Netflix data
df = pd.read_csv(data_path)

# Ensure that the necessary columns are present
# Assuming the columns are: user_id, movie_id, rating
# Rating will be used as the interaction value in this case

if not set(['user_id', 'movie_id', 'rating']).issubset(df.columns):
    raise ValueError("CSV file must contain 'user_id', 'movie_id', and 'rating' columns.")

# Prepare the data for Surprise
reader = Reader(rating_scale=(1, 5))  # Adjust rating scale as per your data (e.g., Netflix's ratings are from 1 to 5)
data = Dataset.load_from_df(df[['user_id', 'movie_id', 'rating']], reader)

# Split the data into training and testing sets
trainset, testset = train_test_split(data, test_size=0.2)

# Train a collaborative filtering model using SVD
model = SVD()
model.fit(trainset)

# Save the trained model
model_file = 'ml_models/movie_recommender_model.pkl'
with open(model_file, 'wb') as f:
    pickle.dump(model, f)

print("Model training complete and saved to movie_recommender_model.pkl")