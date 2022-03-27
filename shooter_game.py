from pygame import *
from random import randint
lost = 0
score = 0
# bebra
class GameSprite(sprite.Sprite):
    def __init__(self,sprite_image,speed,x,y, sizex, sizey):
        super().__init__()
        self.speed = speed
        self.image = transform.scale(image.load(sprite_image),(sizex, sizey))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x>-10:
            self.rect.x -=self.speed
        if keys[K_d] and self.rect.x<650:
            self.rect.x +=self.speed
        if keys[K_s]and self.rect.y<450:
            self.rect.y +=self.speed
        if keys[K_w]:
            self.rect.y -=self.speed
    def fire(self):
        bullet = Bullet('bullet.png',-15, self.rect.centerx,self.rect.top,15,20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global score
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0,620)
            # lost +=1
            # if self.speed == 4:
            #     score -=1
            # elif self.speed == 3:
            #     score -=5
            # elif self.speed == 2:
            #     score -=10
            # elif self.speed == 1:
            #     score -=20
            # else: 
            #     score -= 25
            self.speed = randint(1,5)
            lost+=1
            score -= 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0 :
            self.kill()


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
screemer = transform.scale(image.load('shrek.png'), (win_width, win_height))
menu = transform.scale(image.load('pablo.jpg'), (win_width, win_height))


 
game = True
FPS = 60
clock = time.Clock()


player = Player('rocket.png', 5,350,400, 45, 90)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png',randint(1,3),randint(0,600),-100, 75, 45)
    monsters.add(monster)

asteroids=sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png',randint(1,5),randint(0,600),-100,75,45)
    asteroids.add(asteroid)


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound =mixer.Sound('fire.ogg')
bullets = sprite.Group()
# money=mixer.Sound('money.ogg')
# kick=mixer.Sound('kick.ogg')
# bebra = mixer.Sound('rrrr.mp3')sss

font.init()
font=font.SysFont('Arial',20)
pause=font.render('Чтобы продолжить - нажми r',True,(250,250,250))


lifes = 10
bullets_count=0

finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key ==K_p:
                finish = True
            if e.key == K_r:
                finish = False
            if e.key == K_SPACE and bullets_count < 10:
                fire_sound.play()
                player.fire()
                waittime = 0
                bullets_count += 1

    if not finish:
        # monster.updatehorizontal(100, 400)
        player.update()
        window.blit(background,(0,0))

        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score = score+1
            monster = Enemy('ufo.png',randint(1,5), randint(100,600),-40,80,50)
            monsters.add(monster)
        if sprite.spritecollide(player,monsters,False) or sprite.spritecollide(player,asteroids,False ):
            lifes -= 1
            if sprite.spritecollide(player,monsters,True):
                monster = Enemy('ufo.png',randint(1,5), randint(100,600),-40,80,50)
                monsters.add(monster)         
            if sprite.spritecollide(player,monsters,True):
                asteroid = Enemy('asteroid.png',randint(1,5), randint(100,600),-40,80,50)
                asteroids.add(asteroid)         
            # window.blit(lose, (200,200))

        if lifes <= 0 or lost >= 10:
            finish = True
        if score >= 10:
            finish=True
            
            # window.blit(win,(200,200))

        
        monsters.update()
        monsters.draw(window)

        asteroids.update()
        asteroids.draw(window)

        bullets.update()
        bullets.draw(window)

        if bullets_count == 10 and waittime<10:
            text = font.render('Перезарядка', True, (255, 255, 255))
            window.blit(text,(200,200))
            waittime += 1
        elif bullets_count == 10 and waittime >= 10:
            waittime = 0
            bullets_count=0

        text_lose=font.render('lost: ' + str(lost),1,(255,255,255))
        window.blit(text_lose,(0,0))
        text_score=font.render('score: ' + str(score),1,(255,255,255))
        window.blit(text_score,(0,20))
        lifestext=font.render(str(lifes),True,(250,250,250))
        window.blit(lifestext, (600,10))

        if player.rect.y<0:
            window.blit(screemer,(0,0))
            # bebra.play()
    else:
        window.blit(menu, (0,0))
        window.blit(pause, (100, 100))
        score = 0
        lost = 0
            
        for m in monsters:
            m.rect.y = -100
        for a in asteroids:
            a.rect.y = -100
        lifes = 10
        



        
            


    player.reset()
    # final.reset()
    
    display.update()
    clock.tick(FPS)