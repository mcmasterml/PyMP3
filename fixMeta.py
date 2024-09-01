import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


def process_title(title):
    # Split title by " - " to separate artist from title
    artist_title_split = title.split(" - ", 1)
    if len(artist_title_split) < 2:
        return None, None, None  # Skip if title format is not as expected

    # Extract artist and full title
    artist = artist_title_split[0]
    full_title = artist_title_split[1]

    # Further split the full title to remove the source tag
    title, _ = full_title.rsplit(" ", 1)

    # Extract featured artists and remix artist from the title
    featured_artists = title.split("feat.")[1].split("(")[0].strip()
    remix_artist = title.split("(")[1].replace(" Remix)", "").strip()

    # Combine the extracted parts
    title = title.split("feat.")[0].strip()
    artist_list = [artist, featured_artists, remix_artist]

    return title, ", ".join(artist_list), ""


def update_mp3_metadata(file_path):
    audio = MP3(file_path, ID3=EasyID3)

    # Extract current title
    current_title = audio.get('title', [None])[0]

    if not current_title:
        print(f"No title found for {file_path}")
        return

    # Process title and update metadata
    title, artist, album = process_title(current_title)
    if title and artist:
        audio['title'] = title
        audio['artist'] = artist
        audio['album'] = album
        audio.save()
        print(f"Updated metadata for {file_path}")
    else:
        print(f"Skipped {file_path} due to unexpected title format.")


def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp3"):
            file_path = os.path.join(folder_path, filename)
            update_mp3_metadata(file_path)


# Replace this with the path to your folder containing the MP3 files
folder_path = "/path/to/your/mp3/folder"
process_folder(folder_path)
