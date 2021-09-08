import pygame, math, time, threading, random, json, os

pygame.init()

pygame.display.init()

WIDTH, HEIGHT = 1000, 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clicky Clicker Fusion Reactor")

nova = r'./Assets/NovaSquare-Regular.ttf'
nuclear = pygame.image.load(r'./Assets/nuclear symbol.png')

joules = 0
value = 1
per_second = 0

items = {
    1: {"name": "Harder Workers", "price": 100, "base_price": 100, "owned": 0, "value": 1,
        "info": "1 Joule per second"},
    2: {"name": "Faster Generators", "price": 1200, "base_price": 1200, "owned": 0, "value": 8,
        "info": "8 Joules per second"},
    3: {"name": "Better Haizi", "price": 13000, "base_price": 13000, "owned": 0, "value": 40,
        "info": "40 Joules per second"},
    4: {"name": "Yang Wang", "price": 121000, "base_price": 121000, "owned": 0, "value": 235,
        "info": "235 Joules per second"},
    5: {"name": "Slaves", "price": 980000, "base_price": 980000, "owned": 0, "value": 1000,
        "info": "1 Kiljoule per second"},
    6: {"name": "Raj", "price": 10000000, "base_price": 10000000, "owned": 0, "value": 4500,
        "info": "4.5 Kilojoules per second"},
    7: {"name": "Haizi Power", "price": 140000000, "base_price": 140000000, "owned": 0, "value": 50000,
        "info": "50 Kilojoules per second"},
    8: {"name": "Nimama", "price": 9223372036854775807, "base_price": 9223372036854775807, "owned": 0,
        "value": 2147483647, "info": "2147483647 Joules per second"}
}

# [location, velocity, timer]
click_particles = []
background_particles = []

clock = pygame.time.Clock()

offset = 0

version = 'b1.5'


def save():
    global joules, value, per_second, items

    state = open(r'./Assets/autosave.txt', "w")

    t = threading.Timer
    t.daemon = True
    t(300, save).start()  # Saves every 5 minutes

    values = {
        'joules': joules, "value": value, 'per_second': per_second, 'items': items, 'version': version
    }
    state.write(json.dumps(values))
    state.close()
    print('Saved')


def load():
    global joules, value, per_second, items

    if os.path.isfile('./Assets/autosave.txt'):
        state = open(r'./Assets/autosave.txt', 'r')
        autosave = json.loads(state.read())
        joules = autosave['joules']
        value = autosave['value']
        per_second = autosave['per_second']
        items = autosave['items']


def background():
    background_particles.append(
        [[300, 400], [random.randint(-50, 50) / 50, random.randint(-50, 50) / 50], random.randint(3, 18)])
    for i, v in sorted(enumerate(background_particles), reverse=True):
        v[0][0] += v[1][0] * 2
        v[0][1] += v[1][1] * 2
        v[2] -= 0.01
        if not in_circle(v[0][0], v[0][1], 300, 400, 190):  # Only draw if it's not covered by the button
            pygame.draw.circle(WINDOW, (0, 50 + v[2] * 11, 0), (v[0][0], v[0][1]), v[2])
        if v[2] <= 0:
            background_particles.remove(v)
        if -10 <= v[0][0] >= WIDTH - 415 or -10 <= v[0][1] >= HEIGHT + 10:  # If it goes off the screen
            background_particles.remove(v)


def get_suffix(num):
    suffixes = ['J', 'kJ', 'MJ', 'GJ', 'TJ', 'PJ', 'EJ', 'ZJ', 'YJ']
    for i in range(len(suffixes)):
        if 10 ** (i * 3) <= num <= 10 ** ((i + 1) * 3):
            return str(round(math.floor(num) / 10 ** (i * 3), 3)) + suffixes[i]
        elif num == 0:
            return '0J'


def increment_joules():
    global joules, per_second
    while True:
        joules += per_second * 1 / 60
        time.sleep(1 / 60)


def in_circle(x, y, centre_x, centre_y, radius):
    distance = (centre_x - x) * (centre_x - x) + (centre_y - y) * (centre_y - y)
    if distance < radius * radius:
        return True
    else:
        return False


def draw_text(text, font, colour, x, y, pos="center", alpha=255):
    text_obj = font.render(text, 1, colour)
    text_obj.set_alpha(alpha)
    text_rect = text_obj.get_rect()
    setattr(text_rect, pos, (x, y))
    WINDOW.blit(text_obj, text_rect)


def credits():
    while True:
        WINDOW.fill((31, 38, 64))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        left_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    left_click = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        pygame.display.update()


def settings():
    left_click = False

    while True:
        WINDOW.fill((31, 38, 64))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        draw_text('Settings', pygame.font.Font(nova, 100), (255, 255, 255), WIDTH // 2, 75)

        delete_button = pygame.Rect(WIDTH // 2 - 200, 150, 400, 100)
        pygame.draw.rect(WINDOW, (158, 62, 62), delete_button, 0, 3)
        draw_text('Clear Progress', pygame.font.Font(nova, 50), (255, 255, 255), WIDTH // 2, 200)

        if left_click:
            if delete_button.collidepoint(mouse_x, mouse_y):
                os.remove(r'./Assets/autosave.txt')
                load()

        left_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    left_click = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        pygame.display.update()


def game():
    global joules, value, per_second, offset

    left_click = False
    t1 = threading.Thread(target=increment_joules, args=[])
    t1.daemon = True
    t1.start()

    load()
    save()

    update_store = True

    old_store_item = 0
    old_mouse_x = 0
    can_afford = []
    for _ in range(len(items) + 1):
        can_afford.append(False)

    while True:
        clock.tick(60)
        WINDOW.fill((31, 38, 64), (0, 0, WIDTH - 400, HEIGHT))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        background()

        value = math.floor(1 + per_second / 10)

        stats = pygame.Surface((WIDTH - 400, 125), pygame.SRCALPHA)
        stats.fill((0, 0, 0, 127))
        WINDOW.blit(stats, (0, 0))
        WINDOW.blit(nuclear, ((WIDTH - 400) // 2 - 200, 200))
        draw_text(get_suffix(joules), pygame.font.Font(nova, 80), (255, 255, 255), (WIDTH - 400) // 2, 50)
        draw_text(str(get_suffix(per_second)) + ' per second', pygame.font.Font(nova, 40), (255, 255, 255),
                  (WIDTH - 400) // 2, 105)
        draw_text(str(int(clock.get_fps())) + ' FPS', pygame.font.Font(nova, 20), (255, 255, 255), 10, 10, "topleft")
        draw_text(version, pygame.font.Font(nova, 20), (255, 255, 255), 10, HEIGHT - 30, "topleft")

        menu = pygame.Rect(WIDTH - 400, 0, 400, HEIGHT)

        # if 965 > mouse_x > 935:
        #     update_store = True

        current_store_item = math.floor((mouse_y - offset + 125 - 50) / 100) - 1

        if mouse_x > WIDTH - 400 and current_store_item != old_store_item:
            update_store = True

        if mouse_x < WIDTH - 400 <= old_mouse_x:
            update_store = True

        if mouse_x > WIDTH - 400 >= old_mouse_x:
            update_store = True

        old_mouse_x = mouse_x
        old_store_item = current_store_item

        for i in items:
            rect_y = 125 + (int(i) - 1) * 100 + offset
            if joules < items[i]["price"]:
                if can_afford[int(i)] != False:
                    update_store = True
                    can_afford[int(i)] = False
            else:
                if can_afford[int(i)] != True:
                    update_store = True
                    can_afford[int(i)] = True
            if in_circle(mouse_x, mouse_y, 950, (rect_y + 50), 15):
                info_rect = pygame.Rect(150, rect_y, 450, 100)
                pygame.draw.rect(WINDOW, (49, 51, 56), info_rect)
                pygame.draw.rect(WINDOW, (255, 255, 255), info_rect, 2)
                draw_text(items[i]["info"], pygame.font.Font(nova, 30), (255, 255, 255), 175, rect_y + 20, "topleft")
                draw_text('You have ' + str(items[i]["owned"]) + " " + str(items[i]["name"]),
                          pygame.font.Font(nova, 25), (128, 128, 128), 175,
                          rect_y + 55, "topleft")

            if left_click:
                if mouse_x > WIDTH - 400 and current_store_item == int(i):
                    update_store = True
                    if joules - items[i]["price"] >= 0:
                        joules -= items[i]["price"]
                        items[i]["owned"] += 1
                        per_second += items[i]["value"]
                        items[i]["price"] = math.floor(items[i]["base_price"] * (1.05 ** items[i]["owned"]))

        if update_store:
            pygame.draw.rect(WINDOW, (49, 51, 56), menu)
            draw_text('Store', pygame.font.Font(nova, 80), (255, 255, 255), 800, 50)
            for i in items:
                rect_y = 125 + (int(i) - 1) * 100 + offset
                item_rect = pygame.Rect(WIDTH - 400, rect_y, 400, 100)
                pygame.draw.rect(WINDOW, (84, 85, 87), item_rect)
                if mouse_x > WIDTH - 400 and current_store_item == int(i):
                    pygame.draw.rect(WINDOW, (125, 125, 125), item_rect)
                pygame.draw.rect(WINDOW, (255, 255, 255), item_rect, 2)
                draw_text(items[i]["name"], pygame.font.Font(nova, 35), (255, 255, 255), 615, rect_y + 10, "topleft")
                if items[i]["name"] == "Nimama":
                    draw_text(items[i]["name"], pygame.font.Font(nova, 35), (255, 215, 0), 615, rect_y + 10, "topleft")
                if joules < items[i]["price"]:
                    draw_text(get_suffix(items[i]["price"]), pygame.font.Font(nova, 30), (255, 27, 16), 615,
                              rect_y + 55,
                              "topleft")
                else:
                    draw_text(get_suffix(items[i]["price"]), pygame.font.Font(nova, 30), (255, 255, 255), 615,
                              rect_y + 55,
                              "topleft")
                pygame.draw.circle(WINDOW, (64, 64, 63), (950, rect_y + 50), 15)
                draw_text('i', pygame.font.Font(nova, 25), (255, 255, 255), 950, rect_y + 50)  # Info

        pygame.draw.line(WINDOW, (255, 255, 255), (WIDTH - 400, 0), (WIDTH - 400, HEIGHT), 2)

        if in_circle(mouse_x, mouse_y, 300, 400, 200):
            if left_click:
                joules += value
                click_particles.append([[mouse_x, mouse_y], [random.randint(-10, 10) / 10, -5], 255])

        for i in click_particles:
            i[0][0] += i[1][0]
            i[0][1] += i[1][1]
            i[2] -= 20
            draw_text('+' + get_suffix(value), pygame.font.Font(nova, 50), (255, 255, 255), i[0][0], i[0][1], "center",
                      i[2])
            if i[2] <= 0:
                click_particles.remove(i)

        left_click = False
        update_store = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    left_click = True
            elif event.type == pygame.MOUSEWHEEL:
                if WIDTH - 400 <= mouse_x <= WIDTH:
                    if -300 <= offset + (event.y * 20) <= 0:
                        update_store = True
                        offset += event.y * 20
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        pygame.display.flip()


def main_menu():
    global nova

    click = False
    highlight_colours = [(99, 107, 138), (99, 107, 138), (99, 107, 138)]

    while True:
        WINDOW.fill((31, 38, 64))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        draw_text('CCFR', pygame.font.Font(nova, 150), (255, 255, 255), WIDTH // 2, HEIGHT // 3)
        play_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 250, 300, 100)
        credits_button = pygame.Rect(50, 460, 250, 80)
        settings_button = pygame.Rect(700, 460, 250, 80)

        if play_button.collidepoint((mouse_x, mouse_y)):
            highlight_colours[0] = (255, 255, 255)  # Highlight button white
            if click:
                game()  # Open main game
        elif credits_button.collidepoint((mouse_x, mouse_y)):
            highlight_colours[1] = (255, 255, 255)
            if click:
                credits()  # Open credits
        elif settings_button.collidepoint((mouse_x, mouse_y)):
            highlight_colours[2] = (255, 255, 255)
            if click:
                settings()  # Open credits

        pygame.draw.rect(WINDOW, (73, 78, 99), play_button, 0, 50)
        pygame.draw.rect(WINDOW, highlight_colours[0], play_button, 5, 50)
        draw_text('Play', pygame.font.Font(nova, 75), (255, 255, 255), WIDTH // 2, HEIGHT - 205)

        pygame.draw.rect(WINDOW, (73, 78, 99), credits_button, 0, 50)
        draw_text('Credits', pygame.font.Font(nova, 50), (255, 255, 255), 175, HEIGHT - 200)
        pygame.draw.rect(WINDOW, highlight_colours[1], credits_button, 5, 50)

        pygame.draw.rect(WINDOW, (73, 78, 99), settings_button, 0, 50)
        draw_text('Settings', pygame.font.Font(nova, 50), (255, 255, 255), 825, HEIGHT - 200)
        pygame.draw.rect(WINDOW, highlight_colours[2], settings_button, 5, 50)

        click = False
        highlight_colours = [(99, 107, 138), (99, 107, 138), (99, 107, 138)]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


main_menu()