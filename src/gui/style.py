import dearpygui.dearpygui as dpg


def load_themes():
    colour_red = (164, 6, 6)
    colour_orange = (217, 131, 46)
    colour_black = (0, 0, 0)
    colour_grey = (40, 40, 40)
    colour_orange_muted = (217, 131, 46, 200)
    colour_white = (240, 240, 240)

    with dpg.theme(tag='listbox_theme'):
        with dpg.theme_component():
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, colour_orange,
                                category=dpg.mvThemeCat_Core)  # listbox item: selected
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, colour_red,
                                category=dpg.mvThemeCat_Core)  # listbox item: hovered
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, colour_red,
                                category=dpg.mvThemeCat_Core)  # listbox item: hovered + clicked
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, colour_black,
                                category=dpg.mvThemeCat_Core)  # listbox background colour

    with dpg.theme(tag='app_theme'):
        with dpg.theme_component():
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, colour_black,
                                category=dpg.mvThemeCat_Core)  # background colour
            dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0,
                                category=dpg.mvThemeCat_Core)  # window border thickness
            dpg.add_theme_style(dpg.mvStyleVar_SelectableTextAlign, 0.5, 0.5,
                                category=dpg.mvThemeCat_Core)  # apply listbox only theme
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, colour_black, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, colour_grey, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, colour_orange_muted, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, colour_orange_muted, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, colour_white, category=dpg.mvThemeCat_Core)

    with dpg.theme(tag='button_theme'):
        with dpg.theme_component():
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Button, colour_orange, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, colour_red, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, colour_red, category=dpg.mvThemeCat_Core)

    with dpg.theme(tag='song_playing_theme'):
        with dpg.theme_component():
            # set the colour of all states of a button to the background colour
            dpg.add_theme_color(dpg.mvThemeCol_Button, colour_black, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, colour_black, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, colour_black, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, colour_orange, category=dpg.mvThemeCat_Core)


def load_fonts():
    # add fonts to font registry
    with dpg.font_registry():
        # add font (set as default for entire app)
        default_font = dpg.add_font(id='font1', file='fonts/open_sans/opensans_regular.ttf', size=20)

        dpg.bind_font(default_font)

        # add second font
        dpg.add_font(tag="font2", file='fonts/sedgwick_ave_display/sedgwickavedisplay-regular.ttf', size=36)

        # add third font
        dpg.add_font(tag="font3", file='fonts/pacifico/pacifico-regular.ttf', size=140)

        # add fourth font, used for logo 'music player' part of the logo.
        # Font size must match size specified in draw_text.
        dpg.add_font(tag="font4", file='fonts/reader_pro/readerpro_medium.ttf', size=21)
