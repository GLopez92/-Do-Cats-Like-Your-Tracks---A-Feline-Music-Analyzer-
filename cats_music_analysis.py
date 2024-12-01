# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 08:41:25 2024

@author: GuillermoLopez
"""
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys


# 🎵 Spotify Fun Zone Initialization 🎵
print("🐾 Welcome to the 'Do Cats Like Your Tracks?' Analyzer! Let's get purring! 🐾")

# Initialize Spotipy client with credentials 🐱
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='xxxxxxxxxxxx',  # Replace with your Client ID
    client_secret='xxxxxxxxxxxx',  # Replace with your Client Secret
    redirect_uri='http://localhost:8888/callback',
    scope='user-read-private user-top-read playlist-read-private'
))


# 🎶 Function to fetch top tracks for a cool cat (artist)
def fetch_artist_top_tracks(artist_id):
    try:
        print("😺 Fetching top tracks for the coolest cat in the room...")
        results = sp.artist_top_tracks(artist_id)
        tracks = [{"name": track["name"], "id": track["id"]} for track in results["tracks"]]
        print(f"🎉 Fetched {len(tracks)} purr-worthy tracks for the artist!")
        return tracks
    except spotipy.exceptions.SpotifyException as e:
        print(f"🚫 Spotify API error: {e}")
        sys.exit()
    except Exception as e:
        print(f"😿 Unexpected error: {e}")
        sys.exit()


# 🎵 Function to fetch audio features for a track
def get_audio_features(track_id):
    try:
        print(f"🎧 Analyzing track ID: {track_id}")
        features = sp.audio_features(track_id)
        if features and features[0]:
            print(f"✅ Successfully fetched features for track ID: {track_id}")
            return {
                "tempo": features[0].get("tempo"),
                "energy": features[0].get("energy"),
                "danceability": features[0].get("danceability"),
                "name": track_id
            }
        else:
            print(f"⚠️ No audio features available for track ID: {track_id}. Cats disapprove. 😾")
    except spotipy.exceptions.SpotifyException as e:
        print(f"🚨 Spotify API error for Track ID: {track_id} - {e}")
    except Exception as e:
        print(f"💥 Unexpected error for Track ID: {track_id} - {e}")
    return None


# 🐾 Fetch and process tracks with feline-approved logic
def fetch_and_process_tracks(artist_id):
    tracks = fetch_artist_top_tracks(artist_id)
    if not tracks:
        print("😿 No tracks found for the artist. Cats are disappointed. Exiting...")
        sys.exit()

    audio_features = []
    for track in tracks:
        print(f"🎶 Processing track: {track['name']} (ID: {track['id']})")
        features = get_audio_features(track["id"])
        if features:
            print(f"😻 Adding track: {track['name']} to the analysis!")
            audio_features.append(features)
        else:
            print(f"❌ Skipping track: {track['name']} (ID: {track['id']}) - Cats say 'Nope!'")

    if not audio_features:
        print("💔 No valid audio features found. Cats are heartbroken. Exiting...")
        sys.exit()

    return pd.DataFrame(audio_features)


# 🐈 Assign cat-approved metrics for each track
def assign_cat_metrics(df):
    print("🐾 Assigning 'Meow Factor', 'Napability Index', and 'Zoomie Probability'... 🎉")
    df["Meow Factor"] = (df["energy"] - df["energy"].min()) / (df["energy"].max() - df["energy"].min()) * 10
    df["Napability Index"] = 10 - df["Meow Factor"]
    df["Zoomie Probability"] = (df["danceability"] - df["danceability"].min()) / (df["danceability"].max() - df["danceability"].min()) * 10
    return df


# 🎨 Generate fun visualizations for cat metrics
def generate_report(df):
    print("🎨 Creating a masterpiece for cat-approved tracks! 🖼️")
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        data=df,
        x="tempo",
        y="Meow Factor",
        size="Napability Index",
        hue="Zoomie Probability",
        sizes=(100, 500),
        palette="coolwarm",
        legend="full",
    )
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.title("🐾 Tracks Cats Will Purr To", fontsize=18)
    plt.xlabel("Tempo (BPM) 🕺", fontsize=14)
    plt.ylabel("Meow Factor 😻", fontsize=14)
    plt.legend(title="Zoomie Probability ⚡", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.show()

    # 🎉 Print the top tracks for cats
    top_meow = df.loc[df["Meow Factor"].idxmax()]["name"]
    top_nap = df.loc[df["Napability Index"].idxmax()]["name"]
    top_zoom = df.loc[df["Zoomie Probability"].idxmax()]["name"]

    print("\n🐾 **Feline Analysis Report** 🐾")
    print("✨ Tested with a panel of 12 highly discerning felines! 🐈‍⬛🐈")
    print(f"🎶 **Top Meow Factor Track**: {top_meow}")
    print(f"😴 **Best Nap Track**: {top_nap}")
    print(f"⚡ **Zoomie-Inducing Track**: {top_zoom}")


# 🐱 Main logic to get the purr-fect playlist
if __name__ == "__main__":
    print("🎬 Starting the Cat Music Analyzer... 😺")

    # Define your artist ID (replace with a valid Spotify artist ID)
    artist_id = "7aKKl2wFvnHgKNdEpORCMK"  # Replace with your artist's ID

    # Fetch and process tracks
    print("🔍 Fetching tracks and features...")
    df = fetch_and_process_tracks(artist_id)

    # Assign cat metrics
    print("📊 Calculating metrics for ultimate feline satisfaction...")
    df = assign_cat_metrics(df)

    # Generate report and visualizations
    print("📈 Generating cat-approved analytics... 🐾")
    generate_report(df)

    print("😻 Analysis complete! Your cats now have a purr-fect playlist!")
