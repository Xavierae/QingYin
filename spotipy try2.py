import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Replace with your Spotify API credentials
client_id = 'your_client_id'
client_secret = 'your_client_secret'

# Authenticate with Spotify API
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)


def recommend_tracks_by_genre(genre):
    # Search for tracks based on genre
    recommendations = sp.recommendations(seed_genres=[genre], limit=5)

    recommended_tracks = []
    for track in recommendations['tracks']:
        recommended_tracks.append(track['name'])

    return recommended_tracks


# Example usage
genre = 'pop'  # Replace with the genre you want to recommend tracks for
recommended_tracks = recommend_tracks_by_genre(genre)
if recommended_tracks:
    print(f"Recommended tracks in the '{genre}' genre:")
    for i, track in enumerate(recommended_tracks, 1):
        print(f"{i}. {track}")
