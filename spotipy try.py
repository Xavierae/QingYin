import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Replace with your Spotify API credentials
client_id = '39f0de13ec6f458594c6bc16b59b07a9'
client_secret = 'a4284b9465314453a6681994cc415d61'

# Authenticate with Spotify API
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)


def get_artist_details(artist_name):
    # Search for artist
    results = sp.search(q='artist:' + artist_name, type='artist', limit=1)

    # Check if any artists were found
    if len(results['artists']['items']) == 0:
        print(f"No artist found with name '{artist_name}'")
        return

    artist = results['artists']['items'][0]

    # Print artist details
    print(f"Artist Name: {artist['name']}")
    print(f"Genres: {artist['genres']}")

    # Get top tracks by the artist
    top_tracks = sp.artist_top_tracks(artist['id'], country='US')  # Replace 'US' with your country code if needed

    print("\nTop Tracks:")
    for i, track in enumerate(top_tracks['tracks'][:3], 1):  # Limit to 3 tracks
        print(f"{i}. {track['name']}")
    print("\n")

    return artist


def recommend_tracks_by_artist(artist):
    # Get related artists
    related_artists = sp.artist_related_artists(artist['id'])

    # Print related artists and their top tracks
    print("Related Artists:")
    for i, related_artist in enumerate(related_artists['artists'][:2], 1):  # Limit to 2 related artists
        print(f"{i}. {related_artist['name']}")
        top_tracks = sp.artist_top_tracks(related_artist['id'],
                                          country='US')  # Replace 'US' with your country code if needed
        print("Top Tracks:")
        for j, track in enumerate(top_tracks['tracks'][:3], 1):  # Limit to 3 tracks per related artist
            print(f"  {j}. {track['name']}")
        print("\n")


# Example usage
if __name__ == "__main__":
    artist_name = input("请输入歌手名字：")
    artist = get_artist_details(artist_name)
    if artist:
        recommend_tracks_by_artist(artist)
