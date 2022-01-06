import dearpygui.dearpygui as dpg
import musicplayer.musicplayer as musicplayer
import gui.gui as gui
import gui.files as files
import musicplayer.controller as controller


def setup():
    music_folder = 'music'
    first_song, music_files = files.get_first_song(music_folder)
    mp = musicplayer.Player(first_song)
    app_state = gui.AppState()
    logo_fader = gui.Fader()
    leaves_button_fader = gui.Fader()
    main_window, logo_window = gui.gui(mp, music_folder, music_files, app_state)
    gui.setup_graphics()
    raccoons = gui.create_raccoons()
    fire = gui.create_fire()
    smoke1 = gui.create_smoke(303)
    smoke2 = gui.create_smoke(328)
    particles = gui.create_particle()
    gui.show_viewport()
    return raccoons, mp, app_state, logo_fader, leaves_button_fader, fire, smoke1, smoke2, particles


def run(raccoons, mp, app_state, logo_fader, leaves_button_fader, fire, smoke1, smoke2, particles):
    raccoon_timer = gui.Timer(0.05)
    fire_timer = gui.Timer(0.085)
    smoke_timer1 = gui.TimerInterval(6.5, 0.11, 10)  # run 10 frames at 0.10 seconds interval after 8 seconds,
    smoke_timer2 = gui.TimerInterval(5.0, 0.10, 10)  # the interval then changes randomly after that.
    particles_timer = gui.Timer(0.01)
    reset_particles_timer = gui.TimerRandom(15.0, 65.0, 80.0)
    frame_timer = gui.Timer(0.01)

    while dpg.is_dearpygui_running():

        # get music player state
        player_state = controller.mp_state(mp)

        # move all animated objects

        if raccoon_timer.update():

            # dance if music is playing
            if player_state == 'play':
                for raccoon in raccoons:
                    raccoon.dance()

            # stay idle if music is not playing
            elif player_state in ['pause', 'stop']:
                for raccoon in raccoons:
                    raccoon.idle()

        if fire_timer.update():
            fire.update()

        if smoke_timer1.update():
            smoke1.update()

        if smoke_timer2.update():
            smoke2.update()

        if particles_timer.update():
            for particle in particles:
                particle.update()

        if reset_particles_timer.update():
            for particle in particles:
                particle.reset()

        # update the viewport height except when the user pressed the close button
        if not app_state.closing:
            move_frame = frame_timer.update()
            if move_frame:
                gui.update_viewport_height(player_state, 500, 650, 1)

                # fade the logo when the music and animation is playing
                gui.update_logo_fader(player_state, logo_fader, 1)

        else:

            # when the user pressed the close button:
            # 1. reduce the viewport to only show the logo
            # 2. closing_phase: wait for 2.5 seconds
            # 3. reduce the viewport until nothing is showing and exit the music player app

            move_frame = frame_timer.update()

            # 2. show the logo on screen for 2.5 seconds
            if move_frame and app_state.closing_phase == 1:
                app_state.closing_phase = 2

                # set timer for step # 3
                frame_timer = gui.Timer(0.01)

            # 3. reduce the viewport until nothing is showing and exit the music player app
            if move_frame and app_state.closing_phase == 2:
                new_viewport_height = gui.update_viewport_height('stop', 0, 650, 1)
                if new_viewport_height == 0:
                    controller.mp_close(mp)
                    dpg.stop_dearpygui()

            # 1. reduce the viewport to only show the logo
            if move_frame and app_state.closing_phase == 0:
                gui.update_logo_fader('stop', logo_fader, 1)
                gui.update_leaves_button_fader(leaves_button_fader, 2)
                new_viewport_height = gui.update_viewport_height('stop', 170, 650, 2)
                if new_viewport_height <= 170:
                    app_state.closing_phase = 1

                    # set timer for step # 2
                    frame_timer = gui.Timer(2.5)

        dpg.render_dearpygui_frame()


def main():
    raccoons, mp, app_state, logo_fader, leaves_button_fader, fire, smoke1, smoke2, particle = setup()
    run(raccoons, mp, app_state, logo_fader, leaves_button_fader, fire, smoke1, smoke2, particle)

    # destroy_context should not be placed inside the render loop to avoid an error
    dpg.destroy_context()


if __name__ == "__main__":
    main()
