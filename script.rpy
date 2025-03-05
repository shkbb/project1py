# Ініціалізація
init:
    # Дефініція персонажів
    define a = Character("Алек")
    define l = Character("Ліра", color="#ff6666")
    define e = Character("Ельдар", color="#66ccff")
    define v = Character("Варта", color="#ff6666")
    # Ініціалізація глобальних змінних
    default defeated_by_snake = False
    default has_stone_file = False
    define flash = Fade(0.1, 0.2, 0.1, color="#FFFFFF")
    default click_score = 0
    define config.has_autosave = True  # Включаємо автозбереження (можна використовувати для явного збереження)
    # Не включаємо автозбереження після кожного вибору
    define config.autosave_on_choice = False

    # Завантаження ресурсів
    image bg_forest = "forest.jpg"
    image bg_village = "village.jpg"
    image bg_swamp = "swamp.jpg"
    image bg_prison = "prison.jpg"
    image bg_prison_cell = "bg_prison_cell.jpg"
    image bg_battlefield = "battlefield.jpg"
    image bg_forest_day = "bg_forest_day.jpg"
    image bg_forest_trap = "bg_forest_trap.jpg"
    image bg_forest_captors = "bg_forest_captors.jpg"
    image bg_space_station = "bg_space_station.jpg"
    image bg_bright_light = "bg_bright_light.jpg"

    image monster_snake = "monster_snake.png"
    image monster_bear = "monster_bear.png"

    image lira = "lira.png"
    image alec = "alec.png"
    image eldar = "eldar.png"

# Змінні
default has_herbs = False
default has_ore = False
default defeated_monster = False
default lira_relationship = 0
default player_health = 3
default max_health = 5
default snake_health = 3
default bear_health = 5
default potions = 3

# Екран здоров'я
screen health_bar:
    frame:
        has vbox
        text "Здоров'я"
        bar value player_health range max_health

# Екран для відображення здоров'я ворога
screen enemy_health_bar(enemy_health, max_health):
    frame:
        align (0.5, 0.2)
        vbox:
            text "Здоров'я ворога: [enemy_health]/[max_health]" size 20 color "#ff0000"
            bar value enemy_health range max_health

screen monster_health_bar(monster_health, max_health):
    frame:
        align (0.5, 0.2)
        vbox:
            text "Здоров'я монстра: [monster_health]/[max_health]" size 20 color "#ff0000"
            bar value monster_health range max_health

# Початок гри
label start:
    # Початкова сцена на космічній станції
    scene bg_space_station with fade
    play music "sci-fi_theme.mp3" loop
    a "Космічна станція 'Аврора'. Ще один день, ще один експеримент..."
    a "Що це за кристал? Ми ніколи не знаходили нічого подібного."
    
    show alec_lab_coat at center
    a "Його структура нагадує квантову матрицю, але він випромінює дивну енергію..."
    a "Давайте спробуємо активувати сенсори для детального аналізу."

    # Вибух кристала
    play sound "crystal_activation.wav"
    a "Що за?! Енергія різко зросла! Треба зупинити це!"
    play sound "explosion.wav"
    scene bg_bright_light with flash
    a "Ні, це неможливо! Що відбувається?!"    

    # Телепортація до Ілленору
    scene bg_forest with fade
    stop music fadeout 2.0
    play music "fantasy_theme.mp3" loop
    a "Де я? Це... ліс? Але це не схоже на жодну планету, яку я бачив раніше."

    # Зустріч із Ельдаром
    show alec at left
    show eldar at right
    e "Ти в Ілленорі, мандрівнику. Ми тебе знайшли непритомним у лісі."
    e "Якщо хочеш залишитися тут, доведеться допомогти нам."
    a "Добре, що потрібно зробити?"

    # Завдання
    e "Перше завдання: принеси Смарагдову лілію з болота."
    e "Друге завдання: знищ монстра, який тероризує нас."
    jump swamp_quest


# Пошук трави
label swamp_quest:
    $ autosave_game()

    scene bg_swamp with fade
    a "Це має бути те саме болото. Доведеться бути обережним."

    menu:
        "Шукати траву.":
            $ has_herbs = True
            a "Де ж вона..."
            jump swamp_snake_fight

        "Повернутися до села без трави.":
            a "Я повертаюсь із пустими руками..."
            jump village_return

# Бій зі змією

label swamp_snake_fight:
    scene bg_swamp with fade
    a "Що це за звук?"
    show monster_snake at center
    a "Болотяна змія! Доведеться битися."

    menu:
        "Залишитися і битися.":
            $ player_health = 3
            $ snake_health = 3
            $ potions = 3
            $ monster_skips_turn = False
            $ player_dodged_last_turn = False

            show screen player_health_bar
            show screen enemy_health_bar(enemy_health=snake_health, max_health=3)

            while snake_health > 0 and player_health > 0:
                # Оновлюємо екран після кожного ходу
                show screen enemy_health_bar(enemy_health=snake_health, max_health=3)
                show screen player_health_bar

                $ renpy.restart_interaction()  # Оновлення екрану ворога
                menu:
                    "Ухилитися.": 
                        if renpy.random.randint(1, 100) <= 95:
                            $ player_dodged_last_turn = True
                            a "Я успішно ухилився!"
                        else:
                            $ player_health -= 1
                            $ player_dodged_last_turn = False
                            a "Змія мене вдарила!"
                    "Атакувати.": 
                        if renpy.random.randint(1, 10) > 3:
                            $ snake_health -= 1
                            $ player_dodged_last_turn = False
                            a "Отримуй!"
                        else:
                            $ player_dodged_last_turn = False
                            a "Я промахнувся!"
                    "Використати зілля для відновлення здоров'я." if potions > 0 and player_dodged_last_turn:
                        $ potions -= 1
                        $ player_health = min(player_health + 1, 3)
                        $ monster_skips_turn = True
                        $ player_dodged_last_turn = False
                        a "Я використав зілля. Здоров'я відновлено!"

                if snake_health > 0 and not monster_skips_turn:
                    if renpy.random.randint(1, 2) == 1:
                        $ player_health -= 1
                        a "Змія мене вдарила!"
                    else:
                        a "Змія промахнулась!"
                elif monster_skips_turn:
                    $ monster_skips_turn = False
                    a "Змія пропустила хід!"

            hide screen player_health_bar
            hide screen enemy_health_bar

            if player_health <= 0:
                a "Мене перемогли... Мені треба повернутися до села."
                $ defeated_by_snake = True
                jump village_return
            else:
                a "Я переміг змію!"
                $ defeated_by_snake = False
                jump village_return
        "Піти геть.":
            a "Я не можу битися з цим монстром. Треба повернутися до села."
            $ defeated_by_snake = True
            jump village_return

label village_return:
    $ autosave_game()

    if defeated_by_snake:
        e "Без трави, для тебе є інше завдання."
        jump mountain_quest
    elif has_herbs:
        e "Чудово, ти виконав завдання. Це нам допоможе."
        a "Я радий, що це було корисно."
        e "Тоді ти можеш відправлятися на наступне завдання."
        e "Тобі потрібно розібратися з монстром, який тероризує нас."
        jump bear_quest
    else:
        e "Без трави, для тебе є інше завдання."
        jump mountain_quest  # Переходимо до нового квесту

# Новий квест: пошук копалин
label mountain_quest:
    scene bg_forest with fade
    e "Якщо ти не зміг знайти Смарагдову лілію, є інше завдання."
    e "Ми потребуємо рідкісного мінералу — Вогняного кварцу, який є лише в горах."
    
    scene bg_forest
    a "Гори, здається, в цьому напрямку. Треба бути обережним."
    
    $ ore_collected = 0  # Кількість зібраної руди
    $ attempts_left = 3  # Лічильник спроб у поточному родовищі

    label ore_start:
        menu:
            "Шукати руду.":
                $ attempts_left = 3  # Оновлюємо спроби для нового родовища
                a "Знайшов нове родовище! Потрібно спробувати."
                jump ore_mining
            "Піти геть.":
                a "Я залишаю гори з пустими руками."
                jump village_return_empty

    label ore_mining:
        show screen mining_progress

        "Ось вони, кварцеві уламки! Що робити далі?"

        menu:
            "Добути руду.":
                $ attempts_left -= 1
                if renpy.random.randint(1, 100) <= 60:
                    $ ore_collected += 1
                    a "Я успішно здобув шматок руди!"
                else:
                    a "Руда була занадто крихка і розпалася на дрібні уламки."

                if ore_collected >= 5:
                    hide screen mining_progress
                    a "Я зібрав достатньо руди. Час повертатися."
                    jump village_return_with_ore
                elif attempts_left <= 0:
                    a "Це родовище вичерпано. Треба знайти інше."
                    hide screen mining_progress
                    jump ore_start
                else:
                    jump ore_mining
            
            "Піти геть.":
                hide screen mining_progress
                a "Я залишаю гори з пустими руками."
                jump village_return_empty
label village_return_empty:
e "Ти не виконав жодного нашого завдання."
e "Ми більше не можемо утримувати тебе за безцінь."
jump game_over

# Відображення прогресу збору руди
screen mining_progress:
    frame:
        align (0.5, 0.05)
        vbox:
            text "Зібрано руди: [ore_collected]/5" size 20 color "#ffcc00"
            text "Спроб залишилось: [attempts_left]" size 20 color "#ffcccc"

# Повернення до села після гір
label village_return_with_ore:
    e "Ти молодець, це допоможе нашому поселенню."
    e "Тепер ти можеш переходити для вбивства монстра для нас."
    e "Вдачі, Алек."
    jump bear_quest

# Бій із ведмедем
label bear_quest:
    $ autosave_game()
    scene bg_forest with fade
    a "Де ж цей монстр?"

    show monster_bear at center
    a "Ось і він! Він величезний!"

    show screen player_health_bar
    show screen enemy_health_bar(enemy_health=bear_health, max_health=5)

    $ player_health = 5
    $ bear_health = 5
    $ potions = 3
    $ monster_skips_turn = False
    $ player_dodged_last_turn = False

    while bear_health > 0 and player_health > 0:
        # Оновлення екрану здоров'я після кожної дії
        show screen enemy_health_bar(enemy_health=bear_health, max_health=5)
        show screen player_health_bar

        menu:
            "Ухилитися.":
                if renpy.random.randint(1, 100) <= 95:
                    $ player_dodged_last_turn = True
                    a "Я успішно ухилився!"
                else:
                    $ player_health -= 1
                    $ player_dodged_last_turn = False
                    a "Ведмідь мене вдарив!"
            "Атакувати спину.":
                if renpy.random.randint(1, 10) > 3:
                    $ bear_health -= 1
                    $ player_dodged_last_turn = False
                    a "Відмінний удар!"
                else:
                    $ player_dodged_last_turn = False
                    a "Я промахнувся!"
            "Використати зілля для відновлення здоров'я." if potions > 0 and player_dodged_last_turn:
                $ potions -= 1
                $ player_health = min(player_health + 1, 5)
                $ monster_skips_turn = True
                $ player_dodged_last_turn = False
                a "Я використав зілля. Здоров'я відновлено!"

        if bear_health > 0 and not monster_skips_turn:
            if renpy.random.randint(1, 2) == 1:
                $ player_health -= 1
                a "Ведмідь мене вдарив!"
            else:
                a "Його удар пройшов повз!"
        elif monster_skips_turn:
            $ monster_skips_turn = False
            a "Ведмідь пропустив хід!"

    hide screen player_health_bar
    hide screen enemy_health_bar

    if player_health <= 0:
        a "Мене перемогли..."
        jump game_over
    else:
        a "Монстр переможений. Треба зняти шкуру як доказ."
        $ defeated_monster = True
        jump village_return_with_pelt

# Екран для відображення здоров'я гравця
screen player_health_bar:
    frame:
        align (0.5, 0.1)
        vbox:
            text "Здоров'я гравця" size 20 color "#ffffff"
            bar value player_health range max_health

# Екран для відображення здоров'я ворога
screen enemy_health_bar(enemy_health, max_health):
    frame:
        align (0.5, 0.2)
        vbox:
            text "Здоров'я ворога" size 20 color "#ff0000"
            bar value enemy_health range max_health

# Подальші сцени
# (Продовження без змін)
label village_return_with_pelt:
    scene bg_village with fade
    e "Це шкура монстра? Неймовірно, ти його переміг!"
    a "Це було нелегко, але я впорався."
    e "Молодець. Тепер відпочинь, а потім ми поговоримо про наступні завдання."
    a "Дякую. Піду трохи прогуляюся."
    jump rest_and_trap

# Лейбл для початку прогулянки
label rest_and_trap:
    $ autosave_game()
    scene bg_forest_day with fade
    a "Свіже повітря... Тут так тихо і спокійно."
    
    # Перевірка, чи гравець вже знайшов напильник
    menu:
        "Дослідити галявину.":  # Гравець досліджує галявину
            if not store.has_stone_file:
                a "Цікаво, що тут є..."
                $ store.has_stone_file = True  # Гравець отримує кам'яний напильник
                a "Я знайшов кам'яний напильник! Це може бути корисно."
                jump rest_and_trap
            else:
                a "Я вже досліджував цю галявину. Тут більше нічого немає."
                jump rest_and_trap

        "Піти глибше в ліс.":  # Гравець іде в ліс
            a "Що це за дивний звук? Краще перевірю."

    a "Що за..."
    scene bg_forest_trap with fade
    play sound "sfx_trap.mp3"  # Звук пастки
    a "Це пастка! Я потрапив у сітку!"

    a "Треба спробувати вибратися, але вона дуже міцна... Хтось іде сюди."
    play sound "sfx_steps.mp3"  # Звук кроків

    scene bg_forest_captors with fade
    v "Ага, у нас тут гість. Гляньте, як зручно він потрапив у нашу пастку."
    a "Хто ви такі? Що вам потрібно?"
    v "Питання тут ставимо ми. Забирайте його. Нехай трохи подумає над своєю поведінкою."

    # Перехід до сцени з в'язницею
    scene bg_prison with fade
    a "Де я? Похмуро, холодно... Виглядає як в'язниця."
    jump prison_sequence

# Ліра: вибір допомоги
label prison_sequence:
    scene bg_prison with fade
    l "Вітаю Алек."
    a "Хто ви?"
    l "Ми - Нічні Скьорґи, наша мета знищити всю магію в цьому світі."
    l "Ми стежили за тобою, відтоді, коли ти потрапив у цей світ."
    a "Що?.."
    l "Ми знаємо, що ти не з цього світу."
    l "І ми можемо допомогти тобі повернутися назад."
    l "Але при умові, якщо ти допоможеш нам."
    a "Що ви хочете вам потрібно?"
    l "Ти можеш стати частиною мого світу, якщо знищиш магів."
    l "А також, ти дуже милий хлопчина. Можливо, якщо б ти обрав мене, в нас могло б щось вийти у майбутньому)."
    a "*Вона дійсно виглядає прекрасною. Вона теж мені подобається.."
    a "*Але чи можу я пожертвувати Ельдаром, який мені допоміг..*"
    
    $ autosave_game()

    menu:
        "Допомогти Лірі.":  # Якщо гравець вибирає допомогу
            $ lira_relationship += 1
            jump lira_betrayal_path
        "Відмовитися співпрацювати.":  # Якщо гравець відмовляється співпрацювати
            $ lira_relationship -= 1
            l "Тоді ти залишишся тут назавжди."
            jump escape_sequence

# Шлях співпраці з Лірою
# Продовження лейблу lira_betrayal_path
label lira_betrayal_path:
    l "Ми почнемо атаку завтра."
    menu:
        "Спробувати втекти.":  # Гравець обманює Ліру і намагається втекти
            a "Я не можу їй довіряти."
            jump escape_escape_sequence
        "Піти на співпрацю.":  # Якщо гравець реально вибирає співпрацю
            jump attack_mages

label escape_escape_sequence:
    scene bg_prison with fade
    a "*Я спробую втекти. Охоронець тримає мене за руку.*"
    
    menu:
        "Вдарити охоронця, який мене тримає.":  # Вибір вдарити охоронця
            $ chance = random.randint(1, 100)  # Генерація випадкового числа для шансу
            if chance <= 2:  # Якщо шанс 2%
                jump escape_success1  # Успішна втеча
            else:
                $ attempted_escape = True  # Встановлюємо, що гравець намагався втекти
                jump escape_fail_bnf  # Неуспішна втеча
        "Скоритись.":  # Вибір скоритися
            a "*Я не хочу ризикувати, краще підкоритися її волі.*"
            jump escape_fail  # У будь-якому випадку, якщо гравець скоряється, він не втече

# Неуспішна втеча (98% шанс)
label escape_fail_bnf:
    a "Я не зміг втекти. Охоронець швидко мене зупинив."
    a "Чорт! Я зазнав поразки."
    menu:
        "Спробувати втекти знову.":  # Якщо гравець хоче спробувати втекти знову
            jump escape_escape_sequence  # Повертаємо до спроби втечі
        "Піти на співпрацю.":  # Якщо гравець хоче здатися
            if attempted_escape:  # Якщо гравець вже намагався втекти
                l "Ти вже намагався втекти і не зміг. Тепер не маєш вибору."
            jump lira_betrayal_path  # Переходимо до шляху співпраці з Лірою

# Нова сцена з спробою втечі
label escape_attempt:
    scene bg_prison with fade
    a "Моя єдина можливість — втекти прямо зараз."
    
    # Додаємо екран для втечі
    call screen escape_escape_screen

    # Перевірка чи втік гравець чи був спійманий
    if click_score >= 15:  # Якщо гравець успішно втік
        $ click_score = 0  # Скидаємо лічильник після втечі
        a "Я майже втік!"
        jump escape_success  # Перехід на успішну втечу
    else:
        a "О ні, мене зловили!"
        jump escape_fail  # Гравець не втік, переходить в escape_fail

init python:
    import random  # Додаємо імпорт бібліотеки random

# Логіка для успіху втечі
label escape_success:
    a "Я нарешті на волі!"
    l "Ти справді думав, що в тебе є шанс?"
    jump escape_fail  # Попри втечу, його все одно ловлять

# Логіка для невдачі
label escape_fail:
    a "*Я не зміг втекти...*"
    l "Ти залишишся тут назавжди."
    jump game_over

label escape_fail1:
    a "Я не зміг втекти..."
    jump lira_betrayal_path


# Сцена з боєм
label attack_mages:
    scene bg_battlefield
    a "Ось і поселення..."
    e "Чому ти це робиш?"
    a "Пробач мене, Ельдар."
    e "Ти зрадив нас..."

    # Ініціалізація змінних для інтерактиву
    $ click_score = 0  # Лічильник очків
    $ timer_active = True  # Таймер активний

    # Виклик екрана
    show screen click_fast_challenge1

    # Чекати, поки гравець не досягне 15 кліків
    while click_score < 15:
        $ renpy.pause(0.1)  # Пауза, щоб дозволити таймеру працювати
        # Виходить з циклу, коли кліків достатньо
    $ renpy.hide_screen("click_fast_challenge")  # Закриваємо екран після досягнення 15 кліків

    # Перевірка успіху
    if click_score >= 15:
        l "Дякую за твою допомогу. Але тепер ти мені не потрібен."
        l "Прощавай."
        a "Що?.."
        a "*Вона мене пронизала..."
    else:
        l "Ти виявився занадто слабким..."
        jump game_over

# Функції для взаємодії
init python:
    # Функція збільшення кліків
    def increase_click_score():
        if renpy.store.click_score < 15:
            renpy.store.click_score += 1

    # Функція зменшення кліків
    def decrease_click_score():
        if renpy.store.click_score > 0 and renpy.store.click_score < 15:
            renpy.store.click_score -= 1

# Екран інтерактиву
screen click_fast_challenge1:
    frame:
        align (0.5, 0.5)
        vbox:
            spacing 20
            # Інструкція
            text "Натискайте на кнопку якомога швидше, щоб добити Ельдара." xalign 0.5

            # Кнопка для кліків
            textbutton "Натискай" action Function(increase_click_score) xalign 0.5

            # Лічильник кліків
            text "[click_score]/15 кліків" xalign 0.5

    # Таймер, що віднімає 1 бал кожну секунду
    timer 1.0 repeat True action Function(decrease_click_score)

# Втеча з тюрми, варіанти втечі
label escape_sequence:
    $ autosave_game()
    scene bg_prison_cell with fade
    a "Я тут, але треба якось вибратися..."

    menu:
        "Спробувати зламати кодовий замок.":  # Механіка кодового замка
            a "На дверях кодовий замок. Треба знайти код і спробувати його ввести..."
            jump code_lock_mechanic

        "Спробувати домовитись зі сторожем.":  # Домовитись зі сторожем
            a "Я намагаюсь домовитись, але він не хоче слухати..."
            jump escape_fail

        "Спробувати розпиляти ґрати кам'яним напильником.":  # Розпилювання ґрат
            if store.has_stone_file:
                a "Я використовую кам'яний напильник, щоб розпиляти ґрати."
                $ has_escaped = True
                jump escape_success1
            else:
                a "У мене немає інструментів для цього."
                jump escape_fail

init python:
    def check_code():
        entered = renpy.store.entered_code.strip()
        if entered == renpy.store.correct_code:
            renpy.store.has_escaped = True
        else:
            renpy.store.has_escaped = False

    def limit_input_length(var_name, **kwargs):
        # Обрізаємо довжину введеного тексту до 4 символів
        if len(renpy.store.entered_code) > 4:
            renpy.store.entered_code = renpy.store.entered_code[:4]

# Механіка кодового замка
label code_lock_mechanic:
    a "Я дивлюсь на кодовий замок. Потрібно ввести 4-значний код."
    $ correct_code = "2745"  # Правильний код
    $ entered_code = ""  # Код, який вводить гравець

    screen code_lock_screen:
        frame:
            align (0.5, 0.5)
            vbox:
                text "Введіть 4-значний код:"
                input value VariableInputValue("entered_code") allow "0123456789" changed limit_input_length  # Поле вводу
                textbutton "Спробувати код" action [Function(check_code), Return()]

    call screen code_lock_screen

    if has_escaped:
        jump escape_success1
    else:
        a "Код неправильний. Спробуйте ще раз."
        jump code_lock_mechanic

    return

    # Перевіряємо, чи правильний код
    if entered_code == correct_code:
        a "Замок клацнув! Двері відчинені!"
        jump escape_success1
    else:
        a "Код неправильний. Мабуть, треба спробувати інший..."
        jump escape_fail

label escape_success1:
    a "Я втік! Тепер треба швидко йти далі."
    "Герой вибігає з замку Нічних Скьорґів і бачить, що до воріт вже прийшло все поселення магів. Починається масштабна битва."
    "Він прибігає на поле бою, де його чекає Ліра."
    
    # Переходить до дуелі
    jump duel_with_lyra

# Функції для взаємодії
init python:
    import random

    class ClickChallenge:
        def __init__(self):
            self.click_score = 0
            self.final_click_score = 0
            self.max_clicks = 15

        def increase(self):
            # Збільшуємо кількість кліків, коли гравець натискає кнопку
            if self.click_score < self.max_clicks:
                self.click_score += 1

        def decrease(self):
            # Зменшуємо кількість кліків, якщо гравець не натискає протягом секунди
            if self.click_score > 0:
                self.click_score -= 1

        def store(self):
            self.final_click_score = self.click_score


    click_challenge = ClickChallenge()

    # Функція для вибору дії Ліри
    def lyra_action(player_hp, lyra_hp):
        # Ліра атакує частіше, особливо на початку
        if lyra_hp > 50:
            if random.random() < 0.7:  # 70% шанс атаки
                return "attack"
            else:
                return random.choice(["defense", "provoke"])  # Вибір між захистом і провокацією
        
        # Якщо здоров'я Ліри менше 30, вона вибирає захист
        if lyra_hp <= 30:
            return "defense"  # Ліра намагається захищатися, коли її здоров'я низьке

        # Ліра атакує, якщо гравець не вибирає захист
        if player_hp > 50:
            if random.random() < 0.7:  # 70% шанс атаки
                return "attack"
            else:
                return random.choice(["defense", "provoke"])

        # Якщо здоров'я гравця низьке, Ліра може також атакувати для фінального удару
        if player_hp <= 30:
            if random.random() < 0.7:  # 70% шанс атаки
                return "attack"
            else:
                return random.choice(["defense", "provoke"])

        # Якщо все інше не спрацьовує, Ліра може вибрати провокацію
        return random.choice(["attack", "provoke"])  # Або атака, або провокація, щоб дестабілізувати гравця

init python:
    # Створюємо клас для гравця, який буде зберігати інформацію про зілля
    class Player:
        def __init__(self):
            self.health_potion = 3  # Початково 3 зілля

    # Створюємо екземпляр гравця
    player = Player()

# Екран інтерактиву
screen click_fast_challenge:
    frame:
        align (0.5, 0.5)
        vbox:
            spacing 20
            text "Натискайте на кнопку якомога швидше, щоб завдати удар Лірі!" xalign 0.5
            textbutton "Натискай" action Function(click_challenge.increase) xalign 0.5
            text "[click_challenge.click_score]/15 кліків" xalign 0.5

    # Таймер для зменшення кліків кожну секунду
    timer 1.0 repeat True action Function(click_challenge.decrease)

    # Завершення міні-гри, коли досягнуто 15 кліків
    if click_challenge.click_score >= 15:
        timer 0.1 action Return(True)  # Повертаємо True, якщо досягли 15 кліків

    # Завершення міні-гри через певний час (наприклад, 10 секунд)
    timer 10.0 action Return(False)  # Повертаємо False, якщо час вийшов


# Дуель з Лірою
label duel_with_lyra:
    $ autosave_game()
    # Початкові параметри
    $ player_hp = 100
    $ lyra_hp = 100
    $ attack_damage = 20
    $ defense_block = 10
    $ provoke_effect = 10
    $ duel_result = None  # Змінна для зберігання результату дуелі

    while duel_result is None:  # Цикл дуелі до завершення
        # Відображення стану здоров'я
        show screen health_bars(player_hp, lyra_hp)

        # Виведення стану здоров'я
        "Твоє здоров'я: [player_hp]. Здоров'я Ліри: [lyra_hp]."
        "Вибирай свою дію!"

        # Гравець обирає дію через меню
        $ player_choice = renpy.display_menu([  # Вибір між атакою, захистом і провокацією
            ("Атака", "attack"),
            ("Захист", "defense"),
            ("Провокація", "provoke")
        ])

        # Ліра вибирає свою стратегію, виходячи зі здоров'я
        $ lyra_choice = lyra_action(player_hp, lyra_hp)

        if player_choice == "attack":
            "Ти намагаєшся завдати потужного удару!"
            $ click_challenge.click_score = 0
            call screen click_fast_challenge

            if click_challenge.click_score >= 15:
                "Твій удар успішно досяг Ліри!"
                $ lyra_hp -= 10
            else:
                "Тобі не вдалося завдати сильного удару. Ліра сміється!"

        elif player_choice == "defense":
            if lyra_choice == "attack":
                "Ти частково захистився від атаки Ліри!"
                $ player_hp -= max(attack_damage - defense_block, 0)
            else:
                "Твій захист не знадобився цього разу."

            # Якщо гравець вибрав "Захист", даємо можливість використати зілля
            if player.health_potion > 0:
                $ potion_choice = renpy.display_menu([  # Варіанти використання зілля
                    ("Використати зілля", "use_potion"),
                    ("Продовжити", "continue")
                ])

                if potion_choice == "use_potion":
                    "Ти використовуєш зілля для відновлення здоров'я!"
                    $ player_hp += 20  # Відновлюємо 20 здоров'я
                    $ player.health_potion -= 1  # Зменшуємо кількість зілля
                    if player_hp > 100:  # Обмежуємо максимальне здоров'я
                        $ player_hp = 100
                else:
                    "Ти вирішуєш не використовувати зілля."

        elif player_choice == "provoke":
            if lyra_choice == "provoke":
                "Ви обидва намагаєтесь вивести одне одного з рівноваги, але це не діє!"
            elif lyra_choice == "attack":
                "Ліра атакує, але провокація трохи ослабила її!"
                $ lyra_hp -= provoke_effect
            else:
                "Твоя провокація діє, Ліра здається роздратованою!"
                $ lyra_hp -= provoke_effect

        # Ліра атакує гравця, якщо її дія — атака
        if lyra_choice == "attack" and player_choice != "defense":
            "Ліра завдала тобі удару!"
            $ player_hp -= attack_damage

        # Перевірка результату дуелі (перемога чи поразка)
        if player_hp <= 0:
            $ duel_result = "defeat"  # Якщо гравець програв
        elif lyra_hp <= 0:
            $ duel_result = "victory"  # Якщо Ліра програла

    # Завершення дуелі
    hide screen health_bars

    if duel_result == "victory":
        "Ти переміг Ліру!"
        jump post_duel_victory
    else:
        "Ти програв дуель..."
        jump game_lose
# Оновлений екран для хелсбарів
screen health_bars(player_hp, lyra_hp):
    frame:
        align (0.5, 0.1)
        vbox:
            spacing 10
            hbox:
                text "Гравець: [player_hp]" xalign 0.0
                bar value player_hp range 100 xalign 0.0
            hbox:
                text "Ліра: [lyra_hp]" xalign 0.0
                bar value lyra_hp range 100 xalign 0.0

label post_duel_victory:
    $ autosave_game()
    "Після перемоги над Лірою ти знову опиняєшся перед складним вибором..."
    "Вона впала на коліна, зовсім беззахисна."
    l "Ну давай, візьми та добий мене."
    a "Що ж мені робити..."

    menu:
        "Добити Ліру":
            $ lyra_alive = False
            "Ти підіймаєш меч і робиш вирішальний удар."
            l "Ха... навіть ти... слабкий, як і всі інші..."
            "Її голос зникає, коли життя залишає її тіло."
            "Ти витираєш меч і повертаєшся в поселення магів."
            jump victory_celebration

        "Залишити її живою":
            $ lyra_alive = True
            "Ти опускаєш меч і відходиш убік."
            a "Це не мій шлях."
            "Ти повертаєшся до неї спиною і починаєш йти геть."
            "Раптом ти відчуваєш різкий біль у спині."
            "Обернувшись, ти бачиш Ліру з кров'ю на мечі, що пронизав тебе."
            l "Довіряти ворогу - твоя помилка."
            "Твій зір стає розмитим, і темрява поглинає тебе..."
            return

label victory_celebration:
    "Ти повертаєшся до поселення магів, де тебе зустрічають як героя."
    "Вечір присвячений святкуванню перемоги над Нічними Скьорґами."
    "Ти дивишся на вогонь, відчуваючи як суміш радості і втрати наповнює твоє серце."
    "Можливо, завтра принесе нові випробування, але сьогодні — це твоя перемога."
    return

label game_lose:
    "Це кінець твоєї подорожі. Гра завершена."
    jump game_over

# 1. Функція для автозбереження
init python:
    def autosave_game():
        """
        Зберігає гру як автозбереження.
        """
        renpy.save("autosave")  # Видалено необґрунтований параметр "name"
        renpy.log("Автозбереження виконано.")

# 2. Екран Game Over
screen game_over_screen:
    modal True
    zorder 100

    vbox:
        spacing 20
        align (0.5, 0.5)

        # Текст Game Over
        text "Гра закінчена" size 40 color "#FFFFFF" xalign 0.5

        # Кнопка для головного меню
        textbutton "Головне меню":
            action MainMenu()

        # Кнопка для завантаження автозбереження
        textbutton "Завантажити останнє збереження":
            action Call("load_game")

        # Кнопка виходу з гри
        textbutton "Вихід з гри":
            action Quit()

# 3. Завантаження автозбереження
label load_game:
    if renpy.has_autosave():
        $ renpy.load("autosave")
        return
    else:
        "Автозбереження відсутнє."
        return

# 4. Мітка програшу та виклик екрану Game Over
label game_over:
    # Логіка, яку потрібно виконати перед екраном
    python:
        renpy.log("Гравець програв. Відображаємо екран Game Over.")

    # Показуємо екран Game Over
    show screen game_over_screen
    return
