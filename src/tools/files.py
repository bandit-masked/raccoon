from os import listdir


def get_music_files(folder):
    file_names = []
    for file in listdir(folder):
        if file.endswith('.mp3') or file.endswith('.flac') or file.endswith('.wav'):
            file_names.append(file)
    return file_names


def get_first_song(music_folder):
    try:
        music_files = get_music_files(music_folder)
    except:  # in case music_folder does not exist
        music_files = []
    if music_files == []:
        first_song = 'No music files'
    else:
        first_song = music_files[0]
    return first_song, music_files
