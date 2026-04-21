import pandas as pd
from sklearn.cluster import KMeans

filepath = "data/ML_spotify_data.csv"
spotify = pd.read_csv(filepath)

features = ['danceability', 'energy', 'valence', 'loudness', 'tempo']
spotify_selected = spotify[features]

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler().set_output(transform="pandas")
spotify_scaled = scaler.fit_transform(spotify_selected)

kmeans = KMeans( n_clusters = 5, random_state = 15)

spotify['cluster'] = kmeans.fit_predict(spotify_scaled)
features = ['danceability', 'energy', 'valence', 'loudness', 'tempo']
cluster_summary = spotify.groupby('cluster')[features].mean()

cluster_names = {
    0: "Party",
    1: "Workout",
    2: "Chill",
    3: "Balanced",
    4: "Energetic"
}

spotify['cluster_name'] = spotify['cluster'].map(cluster_names)
spotify.to_csv("data/ML_spotify_data.csv", index=False)