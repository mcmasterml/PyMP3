import os
import re
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3, HeaderNotFoundError


def process_title(title):
    # Use regex to split the title by the first hyphen surrounded by spaces
    artist_title_split = re.split(r'\s*-\s*', title, maxsplit=1)
    if len(artist_title_split) < 2:
        return None, None, None  # Skip if title format is not as expected

    # Extract artist and full title
    artist = artist_title_split[0].strip()
    full_title = artist_title_split[1].strip()

    # Remove the source tag at the end (e.g., 'myfreemp3.vip')
    full_title = re.sub(r'\s*\bmyfreemp3\.vip\b\s*$', '', full_title).strip()

    # Extract the main title, featured artists, and remix artist using regex
    title_match = re.match(
        r'(?P<title>.*?)\s*feat\.\s*(?P<featured>.*?)\s*\((?P<remix>.*?) Remix\)', full_title, re.IGNORECASE)

    if title_match:
        title = title_match.group('title').strip()
        featured_artists = title_match.group('featured').strip()
        remix_artist = title_match.group('remix').strip()

        # Combine the extracted parts
        artist_list = [artist, featured_artists, remix_artist]
        return title, ", ".join(artist_list), ""
    else:
        # If the format doesn't match the expected pattern, just return the full title
        return full_title, artist, ""


def update_mp3_metadata(file_path):
    try:
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
    except HeaderNotFoundError:
        print(f"Skipping file {file_path}: not a valid MP3 file.")
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")


def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp3"):
            file_path = os.path.join(folder_path, filename)
            update_mp3_metadata(file_path)


# Replace this with the path to your folder containing the MP3 files
folder_path = "/your/folder/path"
process_folder(folder_path)
