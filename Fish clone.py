import pygame
import random
import os
xpos = 50
ypos = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (xpos,ypos)


pygame.init()
pygame.font.init()

win_width=1280
win_height=720
fps=60
run = True
background_image = pygame.image.load('background.png')
win = pygame.display.set_mode((win_width,win_height))
pygame.display.set_caption("Fish!")
blue = (0,0,255)
clock = pygame.time.Clock()

class Player:

    def __init__(self, width, height, vel, x, y, lives):
        self.width = width
        self.height = height
        self.vel = vel
        self.x = x
        self.y = y
        self.left = False
        self.right = False
        self.hitbox = (self.x, self.y +(self.height//3), self.width, (self.height//2))
        self.lives = 1
        self.score = [2,]
        
    def draw(self, win):
        player_fish_right = pygame.image.load('playerfishright.png')
        fish_right = pygame.transform.scale(player_fish_right, (self.width,self.height))
        player_fish_left = pygame.image.load('playerfishleft.png')
        fish_left = pygame.transform.scale(player_fish_left, (self.width,self.height))
        
        if self.left:
            win.blit(fish_left,(self.x,self.y))
        elif self.right:
            win.blit(fish_right,(self.x,self.y))
        else:
            win.blit(fish_right,(self.x,self.y))
        self.hitbox = (self.x + (self.width*.1 ), self.y+(self.height//3), self.width-(self.width*.1), self.height//2)

        #player hitbox
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 1)

    def get_rect(self):
        return pygame.Rect(self.hitbox)

    def get_height(self):
        return self.height

    def get_score(self):
        return sum(self.score)

class HealthUp:
    healthsprite = pygame.image.load('healthup.png')
    
    def __init__(self, width, height, healthvely, healthx,healthy):
        self.width = width
        self.height = height
        self.healthvely = healthvely
        self.healthx = healthx
        self.healthy = healthy
        self.hitbox = (self.healthx, self.healthy, self.width, self.height)

    def draw(self, win):
        healthsprite1 = pygame.image.load('healthup.png')
        healthsprite = pygame.transform.scale(healthsprite1, (self.width,self.height))
        self.move()
        win.blit(healthsprite, (self.healthx,self.healthy))
        self.hitbox = (self.healthx, self.healthy, self.width, self.height)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 1)
        
    def move(self):
        self.healthy = self.healthy + self.healthvely

    def get_rect(self):
        return pygame.Rect(self.hitbox)
        
class EnemyFish:
    
    enemy_fish_right = pygame.image.load('enemyfishright.png')
    enemy_fish_left = pygame.image.load('enemyfishleft.png')

    def __init__(self, width, height, velx, vely, x, y):
        self.width = width
        self.height = height
        self.velx = velx
        self.vely = vely
        self.x = x
        self.y = y
        self.path = [self.x, self.y]
        self.hitbox = (self.x, self.y +(self.height//3), self.width, (self.height//2))
        self.enemyRect= pygame.Rect(self.hitbox)
        
    def draw(self, win):
        enemy_fish_right = pygame.image.load('enemyfishright.png')
        fish_right = pygame.transform.scale(enemy_fish_right, (self.width,self.height))
        enemy_fish_left = pygame.image.load('enemyfishleft.png')
        fish_left = pygame.transform.scale(enemy_fish_left, (self.width,self.height))
        self.move()
        if self.velx > 0:
            win.blit(fish_right, (self.x,self.y))
        else:
            win.blit(fish_left,(self.x,self.y))
        self.hitbox = (self.x, self.y +(self.height//3), self.width, (self.height//2))
        
        #enemy hitbox
        #pygame.draw.rect(win,(blue),(self.hitbox),1)
        
    def move(self):
        if self.velx > 0:
            if self.x + self.velx < win_width:
                self.x += self.velx
            else:
                self.velx = self.velx *-1
        else:
            if self.x - self.velx > 0:
                self.x += self.velx
            else:
                self.velx = self.velx *-1
        if self.vely > 0:
            if self.y + self.vely < 720:
                self.y += self.vely
            else:
                self.vely = self.vely *-1
        else:
            if self.y - self.vely > 0:
                self.y += self.vely
            else:
                self.vely = self.vely *-1

    def get_rect(self):
        return pygame.Rect(self.hitbox)
    
    def get_height(self):
        return self.height


player = Player(36, 20, 6, win_width/2, win_height/2, 1)


def randomExcept(start, end, n, param):
    return list(range(int(start), int(n))) + list(range(int(n)+int(param), int(end)))


names = []
posneg = [1,-1]
numberOfEnemies = 0
enemyLimit = 44
while numberOfEnemies <=enemyLimit:   
    width = random.randint(player.width-5,player.width+35)
    height = int(0.5555*width)
    velx = random.randint(1,10)*random.choice(posneg)
    vely = random.randint(0,2)*random.choice(posneg)
    x = int(random.choice(randomExcept(10,1280,player.x,player.width)))
    y = int(random.choice(randomExcept(10,720,player.y,player.height)))
    i = EnemyFish(width, height, velx, vely, x, y)
    names.append(i)
    numberOfEnemies +=1

lifeup1 = False

gameover = False

def gameoverfx():
    
    highscores = open('highscore.txt')
    highestscore = float((highscores.read()))
    highscores.close()    
    score = player.get_score()
    if highestscore < score:
        newhighscores = open ('Highscore.txt', 'w')
        newhighscores.write(str(score))
        newhighscores.close()

    global gameover
    gameover = True
    ball.velx = 0
    ball.vely = 0
    player.vel = 0
    redrawGameWindow()


def redrawGameWindow():
    global gameover
    win.blit(background_image, (0, 0))
    player.draw(win)

    if gameover:
        gameFont = pygame.font.SysFont('fixedsys', 30)
        gameoversurface = gameFont.render('Game Over.', False, (255,0,0))
        win.blit(gameoversurface,(5,25))
    
    if lifeup1==True:
        lifeup.draw(win)

    for name in names:
        name.draw(win)
        
    gameFont = pygame.font.SysFont('fixedsys', 30)
    textsurface = gameFont.render('Lives: '+ str(player.lives), False, (0,0,0))
    playerscore = str(player.get_score())
    scoresurface = gameFont.render('Score: '+ playerscore, False, (0,0,0))
    win.blit(textsurface,(5,5))
    win.blit(scoresurface, (5,30))
    
    pygame.display.update()



#fish1 = EnemyFish(60,35, 2,1,50,50)

while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # implement momentum into movement (releasing left key, sprite will take time to slow down)

    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > player.vel:
        player.x -= player.vel
        player.left = True
        player.right = False
    if keys[pygame.K_RIGHT] and player.x < win_width-player.width:
        player.x += player.vel
        player.left = False
        player.right = True
    if keys[pygame.K_UP] and player.y > player.vel:
        player.y-=player.vel
    if keys[pygame.K_DOWN] and player.y < win_height-player.height-player.vel:
        player.y += player.vel
        

    if player.get_score() % 60 == 0:
        player.score.append(2)
        healthvely = random.randint(2,5)
        healthx = random.randint(10, 1270)
        lifeup = HealthUp(15, 15, healthvely, healthx,5)
        lifeup1=True
        

    if lifeup1 == True:
        if player.get_rect().colliderect(lifeup.get_rect()):
            lifeup1 = False
            player.lives+=1
        
    
    for i in names:
        if player.get_rect().colliderect(i.get_rect()):
            if player.get_height() > i.get_height():
                player.score.append(2)
                names.remove(i)
                player.width +=2
                player.height +=1
            elif player.get_height() < i.get_height():
                player.lives -=1
                player.x = win_width/2
                player.y = win_height/2
                names.clear()
                if player.lives <= 0:
                    gamoverfx()
                
            while len(names) <=enemyLimit:   
                width = random.randint(player.width-20,player.width+20)
                height = int(0.5555*width)
                velx = random.randint(1,8)*random.choice(posneg)
                vely = random.randint(1,2)*random.choice(posneg)
                x = int(random.choice(randomExcept(10,1280,player.x,player.width)))
                y = int(random.choice(randomExcept(10,720,player.y,player.height)))
                i = EnemyFish(width, height, velx, vely, x, y)
                names.append(i)
                numberOfEnemies +=1
            
    redrawGameWindow()
    
pygame.quit()
