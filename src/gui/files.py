from pathlib import Path


def get_music_files(folder_str):
    folder = Path(folder_str)
    items = folder.iterdir()  # folders and files
    extensions = ['.FLAC', '.MP3', '.WAV']
    return [item.name for item in items if item.is_file() and item.suffix.upper() in extensions]


def get_first_song(music_folder):
    try:
        music_files = get_music_files(music_folder)
    except:  # in case music_folder does not exist
        music_files = []
    first_song = 'No music files' if not music_files else music_files[0]
    return first_song, music_files
