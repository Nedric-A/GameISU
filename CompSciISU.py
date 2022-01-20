import pygame
import random
from pygame import mixer
mixer.init()
pygame.init()
#Window
width = 600
height = 600
WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption("Annoying Climb 2.0")
#Frames
FPS = 60
# Colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
sky = (124, 208, 237)

#Variables
scroll_line = 200
scroll = 0
grav = 1
max_platforms = 10
background_scroll = 0
score = 0
#Game Over Variables
fade_counter = 0
game_over = False
#Sounds
pygame.mixer.music.load('GamesIsuAudio/background_audio.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0)
jump_sound = pygame.mixer.Sound('GamesIsuAudio/Spring-Boing.mp3')
jump_sound.set_volume(0.1)
death_sound = pygame.mixer.Sound('GamesIsuAudio/falling.mp3')
#Fonts
font_small = pygame.font.SysFont('Catamara', 25)
font_big = pygame.font.SysFont('Catmara', 30)

# Images
bunny_image = pygame.image.load('GameISUImages/bunny.png')
background = pygame.image.load('GameISUImages/background.png')
platform_image = pygame.image.load('GameISUImages/platform.png')

#Text Outputs
def draw_text(text, font, text_col, x ,y):
    img = font.render(text, True, text_col)
    WIN.blit(img, (x, y))

#background scroll
def draw_background(background_scroll):
    WIN.blit(background, (0, 0 + background_scroll))
    WIN.blit(background, (0, -600 + background_scroll))

#HUD
def draw_hud():
    pygame.draw.rect(WIN, sky, (0, 0, width, 30))
    pygame.draw.line(WIN, white, (0, 30), (width, 30), 2)
    draw_text('Score: ' +str(score) + 'M',font_small, white, 0 ,0)
class Player():
    def __init__(self, x, y):
        #Bunny Size
        self.image = pygame.transform.scale(bunny_image, (65, 65))
        self.width = 60
        self.height = 65
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def move(self):
        scroll = 0
        dx = 0
        dy = 0
        #Keyboard Input
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a]:
            dx = - 5
            self.flip = True
        if keys_pressed[pygame.K_d]:
            dx = 5
            self.flip = False


        #Gravity
        self.vel_y += grav
        dy += self.vel_y
        #Side Borders
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > 600:
            dx = 600 - self.rect.right
        #Platform Borders
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y +dy, self.width, self.height):
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20
                        jump_sound.play()

        #Start Scrolling
        if self.rect.top <= scroll_line:
            #If jumping, scroll
            if self.vel_y < 0:
                scroll = -dy

        #movement update
        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll

    def draw(self):
        WIN.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x-4, self.rect.y))
        pygame.draw.rect(WIN, white, self.rect, 2)

#Platforms
class Platform(pygame.sprite.Sprite):
    def __init__(self,x ,y ,width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (100, 10))
        self.moving = moving
        self.move_counter = random.randint(0,50)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1,2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        #Moving Platforms
        if self.moving == True:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed
        #Switch Directions
        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > width:
            self.direction *=-1
            self.move_counter = 0
        #Updating Y Value Platform Position
        self.rect.y += scroll
        #Unload Gone Platforms
        if self.rect.top > height:
            self.kill()


#Sprites
platform_group = pygame.sprite.Group()

#Start Platform
platform = Platform(width//2 - 50, height - 50, 100, False)
platform_group.add(platform)


#Player
bunny = Player(width//2, height - 150)


#Frames
clock = pygame.time.Clock()
clock.tick(FPS)
run = True
while run:
    if game_over == False:
        scroll = bunny.move()
        #Infinite Background
        background_scroll += scroll
        if background_scroll >= 600:
            background_scroll  = 0
        draw_background(scroll)

        #Platform Generation
        if len(platform_group) < max_platforms:
            plat_width = random.randint(40, 60)
            plat_x = random.randint(0, 500 - plat_width)
            plat_y = platform.rect.y - random.randint(80, 100)
            plat_type = random.randint(1,2)
            #Generates Moving Platforms
            if plat_type == 1 and score > 25:
                plat_moving =True
            else:
                plat_moving =  False
            platform = Platform(plat_x, plat_y, plat_width, plat_moving)
            platform_group.add(platform)

        #Platform Updates
        platform_group.update(scroll)

        #Score
        if scroll > 0:
            score += scroll // 10

        #Drawing the Sprites
        bunny.draw()
        platform_group.draw(WIN)
        draw_hud()

        #Frames Per Minute
        clock.tick(FPS)

        #Game Over
        if bunny.rect.top > height:
            game_over = True
            death_sound.play()

    else:
        if fade_counter < width:
            fade_counter += 5
            pygame.draw.rect(WIN, black, (0, 0, fade_counter, height))

        #Game Over Text
        draw_text('Game Over!', font_big, red, width//2-35, 200)
        draw_text('Score: ' + str(score) + 'M', font_big, white, width//2-30, 250)
        draw_text('Press Space to Play Again', font_big, white, width//2 -100, 300)
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE]:
            #Reset
            game_over = False
            score = 0
            scroll = 0
            fade_counter = 0
            bunny.rect.center = (width//2, height-150)
            platform_group.empty()
            #Generate Platforms Again
            platform = Platform(width//2-50, height -50, 100, False)
            platform_group.add(platform)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
