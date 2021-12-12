import dearpygui.dearpygui as dpg


def mp_interface(sender, data, user_data):
    """mp_interface provides an interface between the GUI callbacks
    and the musicplayer object. It enables updating of the GUI based
    on the musicplayer return functions."""
    mp = user_data[0]  # mp is the musicplayer object
    action = user_data[1]  # action is the selected user action
    if action == 'play':
        player_state, listbox_song, duration, error = mp.play()
    elif action == 'pause':
        player_state, listbox_song, duration, error = mp.pause()
    else:
        player_state, listbox_song, duration, error = mp.stop()

    # update song name in the GUI
    if player_state != 'new':
        song_name = listbox_song.rsplit(".", 1)[0]
        dpg.configure_item(item='song_name', label=song_name)

    if error:
        song_name = 'File cannot be played'
        dpg.configure_item(item='song_name', label=song_name)


def mp_state(mp):
    return mp.playback_status()


def mp_close(mp):
    mp.close_app
