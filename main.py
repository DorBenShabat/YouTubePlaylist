import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import json


def get_authenticated_service():
    client_id = os.environ.get('YOUTUBE_CLIENT_ID')
    client_secret = os.environ.get('YOUTUBE_CLIENT_SECRET')

    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [
                "urn:ietf:wg:oauth:2.0:oob",
                "http://localhost"
            ]
        }
    }

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_config(
        client_config, scopes=["https://www.googleapis.com/auth/youtube.force-ssl"]
    )

    credentials = flow.run_local_server(port=0)
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)


def create_playlist(youtube, title):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": "A playlist created by a Python script",
                "defaultLanguage": "en"
            },
            "status": {
                "privacyStatus": "private"
            }
        }
    )
    response = request.execute()
    return response["id"]


def get_all_songs_in_playlist(youtube, playlist_id):
    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=50,
        playlistId=playlist_id
    )
    response = request.execute()
    return [(item['snippet']['resourceId']['videoId'], item['snippet']['title']) for item in response.get('items', [])]


def add_songs_to_playlist(youtube, playlist_id, songs):
    existing_songs = get_all_songs_in_playlist(youtube, playlist_id)
    existing_song_ids = [song[0] for song in existing_songs]
    for song in songs:
        song_query = f"{song['song']} {song['singer']}"
        song_id = search_song(youtube, song_query)
        if song_id and song_id not in existing_song_ids:
            add_song_to_playlist(youtube, playlist_id, song_id)


def search_song(youtube, song):
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=song
    )
    response = request.execute()
    items = response.get("items")
    if items:
        return items[0]["id"]["videoId"]
    return None


def add_song_to_playlist(youtube, playlist_id, song_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": song_id
                }
            }
        }
    )
    response = request.execute()


def load_songs_from_json(json_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []



def add_new_song():
    song = input("Enter the name of the song: ")
    singer = input("Enter the name of the singer: ")
    return {"song": song, "singer": singer}


def save_songs_to_json(songs, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(songs, json_file, ensure_ascii=False, indent=4)


def get_playlist_id(youtube, title):
    request = youtube.playlists().list(
        part="snippet",
        maxResults=50,
        mine=True
    )
    response = request.execute()

    for item in response.get("items", []):
        if item["snippet"]["title"] == title:
            return item["id"]

    return None


def update_json_list(youtube, playlist_id, songs):
    existing_songs = get_all_songs_in_playlist(youtube, playlist_id)
    existing_song_ids = [song[0] for song in existing_songs]
    updated_songs = []

    for song_id, song_title in songs:
        if song_id not in existing_song_ids:
            if "-" in song_title:
                split_title = song_title.split(" - ", 1)
                singer = split_title[0]
                song_name = split_title[1]
            else:
                singer = ""
                song_name = song_title
            updated_songs.append({"song": song_name.strip(), "singer": singer.strip()})
        else:
            for song in existing_songs:
                if song[0] == song_id:
                    if "-" in song_title:
                        split_title = song_title.split(" - ", 1)
                        singer = split_title[0]
                        song_name = split_title[1]
                    else:
                        singer = ""
                        song_name = song_title
                    updated_songs.append({"song": song_name.strip(), "singer": singer.strip()})
                    break

    save_songs_to_json(updated_songs, 'songs_to_add.json')



if __name__ == "__main__":
    youtube = get_authenticated_service()
    playlist_name = "Reggaeton playlist created by Python"
    playlist_id = get_playlist_id(youtube, playlist_name)
    if not playlist_id:
        playlist_id = create_playlist(youtube, playlist_name)

    songs = load_songs_from_json('songs_to_add.json')
    songs_to_save = get_all_songs_in_playlist(youtube, playlist_id)
    save_songs_to_json(songs_to_save, 'songs_to_add.json')

    while True:
        choice = input("What would you like to do?\n1. Update the JSON list according to songs in the playlist.\n2. Add new songs to the playlist and update the JSON list.\nEnter your choice (1 or 2): ")
        if choice == '1':
            update_json_list(youtube, playlist_id, songs_to_save)
            break
        elif choice == '2':
            while True:
                add_song = input("Would you like to add a new song to the list? (Y/N): ")
                if add_song.lower() == 'y':
                    new_song = add_new_song()
                    songs.append(new_song)
                else:
                    break
            save_songs_to_json(songs, 'songs_to_add.json')
            add_songs_to_playlist(youtube, playlist_id, songs)
            break
        else:
            print("Invalid choice. Please enter either 1 or 2.")



