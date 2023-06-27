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
bg_images = [] 
for i in range(45):
    image = pygame.image.load(f"art/bg/snowySky{2*i+1}.png").convert()
    bg_images.append(image)
bg_width = bg_images[0].get_width()
bg_height = bg_images[0].get_height()
bg_index = 0
scrollX = 0
scrollY = 0
tilesX = 4
tilesY = 4

#title and icon
pygame.display.set_caption("Shuriken Evasion")
icon = pygame.image.load('art/shurikenRed.png')
pygame.display.set_icon(icon)

#background music
mixer.music.load('sounds/Shepard-tone.mp3')
mixer.music.set_volume(0.5)

#player
playerImg = pygame.image.load('art/paperPlane.png').convert()
playerImg.set_colorkey((0,0,0))
playerX = screen_width/2 
playerY = screen_height/2 
playerX_vel = 0
playerY_vel = 0
playerAngle = 0
player_max_vel = 0
boost_ready = True
last_boost_time = 0
current_time = 0
prev_time = 0
gameplay_pause_time = 0
gameplay_resume_time = 0

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
missile_max_acc.append(1.15)
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
boost_Sound = mixer.Sound('sounds/boost.wav')
game_over_Sound = mixer.Sound('sounds/gameOver.wav')

#score
score_value = 0
score_by_twenty = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 20
textY = 20

#highscore
file = open("highscore.txt", "r+")
highscore = int(file.read())
file.close()

#fonts
over_font = pygame.font.Font('freesansbold.ttf',64)
title_font = pygame.font.Font('fonts/Amatic-Bold.ttf',110)

#game over
is_game_over = False

def game_over_text(time):
    game_over1 = over_font.render("YOU FAILED TO DELIVER",True,(168,0,0))
    game_over2 = over_font.render("THE SECRET CODE!",True,(168,0,0))
    minutes = str(int(time/60000))
    if (int(time/1000))%60 < 10:
        seconds = "0"+str((int(time/1000))%60)
    else:
        seconds = str((int(time/1000))%60)
    survival_time = font.render("Survival Time: " + minutes + ":" + seconds,True,(0,0,0))
    final_score = font.render("Your Final Score is " + str(score_value),True,(0,0,0))
    restart_text = font.render("Press R to Restart",True,(0,0,0))
    escape_text = font.render("Press Esc to quit to Title",True,(0,0,0))
    highscore_text = font.render("High Score: "+str(highscore),True,(0,0,0))
    screen.blit(game_over1,(380,280))
    screen.blit(game_over2,(460,360))
    screen.blit(survival_time,(623,440))
    screen.blit(final_score,(600,490))
    screen.blit(highscore_text,(648,540))
    screen.blit(restart_text,(625,590))
    screen.blit(escape_text,(575,640))

def show_score_and_boost(x,y,z):
    score = font.render("Score : " + str(score_value),True,(0,0,0))
    if z == True:
        boost = font.render("Boost is Ready!",True,(0,0,0))
    else:
        boost = font.render("Boost is Recharging",True,(0,0,0))
    screen.blit(score,(x,y))
    screen.blit(boost,(x+950,y))

def show_start_screen():
    
    start_title = title_font.render("SHURIKEN  EVASION",True,(170,0,0))
    start_text = font.render("Start",True,(255,255,255))
    help_text = font.render("Help",True,(255,255,255))
    exit_text = font.render("Exit",True,(255,255,255))
    
    pygame.draw.rect(screen,(0,0,0),[570,280,400,60],border_radius=15)
    pygame.draw.rect(screen,(0,0,0),[570,550,400,60],border_radius=15)
    pygame.draw.rect(screen,(0,0,0),[570,700,400,60],border_radius=15)
    screen.blit(start_title,(532,110))
    screen.blit(start_text,(728,295))
    screen.blit(help_text,(730,565))
    screen.blit(exit_text,(735,715))
    

def show_help_screen():
    help_title = over_font.render("HELP",True,(0,0,0))
    story_text_1 = font.render("You were on an espionage mission. You successfully stole the secret code and gathered",True,(0,0,0))
    story_text_2 = font.render("important intel, and while returning, you disguised yourself as a paper plane.",True,(0,0,0))
    story_text_3 = font.render("But YOU WERE BEING WATCHED, and your disguise has been compromised.",True,(0,0,0))
    story_text_4 = font.render("EVADE THE ENEMY'S SHURIKENS AT ALL COSTS!",True,(0,0,0))
    controls_text_1 = font.render("Use the mouse cursor to navigate through the skies. Click to Activate Boost.",True,(0,0,0))
    controls_text_2 = font.render("Shuriken of same type destroy each other upon collision and give you points. Press Esc",True,(0,0,0))
    controls_text_3 = font.render("during gameplay to Pause the game and press again to Resume. Good Luck!",True,(0,0,0))
    controls_text_4 = font.render("BEWARE: Black shuriken are fast, but Red ones are even faster!",True,(168,0,0))
    back_text = font.render("Back",True,(255,255,255))
    pygame.draw.rect(screen,(0,0,0),[570,700,400,60],border_radius=15)
    screen.blit(help_title,(690,110))
    screen.blit(back_text,(735,715))
    screen.blit(story_text_1,(80,200))
    screen.blit(story_text_2,(160,250))
    screen.blit(story_text_3,(160,300))
    screen.blit(story_text_4,(380,350))
    screen.blit(controls_text_1,(165,500))
    screen.blit(controls_text_2,(80,550))
    screen.blit(controls_text_3,(160,600))
    screen.blit(controls_text_4,(250,650))

def show_pause_screen():
    resume_text = font.render("Resume",True,(255,255,255))
    back_text = font.render("Back to Title",True,(255,255,255))
    pygame.draw.rect(screen,(0,0,0),[570,220,400,60],border_radius=15)
    pygame.draw.rect(screen,(0,0,0),[570,611,400,60],border_radius=15)
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
        spritesheet = pygame.image.load("art/exp.png")
        sprite_width = spritesheet.get_width()//8
        sprite_height = spritesheet.get_height()//8
        self.images = []
        for num in range(39):
            x_offset = (num%8) * sprite_height
            y_offset = (num//8) * sprite_width
            img = spritesheet.subsurface(pygame.Rect(x_offset, y_offset, sprite_width, sprite_height))
            img = pygame.transform.scale(img, (125, 125))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.counter = 0

    def update(self):
        explosion_speed = 1
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
    collision_Sound.set_volume(0.5)
    collision_Sound.play()

#gamestate: 0-start,1-gameplay,2-pause,3-help
game_state = 0
keyup = False
gameplay_pause_duration_boost = 0
gameplay_pause_duration_score = 0
gameplay_pause_duration_total = 0
hue_shift = 1

#game loop
running = True
while running:

    clock.tick(FPS)
    
    #show and update background
    for i in range(tilesX):
        for j in range(tilesY):
            screen.blit(bg_images[int(bg_index)], ((i-1)*bg_width+scrollX,(j-1)*bg_height+scrollY))
    
    bg_index += 0.1
    if bg_index>=45:
        bg_index = 0
    
    #show score and boost
    if (game_state == 1 or game_state == 2) and not is_game_over:
        show_score_and_boost(textX+100,textY+100,boost_ready)
    
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
                boost_ready = True
                prev_time = pygame.time.get_ticks()
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
                gameplay_start_time = pygame.time.get_ticks()
                gameplay_pause_duration_total = 0
            if event.key == pygame.K_ESCAPE:
                if not is_game_over:
                    gameplay_pause_time = pygame.time.get_ticks()
                    keyup = False
                    game_state = 2
                else:
                    game_state = 0
        
        if game_state == 1 and not is_game_over and event.type == pygame.MOUSEBUTTONDOWN and boost_ready:
            player_max_vel = 2
            boost_Sound.set_volume(0.5)
            boost_Sound.play()
            last_boost_time = pygame.time.get_ticks()
            boost_ready = False
        
        if game_state == 2:            
            if keyup and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if is_game_over:
                    game_state = 0
                else:
                    gameplay_resume_time = pygame.time.get_ticks()
                    gameplay_pause_duration_boost += gameplay_resume_time-gameplay_pause_time
                    gameplay_pause_duration_score += gameplay_resume_time-gameplay_pause_time
                    gameplay_pause_duration_total += gameplay_resume_time-gameplay_pause_time
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
                        boost_ready = True
                        prev_time = pygame.time.get_ticks()
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
                        gameplay_start_time = pygame.time.get_ticks()
                        gameplay_pause_duration_total = 0
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
        if not is_game_over and player_max_vel > 0.95:
            player_max_vel -= 0.04
        if not is_game_over and player_max_vel < 0.95:
            player_max_vel += 0.01
        if is_game_over and player_max_vel > 0:
            player_max_vel -= 0.01
        current_time = pygame.time.get_ticks()
        if not is_game_over:
            if current_time - last_boost_time - gameplay_pause_duration_boost > 5000:
                boost_ready = True
                gameplay_pause_duration_boost = 0
            if current_time - prev_time - gameplay_pause_duration_score > 2500:
                score_value += 1;
                prev_time = current_time
                gameplay_pause_duration_score = 0

    #scrolling
    if game_state == 1:
        scrollX -= 30*playerX_vel
        if abs(scrollX) > bg_width:
            scrollX = 0
        scrollY -= 30*playerY_vel
        if abs(scrollY) > bg_height:
            scrollY = 0

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
                missile_angle[i] = (missile_angle[i]+8)%360
            else:
                missile_angle[i] = (missile_angle[i]-8)%360     

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
                gameplay_end_time = pygame.time.get_ticks()
                is_game_over = True 
    
    if not is_game_over:
        player(playerAngle)
    if (game_state == 1 or game_state == 2) and not is_game_over:
        for i in range(number_of_missiles):
            missile(missileX[i],missileY[i],missileType[i],missile_angle[i])
    if game_state == 1:
        if is_game_over:
            if highscore < score_value:
                file = open("highscore.txt", "r+")
                highscore = score_value
                file.seek(0)
                file.write(str(score_value))
                file.close()
            game_over_text(gameplay_end_time-gameplay_start_time-gameplay_pause_duration_total)
            mixer.music.stop()

    #game states : 0(start screen), 1(gameplay/gameover), 2(pause), 3(help screen), 

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
