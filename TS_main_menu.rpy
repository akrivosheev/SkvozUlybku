default ts_hover_joke = None
default persistent.ts_enable_censorship = True
default persistent.ts_enable_neuro = False

init -10 python:

    # ЛОК. СТЕНГАЗЕТА — картинки-анекдоты, выбираются случайно при наведении
    ts_anekdot_images = [f for f in renpy.list_files() if f.startswith("mods/SkvozUlybku/cg/anekdot/")]

    def ts_pick_joke():
        if ts_anekdot_images:
            store.ts_hover_joke = renpy.random.choice(ts_anekdot_images)

    def ts_clear_joke():
        store.ts_hover_joke = None

    def ts_joke_display(fn, maxw=900, maxh=680):
        # store.min/store.float могут быть перекрыты переменными базовой игры (часы/минуты),
        # поэтому берём настоящие builtin-функции напрямую
        import __builtin__
        w, h = renpy.image_size(fn)
        scale = __builtin__.min(maxw / __builtin__.float(w), maxh / __builtin__.float(h), 1.0)
        return Transform(fn, zoom=scale)

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


label TS_prologday1:
    play music "mods/SkvozUlybku/sound/music/Enigma.mp3" fadein 1.0 loop
    call screen ts_main_menu
    return
