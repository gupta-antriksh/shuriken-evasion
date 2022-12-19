import pygame
from pygame.locals import *
import math
import random
from pygame import mixer

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#screen
screen_width = 1542
screen_height = 863
screen = pygame.display.set_mode((screen_width,screen_height),0,32)

#background and scroll variables
bg = pygame.image.load('art/snowySky.png')
bg_width = bg.get_width()
bg_height = bg.get_height()
scrollX = 0
scrollY = 0
tilesX = 4
tilesY = 4

#title and icon
pygame.display.set_caption("Dodge'em All!")
icon = pygame.image.load('art/shurikenRed.png')
pygame.display.set_icon(icon)

#background music
mixer.music.load('sounds/Shepard-tone.mp3')

#player
playerImg = pygame.image.load('art/paperPlane.png').convert()
playerImg.set_colorkey((0,0,0))
playerX = screen_width/2 
playerY = screen_height/2 
playerX_vel = 0
playerY_vel = 0
playerAngle = 0
player_max_vel = 0

#missiles
number_of_missiles = 5
missileImg = []
missileImg.append(pygame.image.load('art/shurikenBlack.png'))
missileImg.append(pygame.image.load('art/shurikenRed.png'))
missileX = []
missileY = []
missileType = []
missileX_vel = []
missileY_vel = []
missileX_acc = []
missileY_acc = []
missile_max_acc = []
missile_angle = []
missile_max_acc.append(1)
missile_max_acc.append(1.1)
for i in range(20):
    if(i%2):
        missileX.append(-564)
    else:
        missileX.append(2106)
    missileY.append(random.randrange(-64,927,1))
    missileX_vel.append(0)
    missileY_vel.append(0)
    missileX_acc.append(0)
    missileY_acc.append(0)
    if i<5 or i%4==1:
        missileType.append(0)
    else:
        missileType.append(1)   
    missile_angle.append(0)

#sounds
collision_Sound = mixer.Sound('sounds/explosion.wav')
game_over_Sound = mixer.Sound('sounds/gameOver.wav')

#score
score_value = 0
score_by_twenty = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 20
textY = 20

#game over
over_font = pygame.font.Font('freesansbold.ttf',64)
is_game_over = False

def game_over_text():
    game_over1 = over_font.render("YOU FELL PREY TO",True,(168,0,0))
    game_over2 = over_font.render("THE ENEMY!",True,(168,0,0))
    final_score = font.render("Your Final Score is " + str(score_value),True,(0,0,0))
    restart_text = font.render("Press R to Restart",True,(0,0,0))
    escape_text = font.render("Press Esc to quit to Title",True,(0,0,0))
    screen.blit(game_over1,(460,280))
    screen.blit(game_over2,(560,360))
    screen.blit(final_score,(600,440))
    screen.blit(restart_text,(625,490))
    screen.blit(escape_text,(575,540))

def show_score(x,y):
    score = font.render("Score : " + str(score_value),True,(0,0,0))
    screen.blit(score,(x,y))

def show_start_screen():
    start_title = over_font.render("SHURIKEN EVASION",True,(128,0,128))
    start_text = font.render("Start",True,(255,255,255))
    help_text = font.render("Help",True,(255,255,255))
    exit_text = font.render("Exit",True,(255,255,255))
    pygame.draw.rect(screen,(0,0,0),[570,280,400,60])
    pygame.draw.rect(screen,(0,0,0),[570,550,400,60])
    pygame.draw.rect(screen,(0,0,0),[570,700,400,60])
    screen.blit(start_title,(452,110))
    screen.blit(start_text,(728,295))
    screen.blit(help_text,(730,565))
    screen.blit(exit_text,(735,715))

def show_help_screen():
    help_title = over_font.render("HELP",True,(0,0,0))
    story_text_1 = font.render("You were on an espionage mission. You succesfully stole the secret code and gathered",True,(0,0,0))
    story_text_2 = font.render("important intel, and while returning, you disguised yourself as a paper plane.",True,(0,0,0))
    story_text_3 = font.render("But YOU WERE BEING WATCHED, and your disguise has been compromised.",True,(0,0,0))
    story_text_4 = font.render("EVADE THE ENEMY'S SHURIKENS AT ALL COSTS!",True,(0,0,0))
    controls_text_1 = font.render("Use the mouse cursor to guide yourself through the snowy skies. Shuriken of",True,(0,0,0))
    controls_text_2 = font.render("same type destroy each other upon collision and give you points. Press Esc",True,(0,0,0))
    controls_text_3 = font.render("during gameplay to Pause the game and press again to Resume. Good Luck!",True,(0,0,0))
    controls_text_4 = font.render("BEWARE: Black shuriken are fast, but Red ones are even faster!",True,(168,0,0))
    back_text = font.render("Back",True,(255,255,255))
    pygame.draw.rect(screen,(0,0,0),[570,700,400,60])
    screen.blit(help_title,(690,110))
    screen.blit(back_text,(735,715))
    screen.blit(story_text_1,(80,200))
    screen.blit(story_text_2,(160,250))
    screen.blit(story_text_3,(160,300))
    screen.blit(story_text_4,(380,350))
    screen.blit(controls_text_1,(160,500))
    screen.blit(controls_text_2,(160,550))
    screen.blit(controls_text_3,(160,600))
    screen.blit(controls_text_4,(250,650))

def show_pause_screen():
    resume_text = font.render("Resume",True,(255,255,255))
    back_text = font.render("Back to Title",True,(255,255,255))
    pygame.draw.rect(screen,(0,0,0),[570,220,400,60])
    pygame.draw.rect(screen,(0,0,0),[570,611,400,60])
    screen.blit(resume_text,(705,235))
    screen.blit(back_text,(675,625))

def player(angle):
    playerImg_copy = pygame.transform.rotate(playerImg,angle)
    screen.blit(playerImg_copy, (playerX-int(playerImg_copy.get_width())/2, (playerY-int(playerImg_copy.get_height())/2)))

def missile(x,y,missileType,angle):
    missileImg_copy = pygame.transform.rotate(missileImg[missileType],angle)
    screen.blit(missileImg_copy,(x-int(missileImg_copy.get_width())/2,y-int(missileImg_copy.get_height())/2))

def distance(x1,y1,x2,y2):
    return math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))

#explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,6):
            img = pygame.image.load(f"art/exp{num}.png")
            img = pygame.transform.scale(img, (100,100))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.counter = 0

    def update(self):
        explosion_speed = 4
        #update explosion animation
        self.counter+=1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        #if animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

explosion_group = pygame.sprite.Group()

def explosion(x,y):
    explosion_group.add(Explosion(x,y))
    collision_Sound.play()

#gamestate: 0-start,1-gameplay,2-pause,3-help
game_state = 0
keyup = False

#game loop
running = True
while running:

    clock.tick(FPS)
    
    #show background
    for i in range(tilesX):
        for j in range(tilesY):
            screen.blit(bg, ((i-1)*bg_width+scrollX,(j-1)*bg_height+scrollY))

    #show score
    if (game_state == 1 or game_state == 2) and not is_game_over:
        show_score(textX+100,textY+100)
    
    #rendering explosions
    if game_state == 1:
        explosion_group.draw(screen)
        explosion_group.update()

    if game_state != 1:
        (mx,my) = pygame.mouse.get_pos()

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #keypresses
        if game_state == 1 and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                #restart
                is_game_over = False
                score_value = 0
                score_by_twenty = 0
                player_max_vel = 0
                for i in range(number_of_missiles):
                    if(i%2):
                        missileX[i]= -564
                    else:
                        missileX[i] = 2106
                    missileY[i] = random.randrange(-64,927,1)
                    missileX_vel[i]
                    missileY_vel[i] = 0
                    missileX_acc[i] = 0
                    missileY_acc[i] = 0
                number_of_missiles = 5
                mixer.music.play(-1)
            if event.key == pygame.K_ESCAPE:
                if not is_game_over:
                    game_state = 2
                    keyup = False
                else:
                    game_state = 0
            i
        
        if game_state == 2:            
            if keyup and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if is_game_over:
                    game_state = 0
                else:
                    game_state = 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mx >= 570 and mx <= 970:
                    if my >= 220 and my <= 280:
                        game_state = 1
                    elif my >= 611 and my <= 671:
                        game_state = 0

        if event.type == KEYUP and event.key == pygame.K_ESCAPE:
            keyup = True

        if game_state == 0:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mx >= 570 and mx <= 970:
                    if my >= 280 and my <= 340:
                        is_game_over = False
                        score_value = 0
                        score_by_twenty = 0
                        player_max_vel = 0
                        for i in range(number_of_missiles):
                            if(i%2):
                                missileX[i]= -564
                            else:
                                missileX[i] = 2106
                            missileY[i] = random.randrange(-64,927,1)
                            missileX_vel[i]
                            missileY_vel[i] = 0
                            missileX_acc[i] = 0
                            missileY_acc[i] = 0
                        number_of_missiles = 5
                        mixer.music.play(-1)
                        game_state = 1
                    if my >= 550 and my <= 610:
                        game_state = 3
                    if my >= 700 and my <= 760:
                        running = False

        if game_state == 3:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mx >= 570 and mx <= 970 and my>=700 and my <= 760:
                    game_state = 0
                

    #player dyanamics
    if game_state == 1:
        (mx,my) = pygame.mouse.get_pos()
        playerX_vel = player_max_vel*(mx-(playerX))/math.sqrt(math.pow(mx-(playerX),2)+math.pow(my-(playerY),2)+0.0001)
        playerY_vel = player_max_vel*(my-(playerY))/math.sqrt(math.pow(mx-(playerX),2)+math.pow(my-(playerY),2)+0.0001)
        if(my<=playerY):             
            playerAngle = (180/math.pi)*math.acos((mx-(playerX))/math.sqrt(math.pow(mx-(playerX),2)+math.pow(my-(playerY),2)+0.0001))-90
        else:
            playerAngle = -(180/math.pi)*math.acos((mx-(playerX))/math.sqrt(math.pow(mx-(playerX),2)+math.pow(my-(playerY),2)+0.0001))-90

    #scrolling
    if game_state == 1:
        scrollX -= 30*playerX_vel
        if abs(scrollX) > bg_width:
            scrollX = 0
        scrollY -= 30*playerY_vel
        if abs(scrollY) > bg_height:
            scrollY = 0
        if not is_game_over and player_max_vel < 0.95:
            player_max_vel += 0.01
        if is_game_over and player_max_vel > 0:
            player_max_vel -= 0.01

    #missile dyanamics
    if game_state == 1:
        for i in range(number_of_missiles):        
            missileX_acc[i] = missile_max_acc[missileType[i]]*(playerX-missileX[i])/math.sqrt(math.pow(playerX-missileX[i],2)+math.pow(playerY-missileY[i],2)) 
            missileY_acc[i] = missile_max_acc[missileType[i]]*(playerY-missileY[i])/math.sqrt(math.pow(playerX-missileX[i],2)+math.pow(playerY-missileY[i],2))    
            missileX_vel[i] = 15*missileX_vel[i]/16 + missileX_acc[i] - playerX_vel
            missileY_vel[i] = 15*missileY_vel[i]/16 + missileY_acc[i] - playerY_vel
            missileX[i] += missileX_vel[i]
            missileY[i] += missileY_vel[i]
            if i%2==0:
                missile_angle[i] = (missile_angle[i]+6)%360
            else:
                missile_angle[i] = (missile_angle[i]-6)%360     

    #missile-missile collision detection
    if game_state == 1 and not is_game_over:
        for i in range(number_of_missiles):
            for j in range(i+1,number_of_missiles):
                if missileType[i]!=missileType[j]:
                    continue
                if distance(missileX[i],missileY[i],missileX[j],missileY[j]) < 16:
                    explosion((missileX[i]+missileX[j])/2,(missileY[i]+missileY[j])/2)
                    if(missileType[i]==0):
                        score_value += 5
                    elif(missileType[i]==1):
                        score_value += 15
                    missileX[i] = -64
                    missileX[j] = 1606
                    missileY[i] = random.randrange(-64,927,1)
                    missileY[j] = random.randrange(-64,927,1)
                    missileX_vel[i] = missileX_vel[j] = 0
                    missileY_vel[i] = missileY_vel[j] = 0

    if game_state == 1 and not is_game_over and score_value-score_by_twenty*20 > 20 and number_of_missiles<20:
        #add another missile
        score_by_twenty += 1        
        number_of_missiles += 1
    
    #missile-player collision detection
    if game_state == 1 and not is_game_over:
        for i in range(number_of_missiles):
            if distance(missileX[i],missileY[i],playerX,playerY) < 48:
                explosion((missileX[i]+playerX)/2,(missileY[i]+playerY)/2)
                game_over_Sound.play()
                is_game_over = True 
    
    if not is_game_over:
        player(playerAngle)
    if (game_state == 1 or game_state == 2) and not is_game_over:
        for i in range(number_of_missiles):
            missile(missileX[i],missileY[i],missileType[i],missile_angle[i])
    if game_state == 1:
        if is_game_over:
            game_over_text()
            mixer.music.stop()

    #start screen
    if game_state == 0:
        playerAngle = 0
        is_game_over = 0
        mixer.music.stop()
        show_start_screen()

    #help screen
    if game_state == 3:
        show_help_screen()

    #pause screen
    if game_state == 2 and not is_game_over:
        show_pause_screen()

    pygame.display.update()
    
    
pygame.quit()
