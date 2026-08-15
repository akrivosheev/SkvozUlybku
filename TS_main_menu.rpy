default ts_hover_joke = None
default persistent.ts_enable_censorship = True
default persistent.ts_enable_neuro = False
default ts_now_playing = None

init -10 python:

    # ЛОК. СТЕНГАЗЕТА — картинки-анекдоты, выбираются случайно при наведении
    ts_anekdot_images = [f for f in renpy.list_files() if f.startswith("mods/SkvozUlybku/cg/anekdot/")]

    def ts_pick_joke():
        if ts_anekdot_images:
            store.ts_hover_joke = renpy.random.choice(ts_anekdot_images)

    def ts_clear_joke():
        store.ts_hover_joke = None

    def ts_fit_zoom(w, h, maxw, maxh):
        # store.min/store.float могут быть перекрыты переменными базовой игры (часы/минуты),
        # поэтому берём настоящие builtin-функции напрямую
        import __builtin__
        return __builtin__.min(maxw / __builtin__.float(w), maxh / __builtin__.float(h), 1.0)

    def ts_scaled_display(im, maxw=900, maxh=680):
        # renpy.image_size() требует "чистый" im.Image и падает на тегах вида
        # "cg volleyball" (ConditionSwitch/ImageReference), поэтому размер берём
        # через реальный рендер — это работает для любого displayable
        im = renpy.displayable(im)
        render = renpy.render(im, renpy.config.screen_width, renpy.config.screen_height, 0, 0)
        w, h = render.width, render.height
        if not w or not h:
            return im
        return Transform(im, zoom=ts_fit_zoom(w, h, maxw, maxh))

    def ts_joke_display(fn, maxw=900, maxh=680):
        return ts_scaled_display(fn, maxw, maxh)

    # ГАЛЕРЕЯ — список CG мода.
    # Формат: (тег картинки, отображаемое имя). Тег — это настоящее имя image из
    # TS_init.rpy, его менять нельзя. А вот отображаемое имя (вторая строка) можно
    # свободно переписывать, а саму пару — удалить, если CG не должен быть в галерее.
    # Открытость проверяется через renpy.seen_image(тег).
    ts_gallery_cgs = [
        ("cg volleyball", "Волейбол (Славя)"),
        ("cg volleyball_un", "Волейбол (Лена)"),
        ("cg butterfly100", "Лена и бабочка"),
        ("cg un_uv_flowers", "Собирают цветы"),
        ("cg sl_sleep", "Славя спит"),
        ("cg tanec_viola", "Танец с Виолой"),
        ("cg tanec_miku", "Танец с Мику"),
        ("cg tanec_slavya", "Танец со Славей"),
        ("cg tanec_ulyana", "Танец с Ульяной"),
        ("cg tanec_lena", "Танец с Леной"),
        ("cg campfire", "Костёр"),
        ("cg mirror_kachok", "Максим у зеркала"),
        ("cg sand_castle", "Песчаный замок"),
        ("cg slavya_dush", "Славя в душе"),
        ("Slavya_and_Maxim_set_up_tent", "Славя и Максим ставят палатку"),
        ("cg rizgim", "Власть рыжим"),
        ("cg uv_end", "Семья - это главное"),
        ("cg le_end", "Как в старые добрые времена"),
        ("cg oxn_end", "С чистого листа"),
        ("cg sla_end", "Величайша тайна вселенно"),
        ("cg bad_end", "Ночной город"),
        ("cg jen_end", "Братья навек"),
    ]

    def ts_gallery_rows(cols=4):
        return [ts_gallery_cgs[i:i + cols] for i in range(0, len(ts_gallery_cgs), cols)]

    def ts_gallery_seen_count():
        return sum(1 for tag, _label in ts_gallery_cgs if renpy.seen_image(tag))

    # ПЛЕЙЛИСТ — список треков из sound/music.
    # Формат: (имя файла, отображаемое имя). Имя файла — реальный файл в
    # sound/music/, его менять нельзя. Отображаемое имя (вторая строка) можно
    # свободно переписывать, а саму пару — удалить, чтобы убрать трек из
    # плейлиста (сам файл при этом никуда не денется).
    ts_playlist_dir = "mods/SkvozUlybku/sound/music/"
    ts_playlist_names = [
        ("Believe_In_You.mp3", "Arseny St - I Will Believe In You"),
        ("Bon_Jovi_-_Ill_Be_There_For_You.mp3", "Bon Jovi — I'll Be There For You"),
        ("Break_My_Fucking_Sky.mp3", "Break My Fucking Sky - Moon"),
        ("Caravan_Palace.mp3", "Caravan Palace - Lone Digger"),
        ("Cinderella_—_Nobody's_Fool_instrumental.mp3", "Cinderella — Nobody's Fool"),
        ("dlinnohvost.mp3", "Yalamuar - Длиннохвост"),
        ("312.mp3", "Город 312 - Останусь"),
        ("Enigma.mp3", "Sergey Eybog - Enigma"),
        ("Frantic_Aerobics.mp3", "Mitch Murder - Frantic Aerobics"),
        ("jen_end.mp3", "Игорь Николаев и Игорь Крутой - Мой друг"),
        ("kachok.mp3", "Survivor - Eye Of The Tiger"),
        ("not_to_late.mp3", "Arseny St - Not To Late"),
        ("Price.mp3", "Twisted Sister - The Price"),
        ("Privet_s_bolshogo_boduna.mp3", "Дюна - Привет с Большого Бодуна"),
        ("Raznye_Ispolniteli_18_And_Life.mp3", "Skid Row - 18 And Life"),
        ("tender-moments.mp3", "Нежная Симфония"),
        ("tolko_dlya_ryzhykh.mp3", "Иванушки International - Только для рыжих"),
        ("Zacepila.mp3", "Артур Пирожков - Зацепила"),
        ("zh_theme.mp3", "Ночные снайперы - Ты город"),
    ]

    # renpy.loadable() отсеивает записи на случай, если файл переименовали/удалили
    # на диске, но забыли поправить список выше
    ts_playlist_tracks = sorted([
        (ts_playlist_dir + fn, label)
        for fn, label in ts_playlist_names
        if renpy.loadable(ts_playlist_dir + fn)
    ], key=lambda t: t[1].lower())

    def ts_play_track(fn):
        store.ts_now_playing = fn
        renpy.music.play(fn, channel="music", loop=True)

    def ts_stop_music():
        store.ts_now_playing = None
        renpy.music.stop(channel="music")

    def ts_continue_game():
        slot = renpy.newest_slot()
        if slot:
            renpy.load(slot)

    # ЦЕНЗУРА — листик поверх открытых мест
    def ts_leaf(size):
        return im.Scale("mods/SkvozUlybku/image/list.png", size, size)

    def ts_censor(base, canvas, spots, size):
        args = [canvas, (0, 0), base]
        for pos in spots:
            args.append(pos)
            args.append(ts_leaf(size))
        return Composite(*args)

    # НЕЙРО — замена CG на нейросетевые версии из cg/cg-neiro, где они есть
    def ts_cg(stem, ext, neiro_stem=None):
        orig = "mods/SkvozUlybku/cg/%s.%s" % (stem, ext)
        neiro = "mods/SkvozUlybku/cg/cg-neiro/%s.png" % (neiro_stem or stem)
        if renpy.loadable(neiro):
            return ConditionSwitch(
                "persistent.ts_enable_neuro", neiro,
                True, orig)
        return orig

screen ts_main_menu():

    add "mods/SkvozUlybku/cg/cg-neiro/menu.png" size (config.screen_width, config.screen_height)

    # Стенгазета на стене ("Вестник Совенка", верхний правый угол) — наводишь курсор, всплывает анекдот
    button:
        xpos 0.63
        ypos 0.03
        xsize 0.25
        ysize 0.28
        background None
        hovered Function(ts_pick_joke)
        unhovered Function(ts_clear_joke)
        action NullAction()

    if ts_hover_joke:
        frame:
            xalign 0.5
            yalign 0.5
            background "#000000cc"
            padding (30, 30)
            add ts_joke_display(ts_hover_joke)

    vbox:
        xpos 0.05
        yalign 0.96
        spacing 14

        textbutton "Новая игра":
            text_size 40
            text_color "#ffffff"
            text_hover_color "#e0ff00"
            action Jump("TS_prologday1_play")

        textbutton "Продолжить":
            text_size 40
            text_color "#ffffff"
            text_hover_color "#e0ff00"
            sensitive renpy.newest_slot() is not None
            action Function(ts_continue_game)

        textbutton "Галерея":
            text_size 40
            text_color "#ffffff"
            text_hover_color "#e0ff00"
            action Show("ts_gallery")

        textbutton "Плейлист":
            text_size 40
            text_color "#ffffff"
            text_hover_color "#e0ff00"
            action Show("ts_playlist")

        textbutton "Настройки":
            text_size 40
            text_color "#ffffff"
            text_hover_color "#e0ff00"
            action Show("ts_settings")

        textbutton "Выход":
            text_size 40
            text_color "#ffffff"
            text_hover_color "#e0ff00"
            action MainMenu()


screen ts_settings():
    modal True
    zorder 20

    add Solid("#000000a0")

    frame:
        xalign 0.5
        yalign 0.5
        padding (50, 50)
        background "#111111e0"

        vbox:
            spacing 22
            xsize 700

            text "Настройки" size 46 color "#ffffff" xalign 0.5

            vbox:
                spacing 10
                text "Музыка" size 30 color "#ffffff"
                bar value Preference("music volume") xsize 600

                text "Звук" size 30 color "#ffffff"
                bar value Preference("sound volume") xsize 600

                text "Скорость текста" size 30 color "#ffffff"
                bar value Preference("text speed") xsize 600

            vbox:
                spacing 12

                textbutton ("[[X]] " if _preferences.skip_unseen else "[[ ]] ") + "Пропускать прочитанное":
                    text_size 30
                    text_color "#ffffff"
                    text_hover_color "#e0ff00"
                    action Preference("skip", "toggle")

                textbutton ("[[X]] " if _preferences.afm_enable else "[[ ]] ") + "Автопрокрутка текста":
                    text_size 30
                    text_color "#ffffff"
                    text_hover_color "#e0ff00"
                    action Preference("auto-forward", "toggle")

                textbutton ("[[X]] " if _preferences.fullscreen else "[[ ]] ") + "Полноэкранный режим":
                    text_size 30
                    text_color "#ffffff"
                    text_hover_color "#e0ff00"
                    action Preference("display", "fullscreen" if not _preferences.fullscreen else "window")

                textbutton ("[[X]] " if persistent.ts_enable_censorship else "[[ ]] ") + "Включить цензуру":
                    text_size 30
                    text_color "#ffffff"
                    text_hover_color "#e0ff00"
                    action ToggleField(persistent, "ts_enable_censorship")

                textbutton ("[[X]] " if persistent.ts_enable_neuro else "[[ ]] ") + "Включить нейро":
                    text_size 30
                    text_color "#ffffff"
                    text_hover_color "#e0ff00"
                    action ToggleField(persistent, "ts_enable_neuro")

            textbutton "Назад":
                xalign 0.5
                text_size 34
                text_color "#ffffff"
                text_hover_color "#e0ff00"
                action Hide("ts_settings")


screen ts_gallery():
    modal True
    zorder 20

    add Solid("#000000e6")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1160
        ysize 720
        background "#111111f0"
        padding (30, 30)

        vbox:
            spacing 16

            text "Галерея" size 42 color "#ffffff" xalign 0.5

            $ ts_seen_count = ts_gallery_seen_count()
            $ ts_total_count = len(ts_gallery_cgs)
            text "Открыто: [ts_seen_count]/[ts_total_count]" size 22 color "#aaaaaa" xalign 0.5

            viewport:
                xsize 1100
                ysize 550
                scrollbars "vertical"
                mousewheel True
                draggable True

                vbox:
                    spacing 14
                    for row in ts_gallery_rows(4):
                        hbox:
                            spacing 14
                            for tag, label in row:
                                $ seen = renpy.seen_image(tag)
                                vbox:
                                    xsize 250
                                    spacing 6
                                    if seen:
                                        button:
                                            xysize (250, 160)
                                            background "#000000"
                                            action Show("ts_cg_viewer", tag=tag)
                                            add ts_scaled_display(tag, 250, 160) xalign 0.5 yalign 0.5
                                    else:
                                        frame:
                                            xysize (250, 160)
                                            background "#1a1a1a"
                                            text "?" size 60 color "#444444" xalign 0.5 yalign 0.5
                                    text (label if seen else "???") size 18 color "#dddddd" xalign 0.5 text_align 0.5

            textbutton "Назад":
                xalign 0.5
                text_size 34
                text_color "#ffffff"
                text_hover_color "#e0ff00"
                action Hide("ts_gallery")


screen ts_cg_viewer(tag):
    modal True
    zorder 30

    button:
        xysize (config.screen_width, config.screen_height)
        background None
        action Hide("ts_cg_viewer")

        add ts_scaled_display(tag, config.screen_width - 80, config.screen_height - 80) xalign 0.5 yalign 0.5


screen ts_playlist():
    modal True
    zorder 20

    add Solid("#000000e6")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 720
        background "#111111f0"
        padding (30, 30)

        vbox:
            spacing 16

            text "Плейлист" size 42 color "#ffffff" xalign 0.5

            viewport:
                xsize 840
                ysize 570
                scrollbars "vertical"
                mousewheel True
                draggable True

                vbox:
                    spacing 4
                    for fn, label in ts_playlist_tracks:
                        button:
                            xsize 820
                            background (Solid("#2a2a2a") if ts_now_playing == fn else None)
                            hover_background "#333333"
                            padding (14, 10)
                            action Function(ts_play_track, fn)

                            hbox:
                                spacing 10
                                text ("▶" if ts_now_playing == fn else "   ") size 20 color "#e0ff00"
                                text label size 20 color "#ffffff"

            hbox:
                xalign 0.5
                spacing 20

                textbutton "Стоп":
                    text_size 30
                    text_color "#ffffff"
                    text_hover_color "#e0ff00"
                    action Function(ts_stop_music)

                textbutton "Назад":
                    text_size 30
                    text_color "#ffffff"
                    text_hover_color "#e0ff00"
                    action Hide("ts_playlist")


label TS_prologday1:
    play music "mods/SkvozUlybku/sound/music/Enigma.mp3" fadein 1.0 loop
    call screen ts_main_menu
    return
