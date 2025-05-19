import pygame
from os.path import join
from random import uniform
import random
import os

class Player(pygame.sprite.Sprite):
    def __init__(self,group):
        super().__init__(group)
        
        self.image = pygame.image.load(r'C:\Users\91903\Desktop\5games-main\space shooter\images\player.png').convert_alpha()
        self.rect =  self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))   
        self.direction = pygame.Vector2()
        self.speed = 400

        #cooldo
        self.can_shoot = True
        self.lazer_shoot_time = 0
        self.cooldown_duration = 300

        #mask
        self.mask = pygame.mask.from_surface(self.image)
        
    def lazer_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.lazer_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self,dt):
        #player input
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d])-int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s])-int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        #lazer input
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and self.can_shoot: 
            Lazer(lazer_surf, self.rect.midtop, (all_sprites, lazer_sprites))
            self.can_shoot = False
            self.lazer_shoot_time = pygame.time.get_ticks()
            lazer_sound.play()
        self.lazer_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, group,star):
        super().__init__(group)
        self.image = star
        self.rect = self.image.get_frect(center = (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))

class Lazer(pygame.sprite.Sprite): 
    def __init__(self, surd, pos ,group):
        super().__init__(group)
        self.image = lazer_surf
        self.rect = self.image.get_frect(midbottom = pos)
        
    def update(self,dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos ,group):
        super().__init__(group)
        self.original_meteor = metor
        self.image = self.original_meteor
        self.rect = self.image.get_frect(center = pos)
        self.direction = pygame.Vector2(uniform(-0.5,0.5),1)
        self.speed = random.randint(200, 400)
        self.rotation = 0
        
    def update(self,dt):
        self.rotation += random.randint(20,60) * dt
        self.image = pygame.transform.rotozoom(self.original_meteor,self.rotation,1)
        self.rect.center += self.direction*self.speed * dt
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
        #used so wobbleness is stopped
        self.rect = self.image.get_frect(center = self.rect.center)

class Animation(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index] 
        self.rect = self.image.get_frect(center = pos)

    def update(self,dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)] 
        else:
            self.kill()

def collison():
    global  running, highscore
    if pygame.sprite.spritecollide(player,meteor_sprites,True,pygame.sprite.collide_mask):
        game_music.stop()
        death_sound.play()
        score = (pygame.time.get_ticks() - start_time) // 100  # or your own score logic
        if score > highscore:
            highscore = score
            save_highscore(highscore)
        running = False

    for lazer in lazer_sprites:
       if pygame.sprite.spritecollide(lazer,meteor_sprites,True,pygame.sprite.collide_mask):
           lazer.kill()
           Animation(eplosion_frames, lazer.rect.midtop,all_sprites)
           explosion_sound.play()

start_time = pygame.time.get_ticks()

def text():
    highscore_surf = font.render(f"High Score: {highscore}", True, "white")
    highscore_rect = highscore_surf.get_rect(midtop=(WINDOW_WIDTH // 2, 20))
    display_surface.blit(highscore_surf, highscore_rect)
    current_time = (pygame.time.get_ticks() - start_time) // 100
    text_surf = font.render(str(current_time),True,'white')
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH/2,WINDOW_HEIGHT-50))
    display_surface.blit(text_surf,text_rect)

def draw_button(screen, text, x, y, w, h, font):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, (170, 170, 170), (x, y, w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, (100, 100, 100), (x, y, w, h))
    
    txt = font.render(text, True, (255, 255, 255))
    screen.blit(txt, (x + 20, y + 10))
    return False

clicked = False

def show_menu():
    while True:
        display_surface.blit(menu_bg, (0, 0))
        title = font2.render("SPACE SHOOTER", True, "white")
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 200))


        myname = font3.render("A simple game by avi", True, "white")
        myname_rect  = myname.get_rect(center=(WINDOW_WIDTH-150,WINDOW_HEIGHT-650))
        display_surface.blit(title, title_rect)
        display_surface.blit(myname, myname_rect)
        
        display_surface.blit(start_button_img, start_button_rect)

        # Mouse click detection
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if start_button_rect.collidepoint(mouse):
            if click[0] and not clicked:
                clicked = True
                return      
            
        if not click[0]:
            clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        pygame.display.update()
        clock.tick(60)

def show_game_over():
     while True:
        display_surface.blit(game_over_bg, (0, 0))
        
        # Draw restart button
        display_surface.blit(restart_but, end_button_rect)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if end_button_rect.collidepoint(mouse):
            if click[0] and not clicked:
                clicked = True
                global start_time
                start_time = pygame.time.get_ticks()
                game_music.play(loops=-1)
                return  # Exit menu to restart game

        if not click[0]:
            clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        clock.tick(60)

def load_highscore():
    if os.path.exists("high.txt"):
        with open("high.txt", "r") as file:
            content = file.read().strip()
            try:
                return int(content)
            except ValueError:
                return 0
    return 0

highscore = load_highscore()

def save_highscore(new_highscore):
    with open("high.txt", "w") as file:
        file.write(str(new_highscore))


#general setup 
pygame.init()
WINDOW_WIDTH,WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
running = True
icon = pygame.image.load(join('images','iconssii.png')).convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption('Space Shooter')
clock = pygame.time.Clock()


#sprite group
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
lazer_sprites = pygame.sprite.Group()
font = pygame.font.Font(r"C:\Users\91903\Desktop\5games-main\space shooter\images\Oxanium-Bold.ttf" ,40 )
font2 = pygame.font.Font(r"C:\Users\91903\Desktop\5games-main\space shooter\images\Oxanium-Bold.ttf" ,80 )
font3 = pygame.font.Font(r"C:\Users\91903\Desktop\5games-main\space shooter\images\Oxanium-Bold.ttf" ,20 )
text_surf = font.render(' ',True,'white')

#import
start_button_img = pygame.image.load(join('images','pngegg.png')).convert_alpha()
start_button_img = pygame.transform.scale(start_button_img, (200, 80))  
start_button_rect = start_button_img.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

menu_bg = pygame.image.load(join('images','menu_bgbg.png')).convert_alpha()
star_surf = pygame.image.load(r'C:\Users\91903\Desktop\5games-main\space shooter\images\star.png').convert_alpha()

game_over_bg = pygame.image.load(join('images','end.png')).convert_alpha()

restart_but = pygame.image.load(join('images','gameover_buton.png')).convert_alpha()
restart_but = pygame.transform.scale(restart_but, (200, 80))
end_button_rect = restart_but.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 200))


game_main_bag = pygame.image.load(join('images','game_bg_main.png')).convert_alpha()
metor = pygame.image.load(r'C:\Users\91903\Desktop\5games-main\space shooter\images\meteor.png').convert_alpha()
lazer_surf = pygame.image.load(r'C:\Users\91903\Desktop\5games-main\space shooter\images\laser.png').convert_alpha()
eplosion_frames = [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]

#sounds
explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
explosion_sound.set_volume(0.2)
lazer_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
lazer_sound.set_volume(0.2)
game_music = pygame.mixer.Sound(join('audio', 'game_music.wav'))
game_music.set_volume(0.1)
game_music.play(loops=-1)
death_sound = pygame.mixer.Sound(join('audio', 'death.mp3'))
death_sound.set_volume(0.2)

for i in range(10):
    Star(all_sprites,star_surf)
player = Player(all_sprites)


#coustom event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 200)

#movement
player_direction = pygame.math.Vector2()
player_speed = 400


# Game loop controller
while True:
    show_menu()  # Main menu screen

    # Reset game state
    all_sprites.empty()
    meteor_sprites.empty()
    lazer_sprites.empty()
    for i in range(30):
        Star(all_sprites, star_surf)
    player = Player(all_sprites)
    running = True

    # Start actual game loop
    while running:
        dt = clock.tick() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == meteor_event:
                x, y = random.randint(0, WINDOW_WIDTH), random.randint(-200, -100)
                Meteor(metor, (x, y), (all_sprites, meteor_sprites))

        display_surface.blit(game_main_bag, (0, 0))
        all_sprites.update(dt)
        collison()
        text()
        all_sprites.draw(display_surface)
        display_surface.blit(text_surf, (10, 10))
        pygame.display.update()

    # Player died → show game over
    show_game_over()


