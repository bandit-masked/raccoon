from os import listdir


def get_music_files(folder):
    return [
        file
        for file in listdir(folder)
        if file.endswith('.mp3')
        or file.endswith('.flac')
        or file.endswith('.wav')
    ]


def get_first_song(music_folder):
    try:
        music_files = get_music_files(music_folder)
    except:  # in case music_folder does not exist
        music_files = []
    first_song = 'No music files' if not music_files else music_files[0]
    return first_song, music_files
