# Import necessary modules
import re  # Regular expressions for string manipulation
from flask import Flask, request, redirect, session, render_template, url_for, flash
import requests  # HTTP requests for interacting with external APIs
import json  # JSON handling
from spotipy import Spotify  # Spotify API client
from spotipy.oauth2 import SpotifyOAuth  # Spotify OAuth authentication
from functools import lru_cache  # Caching function results to optimize performance
import os  # For accessing environment variables

# Import the contractions dictionary
from contractions import contractions

# Retrieve API keys and configuration from environment variables
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')
scopes = os.getenv('SCOPES')

app = Flask(__name__)  # Initialize the Flask application
app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key')  # Use environment variable for secret key

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
    if not sentence:
        return None

    sentence = standardize_sentence(sentence)
    phrases = generate_phrases(sentence.split())

    for phrase_combination in phrases:
        songs = []
        for phrase in phrase_combination:
            song = token_to_song(phrase, spotify)
            if song:
                songs.append(song)

        if songs and len(songs) == len(phrase_combination):
            playlist = spotify.user_playlist_create(
                user=spotify.me()['id'],
                name=sentence,
                public=True,
                collaborative=False,
                description='Have fun with your playlist! Created by @mariahazmir on Github'
            )
            spotify.user_playlist_add_tracks(
                user=spotify.me()['id'],
                playlist_id=playlist['id'],
                tracks=songs
            )
            return playlist['id']

    return None

# Function to find a song matching the given token
def token_to_song(token, spotify):
    if token in ['a', 'to', 'the']:
        return None

    if token.lower() == 'and':
        return '5cIZoKmBiFgjabaBG0D9fO'

    banned = []
    query = f"track:{token}"

    for offset in range(0, 1000, 7):
        if banned:
            banned_suffix = " NOT " + " NOT ".join(banned)
            final_query = f"{query}{banned_suffix}"
        else:
            final_query = query

        if len(final_query) > 1000:
            final_query = final_query[:1000]

        try:
            tracks = cached_search(final_query, spotify)
        except Exception as e:
            print(f"Error during search: {e}")
            return None

        if not tracks:
            return None

        for track in tracks:
            if track['name'].lower() == token.lower():
                return track['uri']
            else:
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
                f'&client_id={client_id}&scope={scopes}&redirect_uri={redirect_uri}')
    return redirect(auth_url)

# Route to handle the callback from Spotify's authorization
@app.route('/callback')
def callback():
    code = request.args.get('code')
    auth_token_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_token_url, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    })
    auth_response_data = auth_response.json()
    session['access_token'] = auth_response_data.get('access_token')
    return redirect(url_for('index'))

# Route to handle playlist generation requests
@app.route('/generate_playlist', methods=['POST'])
def generate_playlist():
    sentence = request.form['sentence']

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

    embed_url = f"https://open.spotify.com/embed/playlist/{playlist_id}" if playlist_id else None
    return render_template('index.html', embed_url=embed_url)

# Run the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
