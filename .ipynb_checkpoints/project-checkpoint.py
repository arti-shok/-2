import pygame, sys
from random import choice
from csv import reader

pygame.init()

size = width, height = 650, 406
screen = pygame.display.set_mode(size)
pygame.display.set_caption('pepe')
fps = 60
clock = pygame.time.Clock()
cell_size = 50
black = 0, 0, 0


with open("C:\\Users\\iriska\\my_project\\kt2\\levels\\levels.txt", "r") as f:
    levels = []
    lines = reader(f)
    for line in lines:
        levels.append(line)
text1 = ["", "1. Начать игру", "2. Выбор уровня","3. Выход"]
text2 = ["","1. Первый уровень. Джунгли", "2. Второй уровень. Ледяная пещера", "3. Третий уровень. Подземелье", "4. Назад"]
text3 = ["","1. Продолжить", "2. Начать сначала", "3. Вернуться в меню", "4. Выйти из игры"]

def load_sound(name, volume = 1):
    fullname = "C:\\Users\\iriska\\my_project\\kt2\\sounds\\"+name
    sound = pygame.mixer.Sound(fullname)
    sound.set_volume(volume)
    return sound

def load_image(name):
    fullname = "C:\\Users\\iriska\\my_project\\kt2\\sprites\\"+name
    if fullname[-3::] == "png": 
        image = pygame.image.load(fullname).convert_alpha()
    else:
        image = pygame.image.load(fullname).convert()
    return image

def terminate():
    pygame.quit()
    sys.exit()

def load_level(name):
    fullname = "C:\\Users\\iriska\\my_project\\kt2\\levels\\" + name
    with open(fullname, "r") as f:
        level_map = []
        for line in f:
            line = line.strip()
            level_map.append(line)
    return level_map

def draw_level(level_map, wall_image, ground_image, queen_image, portal_image, fire_image):
    new_player, x, y, portals = None, None, None, []
    loading()
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            if level_map[y][x] == "#":
                Tile(ground_image, x, y)
                Tile(wall_image, x, y, "wall")
            elif level_map[y][x] == "*":
                Tile(ground_image, x, y)
            elif level_map[y][x] == "%":
                Tile(ground_image, x, y)
                new_player = Player(x, y)
            elif level_map[y][x] == "&":
                queen = Queen(x, y, queen_image)
                Tile(ground_image, x, y)
            elif level_map[y][x] == "+":
                Tile(ground_image, x, y)
                portals.append(Tile(portal_image, x, y, "portal"))
            elif level_map[y][x] == "!":
                Tile(wall_image, x, y, "wall")
                Tile("torch.png", x, y, "torch")
            elif level_map[y][x] == "?":
                Tile(ground_image, x, y)
                Tile("torch.png", x, y, "torch")
            elif level_map[y][x] == "~":
                Tile("water.jpg", x, y, "wall")
            elif level_map[y][x] == ".":
                Tile("sand.jpg", x, y)
            elif level_map[y][x] == "@":
                Tile(ground_image, x, y)
                Enemy("angry_pepe_small.png", x, y)
            elif level_map[y][x] == "^":
                Tile(ground_image, x, y)
                Tile(fire_image, x, y, "fire")
            elif level_map[y][x] == ">":
                Tile("sand.jpg", x, y)
                Tile(fire_image, x, y, "fire")
            elif level_map[y][x] == "B":
                Tile(ground_image, x, y)
                Enemy("rage-pepe.png", x, y)
            elif level_map[y][x] == "H":
                Tile(ground_image, x, y)
                Tile("health_big.png", x, y, "health")
            elif level_map[y][x] == "L":
                Tile(ground_image, x, y)
                Tile("lock.png", x, y, "lock")
            elif level_map[y][x] == "K":
                Tile(ground_image, x, y)
                Tile("key.png", x, y, "key")

    return new_player, queen, portals

def draw_text(txt, font_size, color = black):
    pygame.font.init()
    font = pygame.font.Font("C:\\Users\\iriska\\my_project\\kt2\\font\\font.ttf", font_size)
    text = font.render(txt,1, color)
    text_w, text_h = text.get_width(), text.get_height()
    text_x = (width - text_w) // 2
    text_y = (height - text_h) // 2
    screen.blit(text,(text_x, text_y))

def clear_all():
    all_sprites.empty()
    player_group.empty()
    tiles_group.empty()
    target_group.empty()
    walls_group.empty()
    enemy_group.empty()
    torch_group.empty()
    fire_group.empty()
    health_group.empty()
    lock_group.empty()
    portal_group.empty()
    keys_group.empty()

def loading():
    background = load_image('background.jpg')
    screen.blit(background, (0, 0))
    draw_text("Загрузка...", 50, (181, 24, 24))
    pygame.display.flip()

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, group = None):
        if group == "wall":
            super().__init__(walls_group, tiles_group, all_sprites)
            self.type = "wall"
        elif group == "portal":
            super().__init__(tiles_group, all_sprites, portal_group)
            self.type = "portal"
        elif group == "torch":
            super().__init__(tiles_group, all_sprites, torch_group)
            self.type = "torch"
        elif group == "fire":
            super().__init__(tiles_group, all_sprites, fire_group)
            self.type = "fire"
        elif group == "health":
            super().__init__(tiles_group, all_sprites, health_group)
            self.type = "health"
        elif group == "lock":
            super().__init__(tiles_group, all_sprites, lock_group)
            self.type = "lock"
        elif group == "key":
            super().__init__(tiles_group, all_sprites, keys_group)
            self.type = "key"
        else:
            super().__init__(tiles_group, all_sprites)
            self.type = "ground"
        self.image = load_image(image)
        self.rect = self.image.get_rect().move(cell_size*x, cell_size*y)
        self.add(tiles_group, all_sprites)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.image = load_image("Pepe.png")
        self.health_image = load_image("health.png")
        self.key_image = load_image("key_small.png")
        self.rect = self.image.get_rect().move(cell_size*x, cell_size*y)
        self.portal = True
        self.health = 5
        self.time = 0
        self.keys = 0
        self.add(player_group, all_sprites)
    def move_up(self):
        if self.health > 0:
            step_sound.play()
            self.rect = self.rect.move(0, -cell_size)
            if pygame.sprite.spritecollideany(self, lock_group):
                if self.keys == 0:
                    lock_sound.play()
                    self.rect = self.rect.move(0, cell_size)
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect = self.rect.move(0, cell_size)
    def move_down(self):
        if self.health > 0:
            step_sound.play()
            self.rect = self.rect.move(0, cell_size)
            if pygame.sprite.spritecollideany(self, lock_group):
                if self.keys == 0:
                    lock_sound.play()
                    self.rect = self.rect.move(0, -cell_size)
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect = self.rect.move(0, -cell_size)
    def move_left(self):
        if self.health > 0:
            step_sound.play()
            self.rect = self.rect.move(-cell_size, 0)
            if pygame.sprite.spritecollideany(self, lock_group):
                if self.keys == 0:
                    lock_sound.play()
                    self.rect = self.rect.move(cell_size, 0)
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect = self.rect.move(cell_size, 0)
    def move_right(self):
        if self.health > 0:
            step_sound.play()
            self.rect = self.rect.move(cell_size, 0)
            if pygame.sprite.spritecollideany(self, lock_group):
                if self.keys == 0:
                    lock_sound.play()
                    self.rect = self.rect.move(-cell_size, 0)
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect = self.rect.move(-cell_size, 0)
    def move_portal(self, portals_n):
        if self.health > 0:
            if self.portal:
                portal_sound.play()
                for i in range(len(portals_n)):
                    if pygame.sprite.collide_rect(self, portals_n[i]):
                        self.rect.x = portals_n[(i+1) % len(portals_n)].rect.x
                        self.rect.y = portals_n[(i+1) % len(portals_n)].rect.y
                        self.portal = False
                        break
    def draw_health(self):
        if self.health > 0:
            x = 25
            for i in range(self.health):
                screen.blit(self.health_image, (x, 25))
                x +=27
    def draw_keys(self):
        x = 25
        for i in range(self.keys):
            screen.blit(self.key_image, (x, 60))
            x +=27
    def get_damage(self):
        if self.health > 0:
            if self.time % (fps*3/4) == 0:
                damage_sound.play()
                self.health -= 1
                if self.health == 0:
                    game_over_sound.play()
            self.time +=2
    def get_health(self):
        heart_sound.play()
        if self.health < 5:
            self.health +=1
    def get_key(self):
        key_sound.play()
        self.keys +=1
    def unlock(self, lock_n):

        unlock_sound.play()
        self.keys -=1
        lock_n.kill()

class Queen(pygame.sprite.Sprite):
    def __init__(self, x, y, image_queen):
        super().__init__(target_group, all_sprites)
        self.image = load_image(image_queen)
        self.rect = self.image.get_rect().move(cell_size*x, cell_size*y)
        self.add(target_group, all_sprites)

class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
    def update(self, sprite):
        self.dx = -(sprite.rect.x + sprite.rect.w // 2 - width // 2)
        self.dy = -(sprite.rect.y + sprite.rect.h // 2 - height // 2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_enemy, x, y):
        super().__init__(all_sprites, enemy_group)
        self.delay = 0
        self.image = load_image(image_enemy)
        self.rect = self.image.get_rect().move(x*cell_size, y*cell_size)
        self.add(all_sprites, enemy_group)
    def move(self):
        if self.delay % (fps * 3/4) == 0:
            move = choice([[50,0],[-50,0],[0,50],[0,-50]])
            self.rect.move_ip(move)
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.move_ip([-i for i in move])
        self.delay +=1


def start_screen(text, mode, level_z = None):
    
    background = load_image('background.jpg')
    screen.blit(background, (0, 0))

    pygame.font.init()

    font = pygame.font.Font("C:\\Users\\iriska\\my_project\\kt2\\font\\font.ttf", 60)
    title = font.render("Pepe's Adventures", 1, (181, 24, 24))
    title_rect = title.get_rect()
    title_rect.top = 50
    title_rect.x = 50
    screen.blit(title, title_rect)

    font = pygame.font.Font("C:\\Users\\iriska\\my_project\\kt2\\font\\font.ttf", 35)
    text_coord = 50 + title_rect.height
    menu_sound.play(-1)
    for line in text:
        string = font.render(line, 1, (181, 24, 24))
        string_rect = string.get_rect()
        text_coord = text_coord + 10
        string_rect.top = text_coord
        string_rect.x = 50
        text_coord = text_coord + string_rect.height
        screen.blit(string, string_rect)

    if mode == "start":
        clear_all()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    running = False
                    menu_sound.stop()
                    menu_tick_sound.play()
                    for level in levels:
                        run_level(level[0], level[1], level[2], level[3], level[4], (int(level[5]), int(level[6]), int(level[7])), level[8], level[9], level[10])
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    running = False
                    menu_sound.stop()
                    menu_tick_sound.play()
                    start_screen(text2, "choice")
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    terminate()
            pygame.display.flip()
            clock.tick(fps)
    elif mode == "choice":
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    running = False
                    menu_sound.stop()
                    menu_tick_sound.play()
                    for i in range(2):
                        clear_all()
                        level_n = levels[i]
                        run_level(level_n[0], level_n[1], level_n[2], level_n[3], level_n[4], (int(level_n[5]), int(level_n[6]), int(level_n[7])), level_n[8], level_n[9], level_n[10])
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    running = False
                    menu_sound.stop()
                    menu_tick_sound.play()
                    for i in [1, 2]:
                        clear_all()
                        level_n = levels[i]
                        run_level(level_n[0], level_n[1], level_n[2], level_n[3], level_n[4], (int(level_n[5]), int(level_n[6]), int(level_n[7])), level_n[8], level_n[9], level_n[10])
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    running = False
                    clear_all()
                    menu_sound.stop()
                    menu_tick_sound.play()
                    level_n = levels[2]
                    run_level(level_n[0], level_n[1], level_n[2], level_n[3], level_n[4], (int(level_n[5]), int(level_n[6]), int(level_n[7])), level_n[8], level_n[9], level_n[10])
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                    running = False
                    menu_sound.stop()
                    menu_tick_sound.play()
                    start_screen(text1, "start")
                    break
            pygame.display.flip()
            clock.tick(fps)
    elif mode == "pause":
        sound.stop()
        pause_open_sound.play()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_1 or event.key == pygame.K_ESCAPE):
                    running = False
                    menu_sound.stop()
                    pause_close_sound.play()
                    sound.play(-1)
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    running = False
                    menu_sound.stop()
                    menu_tick_sound.play()
                    if level_z == "level1.txt":
                        for i in range(2):
                            clear_all()
                            level_n = levels[i]
                            run_level(level_n[0], level_n[1], level_n[2], level_n[3], level_n[4], (int(level_n[5]), int(level_n[6]), int(level_n[7])), level_n[8], level_n[9], level_n[10])
                    elif level_z == "level2.txt":
                        for i in [1, 2]:
                            clear_all()
                            level_n = levels[i]
                            run_level(level_n[0], level_n[1], level_n[2], level_n[3], level_n[4], (int(level_n[5]), int(level_n[6]), int(level_n[7])), level_n[8], level_n[9], level_n[10])
                    elif level_z == "level3.txt":
                        level_n = levels[2]
                        clear_all()                      
                        level_n = levels[2]
                        run_level(level_n[0], level_n[1], level_n[2], level_n[3], level_n[4], (int(level_n[5]), int(level_n[6]), int(level_n[7])), level_n[8], level_n[9], level_n[10])
                    
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    running = False
                    menu_sound.stop()
                    menu_tick_sound.play()
                    start_screen(text1, "start")
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                    running = False
                    terminate()
                    break
            pygame.display.flip()
            clock.tick(fps)

def run_level(level_map, wall_image, ground_image, target_image, portal_image, color, fire_image, level_sound, level_theme):

    with open("C:\\Users\\iriska\\my_project\\kt2\\levels\\text_" + level_map, "r", encoding= 'utf8') as f:
        reader = f.readlines()
        level_text = [i.strip() for i in reader]
    player, target, portals = draw_level(load_level(level_map), wall_image, ground_image, target_image, portal_image, fire_image)
    camera = Camera()
    global sound
    sound = load_sound(level_sound, 0.2)
    theme = load_sound(level_theme)
    theme.play()
    sound.play(-1)
    running = True
    textQ = True
    font_grow = True
    while running:
        for event in pygame.event.get():
            while textQ:
                for event_n in pygame.event.get():
                    if event_n.type == pygame.QUIT:
                        terminate()
                    if event_n.type == pygame.KEYDOWN:
                        textQ = False
                        theme.stop()
                screen.fill(color)
                if font_grow:
                    for i in range(40,45,1):
                        screen.fill(color)
                        draw_text(level_text[0], i)
                    font_grow = not font_grow
                else:
                    for i in range(45,40,-1):
                        screen.fill(color)
                        draw_text(level_text[0], i)
                    font_grow = not font_grow

                pygame.display.flip()
                clock.tick(fps//10)
                
                
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                player.move_up()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                player.move_down()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player.move_left()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player.move_right()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                start_screen(text3, "pause", level_map)
           
        camera.update(player)
        for sprite in all_sprites:
             camera.apply(sprite)

        for enemy in enemy_group:
            enemy.move()

        if pygame.sprite.spritecollideany(player, portal_group):
            player.move_portal(portals)
        else:
            player.portal = True

        if pygame.sprite.spritecollideany(player, enemy_group) or pygame.sprite.spritecollideany(player, fire_group):
            player.get_damage() 

        if pygame.sprite.groupcollide(player_group, health_group, False, True):
            player.get_health()

        if pygame.sprite.groupcollide(player_group, keys_group, False, True):
            player.get_key()

        for lock in lock_group:
            if pygame.sprite.collide_rect(player, lock):
                player.unlock(lock)  

        if not pygame.sprite.collide_rect(player, target):
            screen.fill(color)
            tiles_group.draw(screen)
            
            enemy_group.draw(screen)
            target_group.draw(screen)
            player_group.draw(screen)
            player.draw_health()
            player.draw_keys()
        else:
            clear_all()
            sound.stop()
            if level_map == "level3.txt":
                textQ = True
                font_grow = True
                end_sound.play()
                ending_sound.play()
                while textQ:
                    for event_n in pygame.event.get():
                        if event_n.type == pygame.QUIT:
                            terminate()
                        if event_n.type == pygame.KEYDOWN:
                            textQ = False
                            end_sound.stop()
                            ending_sound.stop()
                            del(portals, camera,target, level_text, textQ)
                            start_screen(text1, "start")
                            running = False
                    screen.fill(color)
                    if font_grow:
                        for i in range(40,45,1):
                            screen.fill(color)
                            draw_text(level_text[1], i)
                        font_grow = not font_grow
                    else:
                        for i in range(45,40,-1):
                            screen.fill(color)
                            draw_text(level_text[1], i)
                        font_grow = not font_grow

                    pygame.display.flip()
                    clock.tick(fps//10) 
            else:
                del(portals, camera, target, level_text, textQ, sound, theme)
                running = False
        
        if player.health <= 0:
            screen.blit(load_image('gameover.png'), (125, 61))  

        pygame.display.flip()
        clock.tick(fps)
    
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
target_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
torch_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
fire_group = pygame.sprite.Group()
health_group = pygame.sprite.Group()
lock_group = pygame.sprite.Group()
keys_group = pygame.sprite.Group()


menu_sound = load_sound("menu.wav", 0.3)
menu_tick_sound = load_sound("Menu_tick.wav")
pause_close_sound = load_sound("pause_close.wav")
pause_open_sound = load_sound("pause_open.wav")

lock_sound = load_sound("Door_Closed.wav", 0.7)
unlock_sound = load_sound("Door_Opened.wav")
end_sound = load_sound("end.wav", 0.1)
game_over_sound = load_sound("game_over.wav", 0.5)
heart_sound = load_sound("heart.wav", 0.7)
key_sound = load_sound("key.wav")
damage_sound = load_sound("Player_Hit.wav")
portal_sound = load_sound("portal.wav", 0.4)
step_sound = load_sound("step_1.wav", 0.4)
ending_sound = load_sound("theme_level3_2.wav")

start_screen(text1, "start")


terminate()