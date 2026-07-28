default tree_game_progress = 1
default tree_game_zone = (0.4, 0.6)
default tree_game_done = False
default tree_game_start_time = 0.0
default tree_game_crawler_frac = 0.0
default tree_game_moving_forward = True
default tree_game_display_frame = 1

init python:

    TREE_GAME_TOTAL_FRAMES = 53
    TREE_GAME_WIN_FRAME = 26
    TREE_GAME_PERIOD = 1.4
    TREE_GAME_MIN_ZONE = 0.09
    TREE_GAME_MAX_ZONE = 0.24
    TREE_GAME_TICK = 0.02
    TREE_GAME_STEP = 5
    TREE_GAME_WIGGLE_PATTERN = [0, 1, 2, 1]
    TREE_GAME_WIGGLE_STEP = 0.22
    TREE_GAME_FINALE_FRAME_TIME = 0.1

    def tree_game_frac_at(t):
        phase = (t % TREE_GAME_PERIOD) / TREE_GAME_PERIOD
        if phase < 0.5:
            return phase * 2.0
        else:
            return (1.0 - phase) * 2.0

    def tree_game_new_zone():
        progress_ratio = (store.tree_game_progress - 1) / float(TREE_GAME_WIN_FRAME - 1)
        width = TREE_GAME_MAX_ZONE - (TREE_GAME_MAX_ZONE - TREE_GAME_MIN_ZONE) * progress_ratio
        start = renpy.random.uniform(0.02, 0.98 - width)
        store.tree_game_zone = (start, start + width)

    def tree_game_frame_path(index=None):
        if index is None:
            index = store.tree_game_display_frame
        return "/mods/SkvozUlybku/cg/game_frames/frame_%04d.jpg" % index

    def tree_game_clamp(value, low, high):
        if value < low:
            return low
        if value > high:
            return high
        return value

    def tree_game_tick():
        if store.tree_game_done:
            return

        t = renpy.get_game_runtime() - store.tree_game_start_time

        phase = (t % TREE_GAME_PERIOD) / TREE_GAME_PERIOD
        store.tree_game_moving_forward = phase < 0.5
        store.tree_game_crawler_frac = tree_game_frac_at(t)

        wiggle_index = int(t / TREE_GAME_WIGGLE_STEP) % len(TREE_GAME_WIGGLE_PATTERN)
        wiggle_back = TREE_GAME_WIGGLE_PATTERN[wiggle_index]
        store.tree_game_display_frame = tree_game_clamp(store.tree_game_progress - wiggle_back, 1, TREE_GAME_TOTAL_FRAMES)

    def tree_game_on_click():
        if store.tree_game_done:
            return

        frac = store.tree_game_crawler_frac
        zone_start, zone_end = store.tree_game_zone
        hit = store.tree_game_moving_forward and (zone_start <= frac <= zone_end)

        if hit:
            store.tree_game_progress = tree_game_clamp(store.tree_game_progress + TREE_GAME_STEP, 1, TREE_GAME_WIN_FRAME)
        else:
            store.tree_game_progress = tree_game_clamp(store.tree_game_progress - TREE_GAME_STEP, 1, TREE_GAME_WIN_FRAME)

        if store.tree_game_progress >= TREE_GAME_WIN_FRAME:
            store.tree_game_done = True
            store.tree_game_display_frame = store.tree_game_progress
            renpy.end_interaction(True)
        else:
            tree_game_new_zone()
            renpy.restart_interaction()

    def tree_game_play_finale():
        renpy.show("tree_game_finale_bg", what=Solid("#000000"), zorder=9)

        for i in range(store.tree_game_progress, TREE_GAME_TOTAL_FRAMES + 1):
            renpy.show("tree_game_finale_frame", what=Transform(tree_game_frame_path(i), zoom=1.8), zorder=10)
            renpy.pause(TREE_GAME_FINALE_FRAME_TIME, hard=True)

        renpy.hide("tree_game_finale_frame")
        renpy.hide("tree_game_finale_bg")

transform tree_game_scale:
    zoom 1.8

screen tree_escape_game():
    zorder 10
    modal True

    timer TREE_GAME_TICK repeat True action Function(tree_game_tick)

    add Solid("#000000")

    add tree_game_frame_path() at tree_game_scale xalign 0.5 yalign 0.4

    text "Нажимай, только когда бегунок движется вперёд и находится в подсвеченной зоне!" xalign 0.5 ypos 860 size 34 color "#ffffff"

    fixed:
        xalign 0.5
        ypos 920
        xsize 900
        ysize 46

        add Solid("#00000080") xysize (900, 46)

        add Solid("#e0ff0090") xpos int(900 * tree_game_zone[0]) xsize int(900 * (tree_game_zone[1] - tree_game_zone[0])) ysize 46

        add Solid("#ff2222") xpos int(900 * tree_game_crawler_frac) xsize 14 ysize 46

    key "K_SPACE" action Function(tree_game_on_click)

    button:
        xysize (config.screen_width, config.screen_height)
        background None
        action Function(tree_game_on_click)

label ts_day4_tree_minigame:
    $ tree_game_progress = 1
    $ tree_game_done = False
    $ tree_game_display_frame = 1
    $ tree_game_new_zone()
    $ tree_game_start_time = renpy.get_game_runtime()
    $ tree_game_crawler_frac = 0.0
    call screen tree_escape_game
    $ tree_game_play_finale()
    return
