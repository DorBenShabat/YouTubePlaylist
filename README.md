# YouTubePlaylist

YouTubePlaylist is a Python script that allows you to create and manage playlists on YouTube. With this script, you can easily add songs to your YouTube playlists using the YouTube Data API.

## Features

- Authenticate with your YouTube account to gain access to your playlists.
- Create a new playlist or add songs to an existing playlist.
- Search for songs on YouTube using keywords.
- Avoid adding duplicate songs to your playlist.
- Load songs from a JSON file to populate your playlist.

## Prerequisites

Before running the script, make sure you have the following:

1. Python 3.x installed on your machine.
2. YouTube Data API credentials (client ID and client secret).
3. Set up the necessary environment variables (`YOUTUBE_CLIENT_ID` and `YOUTUBE_CLIENT_SECRET`) with your YouTube API credentials.

## Getting Started

1. Clone the repository:

   ```
   git clone https://github.com/DorBenShabat/YouTubePlaylist.git
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Run the script:

   ```
   python main.py
   ```

4. Follow the prompts to authenticate with your YouTube account and provide the necessary information to create or update your playlist.

## Configuration

- The `songs_to_add.json` file contains the list of songs to add to the playlist. You can modify this file to include your desired songs in the following format:

   ```
   [
       {
           "song": "Song Name",
           "singer": "Artist Name"
       },
       ...
   ]
   ```

- By default, the playlist will be set to private. You can modify the privacy status in the `create_playlist` function in the code.

## Contributions

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please feel free to open an issue or submit a pull request.

Enjoy creating and managing your YouTube playlists with ease using the YouTubePlaylist script!
