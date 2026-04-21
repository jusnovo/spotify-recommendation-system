from sklearn.metrics.pairwise import cosine_similarity
from src.clustering import spotify, spotify_scaled

spotify.reset_index(drop=True, inplace=True)
spotify_scaled.reset_index(drop=True, inplace=True)

def recommend_similar(song_name, n_rec=5):

    song_idx = spotify[spotify['name'] == song_name].index

    if len(song_idx) == 0:
        return "Song not found"

    song_idx = int(song_idx[0])

    song_vector = spotify_scaled.iloc[[song_idx]]

    similarities = cosine_similarity(song_vector, spotify_scaled)[0]

    recommendations = spotify.copy()
    recommendations['similarity'] = similarities

    cluster = spotify.iloc[song_idx]['cluster']
    recommendations = recommendations[recommendations['cluster'] == cluster]
    recommendations = recommendations[recommendations.index != song_idx]

    recommendations = recommendations.sort_values(by='similarity', ascending=False)

    return recommendations[['name', 'artists', 'cluster_name', 'popularity', 'similarity']].head(n_rec)