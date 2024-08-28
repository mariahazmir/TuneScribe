# Import necessary modules
import re  # Regular expressions for string manipulation
# Flask web framework and related functions
from flask import Flask, request, redirect, session, render_template, url_for, flash
import requests  # HTTP requests for interacting with external APIs
import json  # JSON handling
from spotipy import Spotify  # Spotify API client
from spotipy.oauth2 import SpotifyOAuth  # Spotify OAuth authentication
from functools import lru_cache  # Caching function results to optimize performance

# Import the contractions dictionary and Spotify credentials
from contractions import contractions
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPES

app = Flask(__name__)  # Initialize the Flask application
app.secret_key = 'chicken_noodle_soup'  # Set the secret key for session management

# Function to create a Spotify client instance using the provided token


def create_spotify_client(token):
    return Spotify(auth=token)

# Caching search results to optimize repeated queries


@lru_cache(maxsize=1000)
def cached_search(query, spotify):
    return spotify.search(q=query, type='track', limit=50)['tracks']['items']

# Function to convert the user's sentence to a standardized format


def standardize_sentence(sentence):
    # Remove punctuation except for apostrophes
    sentence = re.sub(r'[^\w\s\']', '', sentence)
    # Convert the sentence to lowercase
    sentence = sentence.lower()
    # Replace contractions with their expanded forms
    for word, replacement in contractions.items():
        sentence = re.sub(r'\b' + word + r'\b', replacement, sentence)
    return sentence

# Function to create a Spotify playlist based on a given sentence


def create_playlist(sentence, spotify):
    # If the sentence is empty, return None
    if not sentence:
        return None

    # Standardize the input sentence
    sentence = standardize_sentence(sentence)
    # Generate all possible phrase combinations from the sentence
    phrases = generate_phrases(sentence.split())

    # Iterate through each phrase combination to find matching songs
    for phrase_combination in phrases:
        songs = []
        for phrase in phrase_combination:
            song = token_to_song(phrase, spotify)
            if song:
                songs.append(song)

        # If songs are found for the entire phrase combination, create a playlist
        if songs and len(songs) == len(phrase_combination):
            # Create a new playlist with the name 'Your Phrase Playlist'
            playlist = spotify.user_playlist_create(
                user=spotify.me()['id'],
                name=sentence,
                public=True,
                collaborative=False,
                description='Have fun with your playlist! Created by @mariahazmir on Github'
            )
            # Add the found songs to the playlist
            spotify.user_playlist_add_tracks(
                user=spotify.me()['id'],
                playlist_id=playlist['id'],
                tracks=songs
            )
            return playlist['id']

    return None

# Function to find a song matching the given token


def token_to_song(token, spotify):
    # Skip common short words
    if token in ['a', 'to', 'the']:
        return None

    # Return a specific song URI for the word 'and'
    if token.lower() == 'and':
        return '5cIZoKmBiFgjabaBG0D9fO'

    # List to keep track of banned words
    banned = []
    # Create a search query for the token
    query = f"track:{token}"

    # Search for tracks matching the token, handling up to 1000 results
    for offset in range(0, 1000, 7):
        if banned:
            banned_suffix = " NOT " + " NOT ".join(banned)
            final_query = f"{query}{banned_suffix}"
        else:
            final_query = query

        # Ensure the query length does not exceed 1000 characters
        if len(final_query) > 1000:
            final_query = final_query[:1000]

        try:
            # Search for tracks using the cached search function
            tracks = cached_search(final_query, spotify)
        except:
            return None

        # If no tracks are found, return None
        if not tracks:
            return None

        # Check if the track name matches the token exactly
        for track in tracks:
            if track['name'].lower() == token.lower():
                return track['uri']
            else:
                # Add mismatched words to the banned list to refine the search
                words = track['name'].split(' ')
                for word in words:
                    if word.lower() != token.lower() and len(banned) < 10:
                        banned.append(word)
                offset = 0
    return None

# Function to generate all possible phrase combinations from a list of words


def generate_phrases(words):
    n = len(words)
    phrases = []

    # Helper function to recursively generate combinations
    def generate_combinations(start, current_combination):
        if start == n:
            if current_combination:
                phrases.append(current_combination[:])
            return

        for i in range(start, n):
            current_combination.append(' '.join(words[start:i+1]))
            generate_combinations(i + 1, current_combination)
            current_combination.pop()

        if start < n - 1:
            current_combination.append(words[start])
            generate_combinations(start + 1, current_combination)
            current_combination.pop()

    generate_combinations(0, [])
    return phrases

# Route to render the index page


@app.route('/')
def index():
    return render_template('index.html')

# Route to redirect users to the Spotify authorization page


@app.route('/login')
def login():
    auth_url = ('https://accounts.spotify.com/authorize?response_type=code'
                f'&client_id={CLIENT_ID}&scope={SCOPES}&redirect_uri={REDIRECT_URI}')
    return redirect(auth_url)

# Route to handle the callback from Spotify's authorization


@app.route('/callback')
def callback():
    code = request.args.get('code')
    auth_token_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_token_url, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    auth_response_data = auth_response.json()
    session['access_token'] = auth_response_data['access_token']
    return redirect(url_for('index'))

# Route to handle playlist generation requests


@app.route('/generate_playlist', methods=['POST'])
def generate_playlist():
    sentence = request.form['sentence']

    # Check if the sentence exceeds 200 characters
    if len(sentence) > 200:
        flash('Oops! The sentence must be 200 characters or less.')
        return redirect(url_for('index'))

    access_token = session.get('access_token')

    if not access_token:
        return redirect(url_for('login'))

    spotify = create_spotify_client(access_token)
    playlist_id = create_playlist(sentence, spotify)

    if not playlist_id:
        flash('Sorry! We could not generate a playlist. How about a different sentence?')

    # Generate the embed URL for the created playlist
    embed_url = f"https://open.spotify.com/embed/playlist/{playlist_id}" if playlist_id else None
    return render_template('index.html', embed_url=embed_url)


# Run the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
