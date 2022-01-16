import miniaudio


class Player:

    def __init__(self, first_song):
        self.player_state = 'new'  # available player states: new, play, pause, stop
        self.info = None
        self.duration = ''
        self.playback_device = None
        self.listbox_song = first_song  # ''
        self.song_playing = first_song  # ''
        self.listbox_song_filename = first_song
        self.same_song_selected = False
        self.go_play = False
        self.go_stop = False
        self.go_load = False
        # calling the playback_device on init without a song, so it starts
        # faster when actually calling it again when playing the first song.
        self.playback_device = miniaudio.PlaybackDevice()

    def song_change(self, sender, listbox_song, music_folder):
        self.listbox_song = listbox_song
        self.listbox_song_filename = music_folder + '/' + self.listbox_song
        if self.listbox_song == self.song_playing:
            self.same_song_selected = True
        else:
            self.same_song_selected = False

    def playback_status(self):
        return self.player_state

    def stream_progress_callback(self, framecount):
        pass

    def stream_end_callback(self):
        self.player_state = 'stop'

    def play(self):
        # Depending on the state of the player, the following actions may be required.
        #
        # 1. Stop device
        # 2. Load new song
        # 3. Play song (start from beginning)

        # NEW: This is the player state after starting the app
        if self.player_state == 'new':
            self.go_stop = False
            self.go_load = True
            self.go_play = True

        elif self.player_state == 'pause':
            self.go_stop = False
            self.go_load = not self.same_song_selected
            self.go_play = True

        elif self.player_state in ['stop', 'play']:
            self.go_stop = True
            self.go_load = True
            self.go_play = True

        if self.go_stop:
            self.playback_device.close()  # close = pause music and close device
            self.go_stop = False

        if self.go_load:
            try:
                self.filestream = miniaudio.stream_file(self.listbox_song_filename)
                self.callbacks_stream = miniaudio.stream_with_callbacks(self.filestream, self.stream_progress_callback,
                                                                        self.stream_end_callback)
                next(self.callbacks_stream)  # start the generator
            except:
                self.player_state = 'stop'
                self.song_playing = ''
                self.duration = 0
                error = True
                return self.player_state, self.song_playing, self.duration, error

            self.go_load = False

        if self.go_play:
            if self.player_state in ['stop', 'play']:
                self.playback_device = miniaudio.PlaybackDevice()
            self.playback_device.start(self.callbacks_stream)
            self.info = miniaudio.get_file_info(self.listbox_song_filename)
            self.duration = int(round(self.info.duration, 0))

            # Update variables
            self.player_state = 'play'
            self.song_playing = self.listbox_song
            self.same_song_selected = True

        return self.player_state, self.song_playing, self.duration, False

    def pause(self):
        if self.player_state == 'play':
            self.playback_device.stop()
            self.player_state = 'pause'

        return self.player_state, self.song_playing, self.duration, False

    def stop(self):
        if self.player_state not in ['new', 'stop']:
            self.playback_device.close()  # close = pause music and close device
            self.player_state = 'stop'
        return self.player_state, self.song_playing, self.duration, False

    def close_app(self):
        # stop the playback_device if it is running in the background
        if self.player_state != 'new':
            self.playback_device.stop()
