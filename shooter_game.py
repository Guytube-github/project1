#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter Game")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

clock = time.Clock()
FPS = 60

lost = 0
score = 0
max_lost = 3
life = 3

font.init()
font7 = font.SysFont('Arial', 70)
font6 = font.SysFont('Arial', 70)
font5 = font.SysFont('Arial', 70)
font4 = font.SysFont('Arial', 70)
font3 = font.SysFont('Arial', 70)
win = font3.render('YOU WON!', True, (0, 255, 0))
font2 = font.SysFont('Arial', 70)
lose = font2.render('YOU LOSE!', True, (255, 0, 0))


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_height - 80)
            lost = lost + 1

class Bullet(GameSprite): 
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()
player = Player('rocket.png', 5, win_height - 80, 10)
monsters_group = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_height - 80), -40, randint(1, 2))
    monsters_group.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy('asteroid.png', randint(30, win_width - 30), -40, randint(1, 2))
    asteroids.add(asteroid)

num_fire = 0
rel_time = False
finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    player.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True




    if not finish:
        window.blit(background,(0, 0))
        bullets.update()
        player.update()
        monsters_group.update()
        asteroids.update()
        bullets.draw(window)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font4.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))

            else:
                num_fire = 0
                rel_time = False


        collides = sprite.groupcollide(monsters_group, bullets, True, True)
        for k in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, win_height - 80), -40, randint(1, 5))
            monsters_group.add(monster)

        if score >= 10:
            finish = True
            window.blit(win, (200, 200))
        if sprite.spritecollide(player, monsters_group, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, monsters_group, True)
            sprite.spritecollide(player, asteroids, True)
            life = life - 1
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if life == 3:
            ok1 = font5.render('3', True, (0, 255, 0))
            window.blit(ok1, (650, 50))
        

        if life == 2:
            ok2 = font6.render('2', True, (255, 255, 0))
            window.blit(ok2, (650, 50))

        if life == 1:
            ok3 = font7.render('1', True, (255, 0, 0))
            window.blit(ok3, (650, 50))

        player.reset()
        monsters_group.draw(window)
        asteroids.draw(window)
        text = font1.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        display.update()
    clock.tick(FPS)



