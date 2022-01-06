import dearpygui.dearpygui as dpg
import gui.config as config
import gui.style as style
import gui.graphics as graphics
import musicplayer.controller as controller
import random


class AppState:
    def __init__(self):
        self.closing = False
        self.closing_phase = 0


class Fader:
    def __init__(self):
        self.level = 0  # 0 = fully transparent


class Timer:
    # keeps track of DPG time since last render
    # note: frame rate speeds up by a factor of 4 to 5
    # when manipulating the viewport

    def __init__(self, interval):
        self.total_time = dpg.get_total_time()
        self.last_total_time = dpg.get_total_time()
        self.interval = interval

    def update(self):
        self.total_time = dpg.get_total_time()
        delta_time = dpg.get_total_time() - self.last_total_time
        if delta_time > self.interval:
            self.last_total_time = self.total_time
            return True
        return False


class TimerRandom:

    def __init__(self, initial_interval, min_interval, max_interval):
        self.total_time = dpg.get_total_time()
        self.last_total_time = dpg.get_total_time()
        self.interval = initial_interval
        self.min_interval = min_interval
        self.max_interval = max_interval

    def update(self):
        self.total_time = dpg.get_total_time()
        delta_time = dpg.get_total_time() - self.last_total_time
        if delta_time > self.interval:
            self.last_total_time = self.total_time
            self.interval = random.randrange(self.min_interval, self.max_interval)
            return True
        return False


class TimerInterval:

    # TimerInterval runs a series of frames back-to-back and breaks in between.
    # The first interval is specified. After that, the interval is a
    # random value in a range of values (hard-coded in the class).
    # This is used to create randomness in the puffs of smoke for example.

    def __init__(self, interval_time, frame_time, num_frames):

        # variables used for the interval
        self.interval_time = interval_time
        self.num_frames = num_frames
        self.last_total_interval_time = dpg.get_total_time()

        # variables used for the animation loop
        self.frame_time = frame_time
        self.animation_loop = False
        self.current_frame = 0
        self.last_total_frame_time = 0

        # variables used for interval and animation loop
        self.total_time = dpg.get_total_time()
        self.last_total_time = dpg.get_total_time()
        self.state = False

    def update(self):
        self.state = False
        self.total_time = dpg.get_total_time()
        delta_interval_time = dpg.get_total_time() - self.last_total_interval_time

        if delta_interval_time > self.interval_time:
            self.animation_loop = True
            self.last_total_interval_time = self.total_time

        if self.animation_loop:  # the interval between animation has passed and a new animation is shown
            delta_frame_time = dpg.get_total_time() - self.last_total_frame_time

            if delta_frame_time > self.frame_time:
                self.last_total_frame_time = self.total_time
                self.current_frame += 1
                self.state = True

        if self.current_frame > self.num_frames:
            self.animation_loop = False
            self.current_frame = 0
            self.state = False
            self.interval_time = random.randrange(4, 11)

        return self.state


def update_viewport_height(player_state, min_height, max_height, step_size):
    viewport_height = dpg.get_viewport_height()
    new_viewport_height = dpg.get_viewport_height()

    # show animation window when playing music
    if player_state == 'play' and viewport_height < max_height:
        new_viewport_height = viewport_height + step_size
        dpg.set_viewport_height(new_viewport_height)
    if player_state == 'stop' and viewport_height > min_height:
        new_viewport_height = viewport_height - step_size
        dpg.set_viewport_height(new_viewport_height)

    return new_viewport_height


def update_logo_fader(player_state, fader, step_size):
    level = fader.level

    if player_state == 'play' and level < 150:
        # make the logo darker when playing music
        fader.level += step_size
        dpg.configure_item('logo_text_filter', fill=(0, 0, 0, fader.level))

    if player_state == 'stop' and level > 0:
        # make the logo brighter when 'stop' is pressed
        fader.level -= step_size
        dpg.configure_item('logo_text_filter', fill=(0, 0, 0, fader.level))


def update_leaves_button_fader(fader, step_size):
    if fader.level < 255:
        fader.level += step_size
        dpg.configure_item('leaves_button_filter', fill=(0, 0, 0, fader.level))


def setup_graphics():
    graphics.create_drawing_layers()
    graphics.load_logo()
    graphics.create_scene()


def create_raccoons():
    # load the textures once for all raccoons and all animations
    dance_left = graphics.load_textures('assets/raccoon/dance_left', 'raccoon', 'png', 14)
    dance_right = graphics.load_textures('assets/raccoon/dance_right', 'raccoon', 'png', 14)
    idle_left = graphics.load_textures('assets/raccoon/idle_left', 'raccoon', 'png', 11)
    idle_right = graphics.load_textures('assets/raccoon/idle_right', 'raccoon', 'png', 11)

    # create a dictionary of 4 lists containing the animation textures
    textures = {'dance_left': dance_left,
                'dance_right': dance_right,
                'idle_left': idle_left,
                'idle_right': idle_right}

    raccoons = []

    # raccoon crossing in the background
    raccoons.append(graphics.Raccoon(1400, 492, 5, 3.1, textures, 195, 195, 'right', True, 3000, 500, 0, 'layer_02'))
    raccoons.append(graphics.Raccoon(-500, 491, 11, -3.1, textures, 190, 190, 'left', True, 500, 3000, 0, 'layer_02'))

    # speedy raccoon
    raccoons.append(graphics.Raccoon(-1000, 495, 1, 6, textures, 180, 180, 'right', False, 2500, 7000, 0, 'layer_00'))

    # small raccoon
    raccoons.append(graphics.Raccoon(-2900, 497, 1, 2.5, textures, 200, 200, 'right', True, 1500, 4500, 0, 'layer_02'))

    # raccoons dancing together in the same direction
    raccoons.append(graphics.Raccoon(-2600, 488, 3, 3, textures, 165, 165, 'right', True, 1000, 6000, 0, 'layer_06'))
    raccoons.append(graphics.Raccoon(-2650, 488, 13, 3, textures, 163, 163, 'left', True, 1000, 6000, 0, 'layer_06'))
    raccoons.append(graphics.Raccoon(-2760, 487, 6, 3, textures, 168, 168, 'right', True, 1000, 6000, 0, 'layer_06'))
    raccoons.append(graphics.Raccoon(-2820, 491, 9, 3, textures, 161, 161, 'right', True, 1000, 6000, 0, 'layer_05'))

    # 2 raccoons near the fire
    raccoons.append(graphics.Raccoon(135, 490, 0, 1, textures, 200, 200, 'right', False, 35, 10, 10, 'layer_08'))
    raccoons.append(graphics.Raccoon(320, 489, 8, 0.8, textures, 188, 188, 'left', False, 5, 40, 10, 'layer_08'))

    # speedy raccoon foreground
    raccoons.append(graphics.Raccoon(-15000, 490, 9, 10, textures, 200, 200, 'right', True, 5000, 16000, 0, 'layer_09'))

    # hesitant raccoons
    raccoons.append(graphics.Raccoon(780, 489, 3, -0.7, textures, 180, 180, 'left', False, 250, 700, 10, 'layer_09'))
    raccoons.append(graphics.Raccoon(-1250, 497, 7, 0.7, textures, 175, 175, 'right', False, 0, 1200, 10, 'layer_09'))

    return raccoons


def create_fire():
    flames = graphics.load_textures('assets/flame', 'flame', 'png', 8)
    return graphics.Animation(280, 540, 8, flames, 100, 100, 'layer_07')


def create_smoke(x_pos):
    smokes = graphics.load_textures('assets/smoke', 'smoke', 'png', 10)
    return graphics.Animation(x_pos, 610, 10, smokes, 30, 30, 'layer_07')


def create_particle():
    particle_textures = graphics.load_textures('assets/particle', 'dust', 'png', 13)
    particles = []
    num_particles = random.randint(200, 300)
    x_pos = 1000  # particles are created out of range
    layer = 'layer_06'
    for _ in range(num_particles):
        y_pos = 445 + random.randint(0, 50) + x_pos / 10
        horizontal_speed = random.randint(6, 9) / 10
        starting_frame = random.randint(0, 12)
        size = random.randint(1, 7)
        particles.append(
            graphics.Particle(x_pos, y_pos, horizontal_speed, starting_frame, 13, 40, particle_textures, size, size,
                              layer))

    return particles


def app_state_close(sender, app_data, app_state):
    app_state.closing = True


def drag_viewport(sender, app_data, user_data):
    if dpg.get_mouse_pos(local=False)[1] < 140:  # only drag the viewport when dragging the logo
        drag_deltas = app_data
        viewport_current_pos = dpg.get_viewport_pos()
        new_x_position = viewport_current_pos[0] + drag_deltas[1]
        new_y_position = viewport_current_pos[1] + drag_deltas[2]
        new_y_position = max(new_y_position, 0) # prevent the viewport to go off the top of the screen
        dpg.set_viewport_pos([new_x_position, new_y_position])


def gui(mp, music_folder, music_files, app_state, fill):
    # sourcery skip: extract-method
    dpg.create_context()
    style.load_themes()
    style.load_fonts()

    with dpg.window(label='logo', **config.logo_window) as logo_window:
        dpg.bind_item_theme(logo_window, 'app_theme')
        leaf = graphics.load_texture('assets/scene/leaves_button.png')
        dpg.add_image_button(texture_tag=leaf, tag='close_button', pos=(543, 0), user_data=app_state,
                             callback=app_state_close, frame_padding=0)

        with dpg.handler_registry():
            dpg.add_mouse_drag_handler(button=0, threshold=0.0, callback=drag_viewport)

    with dpg.window(label="main window", **config.main_window) as main_window:
        dpg.bind_item_theme(main_window, 'app_theme')
        dpg.set_exit_callback(mp.close_app)

        if len(music_files) > 0:
            mp.song_change('sender_dummy', music_files[0], music_folder)
            dpg.add_listbox(tag='listbox_files', items=music_files,
                            callback=mp.song_change, user_data=music_folder, width=565, num_items=6)
        else:
            dpg.add_listbox(tag='listbox_files', items=['No music files'],
                            callback=mp.song_change, user_data=music_folder, width=565, num_items=6)
        dpg.bind_item_theme('listbox_files', 'listbox_theme')
        dpg.add_spacer(height=30)

        # buttons
        with dpg.group(tag='buttons'):
            dpg.bind_item_theme('buttons', 'button_theme')
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=31)
                dpg.add_button(tag='play_button', label='PLAY', user_data=[mp, 'play'],
                               callback=controller.mp_interface, **config.button)
                dpg.add_spacer(width=30)
                dpg.add_button(tag='pause_button', label='PAUSE', user_data=[mp, 'pause'],
                               callback=controller.mp_interface, **config.button)
                dpg.add_spacer(width=30)
                dpg.add_button(tag='stop_button', label='STOP', user_data=[mp, 'stop'],
                               callback=controller.mp_interface, **config.button)

        dpg.add_spacer(height=14)

        # display song name
        dpg.add_button(tag='song_name', label='', width=565)
        dpg.bind_item_theme('song_name', 'song_playing_theme')
        dpg.bind_item_font(item='song_name', font='font2')

    dpg.create_viewport(title='Music player', height=500, width=622, x_pos=100, y_pos=100, decorated=False)
    dpg.set_viewport_min_height(0)
    dpg.set_viewport_min_width(0)
    dpg.setup_dearpygui()
    return main_window, logo_window

def show_viewport():
    dpg.show_viewport()