# TuneScribe by @mariahazmir

## 🎶 Project Overview

Welcome to **TuneScribe** – the magical app that turns your words into a personalized Spotify playlist! The songs are arranged in the exact order of the words in your sentence, creating a playlist that is a direct, musical replica of your input. Each word in your sentence corresponds to a song, making the playlist a true reflection of your original phrase. Imagine typing in a sentence, phrase, or even your favorite quote, and having it transformed into a unique playlist that reflects the essence of your input.

This web app is built with a blend of Flask wizardry, Spotify API smarts, and a sprinkle of OAuth magic, all designed to make your music experience seamless and fun. Ready to turn your thoughts into tunes? Let's dive in!

## 🎸 Project Description

**TuneScribe** makes playlist creation as easy as typing. Just enter a sentence or phrase, and watch as TuneScribe works its magic to craft a Spotify playlist that speaks your language – literally. It’s all about creating something special and personal, just for you.

### How It Works:
- **User-Friendly Login**: Sign in with your Spotify account and let TuneScribe handle the rest.
- **Unique Playlists Every Time**: No two playlists are the same – your input shapes your tunes!
- **Real-Time Feedback**: While your playlist is being composed, you'll get a nifty loading screen. Once it's ready, your playlist is displayed right on the page. 🎉

## 🛠️ File Descriptions

### `app.py`
This is the brain of TuneScribe – the file where all the magic happens:
- **Flask Setup**: Lays down the foundation of the app.
- **Spotify Authentication**: Handles the sign-in process with Spotify, so you can create playlists directly in your account.
- **Playlist Wizardry**: Transforms your sentence into a playlist by standardizing input, searching for songs, and compiling them.
- **Session Management**: Keeps you logged in and happy across the site.

### `credentials.py`
The vault for TuneScribe’s Spotify secrets:
- **Spotify API Credentials**: Your ticket to accessing the Spotify universe – includes Client ID, Secret, and Redirect URI.

### `contractions.py`
No more "cant" or "wont" – this file expands contractions to make sure your playlists hit the right notes:
- **Contraction Expansion**: A handy dictionary that turns "youre" into "you're" for more accurate song searches.

### `requirements.txt`
The shopping list for TuneScribe’s Python needs:
- **Dependencies**: Everything from Flask to Spotipy – all the ingredients that make TuneScribe run smoothly.

### `static/styles.css`
The fashion statement for TuneScribe’s UI:
- **Dark Mode**: Black backgrounds and Spotify-green text for that sleek, modern look.
- **Cool Fonts**: Using Varela Round and Codec Pro to keep things stylish.
- **Responsive Design**: Looks great on any screen – whether you’re on your phone or desktop.

### `templates/index.html`
The heart of TuneScribe’s interface:
- **Input Form**: Where you type your magic words.
- **Loading Screen**: A fun little animation while your playlist is being crafted.
- **Playlist Display**: An embedded Spotify playlist, tailored just for you.

## 🎨 Design Choices

### Input Magic
To make sure your playlist matches your vibe:
- **No Punctuation**: Punctuation is stripped out to avoid any hiccups.
- **Contraction Expansion**: Common contractions are expanded to ensure no word is left behind.

### Speedy Searches
TuneScribe is quick on its feet, using caching to speed up song searches. Efficiency at its best!

### Search Mechanism
1. **Standardizing Input**: Your sentence is cleaned up and ready for action.
2. **Phrase Generation**: We create magic word combos to find the best songs.
3. **Song Search**: We hit the Spotify database to find tracks that match your input.
4. **Song Selection**: Only the best songs make the cut for your playlist.

### Smooth Error Handling
If we can’t find enough songs, no worries! We’ll let you know with a friendly message and some suggestions.

### Fun UI Design
The whole app is designed to keep things light and engaging:
- **Dark Theme**: Inspired by Spotify’s own look, with our twist.
- **Loading Screen**: Keeps you in the loop while your playlist is in the oven.
- **Playful Language**: We’re all about having fun here, from titles to buttons.

## 🎧 Conclusion

**TuneScribe** is your go-to app for turning words into music. With a combination of cutting-edge tech and thoughtful design, it makes playlist creation not just easy, but enjoyable. Whether you're chilling, partying, or just daydreaming, TuneScribe creates a musical experience that's uniquely yours. So go ahead – type, tune, and vibe!
