# TuneScribe

## Project Overview

**TuneScribe** is a web application that allows users to generate Spotify playlists based on a given sentence or phrase. The application leverages the Spotify API to search for songs whose titles match words or phrases in the user's input, creating a playlist that reflects the essence of the entered text. This project combines web development with Flask, OAuth for Spotify authentication, and various programming techniques to create a seamless and engaging user experience.

## Project Description

TuneScribe is designed to make creating personalized Spotify playlists fun and intuitive. Users enter a sentence or phrase into the web interface, and TuneScribe processes this input to generate a playlist. The application standardizes the input by removing punctuation and expanding common contractions to ensure accurate song searches. Using the Spotify API, TuneScribe searches for songs that match the words in the user's input and compiles these songs into a new playlist on the user's Spotify account.

Key features of TuneScribe include:
- **User Authentication**: Users log in with their Spotify credentials to allow the application to create playlists on their behalf.
- **Dynamic Playlist Creation**: The application generates playlists based on user input, ensuring a unique and personalized playlist every time.
- **Real-time Feedback**: A loading screen informs users that their playlist is being generated, and the resulting playlist is embedded on the page once it's ready.

## File Descriptions

### app.py

This is the main application file that contains the core logic for TuneScribe. It includes the following key components:
- **Flask Application Setup**: Initializes the Flask app and sets up routes for various endpoints.
- **Spotify Authentication**: Manages the OAuth flow to authenticate users with their Spotify accounts.
- **Playlist Generation**: Contains functions to standardize user input, search for matching songs using the Spotify API, and create playlists based on the input.
- **Session Management**: Handles user sessions to maintain authentication state across different pages.

### credentials.py

This file contains configuration settings for the application, including:
- **Spotify API Credentials**: Client ID, Client Secret, and Redirect URI for Spotify API authentication.

### contractions.py

This file contains a dictionary for expanding common contractions in user input to ensure accurate song searches. It is used to replace contractions in the input sentence with their expanded forms.

### requirements.txt

This file lists the Python dependencies required for the project. It includes libraries such as Flask, requests, and Spotipy.

### static/styles.css

This CSS file contains the styling rules for the application's user interface. Key styles include:
- **Dark Theme**: The background is set to black with Spotify's green color for text to create a visually appealing dark theme.
- **Custom Fonts**: The Varela Round and Codec Pro fonts are used throughout the application for a consistent and modern look.
- **Responsive Design**: Styles are designed to ensure the application is usable on various screen sizes.

### templates/index.html

This HTML file defines the structure of the main page of the application. It includes:
- **User Input Form**: A textarea for users to enter their sentence and a button to submit the form.
- **Loading Screen**: A message displayed while the playlist is being generated.
- **Embedded Playlist**: An iframe to display the generated playlist once it's ready.

## Design Choices

### User Input Standardization

To ensure accurate song searches, the input is standardized by:
- **Removing Punctuation**: Punctuation marks are removed from the input to avoid mismatches.
- **Expanding Contractions**: Common contractions are expanded to their full forms using a predefined dictionary from `contractions.py`.

### Caching Search Results

The application uses caching to optimize repeated song searches. This reduces the number of API calls and improves performance, especially when dealing with common words.

### Searching Mechanism

The search mechanism involves several steps:
1. **Standardizing Input**: The user's input sentence is standardized by removing punctuation and expanding contractions.
2. **Generating Phrases**: The standardized sentence is split into words, and various combinations of these words are generated to form phrases.
3. **Searching for Songs**: The application uses the Spotify API to search for songs matching each phrase. Cached results are used to minimize redundant API calls.
4. **Selecting Songs**: The application selects songs that match the phrases, ensuring they align closely with the user's input.

### Error Handling

If a playlist cannot be generated (e.g., due to lack of matching songs), the application handles this gracefully by displaying an appropriate message to the user.

### UI Design

The user interface is designed to be simple and intuitive. Key elements include:
- **Dark Theme**: Inspired by Spotify's branding, the application uses a black background and green text.
- **Loading Screen**: Provides real-time feedback to users while the playlist is being generated.
- **Fun Messaging**: Titles and buttons use playful language to enhance user engagement.

## Conclusion

TuneScribe combines the power of Flask, the Spotify API, and various web development techniques to create a fun and engaging application for generating personalized playlists. The project demonstrates the integration of multiple technologies and careful attention to user experience. By standardizing user input, caching search results, and handling errors gracefully, TuneScribe ensures a smooth and enjoyable user journey from start to finish.
