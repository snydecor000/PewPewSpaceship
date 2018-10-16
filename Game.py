# Sprite Sheet Animation Demo
x = 0
y = 25
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

import pygame, sys, random, math
from pygame.locals import *
#initialize pygame
pygame.init()

red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
purple = (150,0,150)
white = (255,255,255)
black = (0,0,0)
aqua = (0,255,255)
lGreen = (40, 193, 56)
brown = (139,69,19)
grass = (13, 112, 23)
yellow = (255,255,0)
gray = (107,107,107)

##########################################
class SpriteSheetImage(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self) #extend the base Sprite class
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.health = 3
        self.xS = 0
        self.yS = 0
        self.salvage = 0
        self.speed = 5

    #X property
    def _getx(self): return self.rect.x
    def _setx(self,value): self.rect.x = value
    X = property(_getx,_setx)

    #Y property
    def _gety(self): return self.rect.y
    def _sety(self,value): self.rect.y = value
    Y = property(_gety,_sety)

    #position property
    def _getpos(self): return self.rect.topleft
    def _setpos(self,pos): self.rect.topleft = pos
    position = property(_getpos,_setpos)

    def getImage(self): return self.image

    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0,0,width,height)
        self.columns = columns
        #try to auto-calculate total frames
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def move(self):
        self.X += self.xS
        self.Y += self.yS

    def update(self, current_time, rate=30):
        #update animation frame number
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        #build current frame only if it changed
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self) #extend the base Sprite class
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.xS = 0
        self.yS = 0
        self.angle = 0
        self.speed = 0

    #X property
    def _getx(self): return self.rect.x
    def _setx(self,value): self.rect.x = value
    X = property(_getx,_setx)

    #Y property
    def _gety(self): return self.rect.y
    def _sety(self,value): self.rect.y = value
    Y = property(_gety,_sety)

    #position property
    def _getpos(self): return self.rect.topleft
    def _setpos(self,pos): self.rect.topleft = pos
    position = property(_getpos,_setpos)

    def getImage(self): return self.image

    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0,0,width,height)
        self.columns = columns
        #try to auto-calculate total frames
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=30):
        self.X += self.xS
        self.Y += self.yS

        #build current frame only if it changed
        rect = Rect(0, 0, self.frame_width, self.frame_height)
        self.image = self.master_image.subsurface(rect)
        self.image = rot_center2(self.image,self.angle)


def rot_center(image, angle):
    image = pygame.transform.scale(image,(150,150))
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def rot_center2(image, angle):
    loc = image.get_rect().center  #rot_image is not defined 
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite
def pews():
    pew.play()
##########################################
white = (255,255,255)
black = (0,0,0)

width = 1600
height = 800

SCREEN = pygame.display.set_mode((width,height),0,32)
pygame.display.set_caption("Sprite Sheet Demo")

pew = pygame.mixer.Sound("Pew.ogg")
pew.set_volume(0.3)
clok = pygame.mixer.Sound("clock.ogg")
inter = pygame.mixer.Sound("05 Come and Find Me.ogg")
inter.set_volume(0.5)
instruct = pygame.mixer.Sound("08 Ascending.ogg")
instruct.set_volume(0.6)
gameM = pygame.mixer.Sound("Space Trip.ogg")
gameM.set_volume(0.5)
titleS = pygame.mixer.Sound("10 Arpanauts.ogg")
titleS.set_volume(0.3)

clock = pygame.time.Clock()
ticks = pygame.time.get_ticks()

back = pygame.image.load("spaceBackground.png")
back2 = pygame.image.load("space3small.png")
back2 = pygame.transform.scale(back2,(1600,900))

shooterCounter = 10000
pewS = False

lazer = SpriteSheetImage(SCREEN)
lazer.load("lazer.png",10,20,1)##picture,width,height,cols
lazerGroup = pygame.sprite.Group()
lazerGroup.add(lazer)
lazer.position = -300,-300
lazer.frame = 0
lazer.first_frame = 0
lazer.last_frame = 0

ship = SpriteSheetImage(SCREEN)
ship.load("shipNew2.png",73,73,11)##picture,width,height,cols
shipGroup = pygame.sprite.Group()
shipGroup.add(ship)
ship.position = 400,400
ship.frame = 0
ship.first_frame = 0
ship.last_frame = 0

EshipGroup = pygame.sprite.Group()

wrenchGroup = pygame.sprite.Group()

maxSpeed = 10#10
acceleration = 0.5#0.5
spaceAccel = 0.05#0.05
xS = 0
yS = 0

keyLeft = False
keyRight = False
keyUp = False
keyDown = False

font = pygame.font.Font("Minecraft.ttf",150)
font2 = pygame.font.Font("Minecraft.ttf",25)
font3 = pygame.font.Font("Minecraft.ttf",40)
title = font.render("PEW PEW Spaceship",1,white)
text1 = font2.render("Instructions",1,white)
text2 = font2.render("<-------Back",1,white)
text3 = font3.render("Use the W A S D keys on the keyboard to move your spaceship",1,white)
text4 = font3.render("Use the mouse one button to fire lazers",1,white)
text5 = font3.render("Use the mouse movement to aim your spaceship",1,white)
text6 = font2.render("     Start    ",1,white)
text7 = font3.render("Salvage: ",1,green)
text8 = font3.render("Collect green wrenches to gain salvage",1,green)
text9 = font3.render("You lose health when an enemy ship hits you",1,green)
text10 = font3.render("If you lose all of your salvage, you lose",1,green)
text11 = font3.render("Use salvage to upgrade your ship",1,green)
text12 = font2.render("Cost: 30",1,white)
text13 = font2.render("Shooter Speed",1,white)
text16 = font3.render("Shoot the boxes to upgrade your ship",1,white)
wasd = pygame.image.load("wasd2.png")
mouse = pygame.image.load("mouse.png")
mouse = pygame.transform.scale(mouse,(200,200))
SCREEN.blit(title,(75,350))
screen = "title"
titleS.play()
edge = True

count = 1600
count2 = 0

stage = 3
stageActual = 1
eCount = 0
respawnTimer = 0
respawnMin = 80
wave = 10

shootSpeed = 0
salvageDeduct = 0
ship.salvage = 0

shootYes = False

easter = 0
easterB = False
easterComplete = False

numShots = 1
oddOffset = [0,15,-15,30,-30,45,-45,60,-60,75,-75,90,-90,105,-105,120,-120,135,-135,150,-150,165,-165,180,-180]
cost1 = 20
cost2 = 100

trishot = True
speedShot = True

ship.health = 2
rainbow = True

while True:
    if(rainbow and shootSpeed >=30):
        rainbow=False
        ship.frame = 1
        ship.first_frame = 1
        ship.last_frame = 10
    elif(shootSpeed <30):
        ship.frame = 0
        ship.first_frame = 0
        ship.last_frame = 0
    
    if(stageActual < 5):
        respawnMin = 80 - ((stageActual-1)*5)
    else:
        respawnMin = 80 - ((stageActual-1)*10)
    SCREEN.fill((0,0,0))
    if(edge):
        edge = False
        ship.X = width/2 - 75
        ship.Y = height/2 - 75
##        xS = 0
##        yS = 0
        for e in wrenchGroup:
            e.kill()
    if(pewS):
        pews()
    shooterCounter+=1
    

    if screen == "title":
        for e in EshipGroup:
            e.kill()
        for e in wrenchGroup:
            e.kill()
        SCREEN.blit(back,(0,0))
        pygame.draw.rect(SCREEN,blue,(0,0,200,150),0)
        pygame.draw.rect(SCREEN,green,(width-200,0,200,150),0)
        SCREEN.blit(text1,(25,65))
        SCREEN.blit(title,(80,350))
        SCREEN.blit(text6,(width - 200 + 25,65))
        if(ship.X < 180 and ship.Y < 120):
            screen = "instructions"
            titleS.stop()
            instruct.play()
            edge = True
        if(ship.X + 150 > width - 180 and ship.Y < 120):
            screen = "begTrans"
            titleS.stop()
    elif screen == "instructions":
        SCREEN.blit(back,(0,0))
        pygame.draw.rect(SCREEN,red,(0,0,200,150),0)
        SCREEN.blit(text2,(25,65))
        SCREEN.blit(wasd,(10,210))
        SCREEN.blit(text3,(10,360))
        SCREEN.blit(mouse,(10,400))
        SCREEN.blit(text4,(10,610))
        SCREEN.blit(text5,(10,660))
        SCREEN.blit(text8,(370,50))
        SCREEN.blit(text9,(320,100))
        SCREEN.blit(text10,(370,150))
        SCREEN.blit(text11,(420,200))
        if(ship.X < 180 and ship.Y < 120):
            titleS.play()
            screen = "title"
            edge = True
            instruct.stop()
    elif screen == "begTrans":
        wave = 10
        backR = rot_center2(back,count2)
        SCREEN.blit(backR,(0,0))
        count -= 5
        count2 += 2
        back = pygame.transform.scale(back,(count,int(count/2)))

        if(count < 5):
            screen = "game"
            gameM.play()
    elif screen == "game":
        speedShot = True
        SCREEN.blit(back2,(0,0))
        text71 = font3.render("Salvage " + str(ship.salvage),1,green)
        text81 = font3.render("Ships Remaining " + str(wave),1,(135,206,250))
        text20 = font3.render("Stage " + str(stageActual),1,(135,206,250))
        text25 = font3.render("Health " + str(ship.health),1,(255,86,86))
        SCREEN.blit(text20,(width-300,755))
        SCREEN.blit(text25,(width-660,755))
        SCREEN.blit(text71,(5,755))
        SCREEN.blit(text81,(350,755))
        eCount = 0
        respawnTimer += 1
        for e in EshipGroup:
            e.move()
            eCount += 1
        if(respawnTimer > respawnMin):
            respawnTimer = 0
            if(eCount < wave):
                Eship2 = SpriteSheetImage(SCREEN)
                Eship2.load("ufo.png",110,32,3)##picture,width,height,cols
                EshipGroup.add(Eship2)
                randomInt = random.randint(0,3)
                if randomInt == 0:
                   Eship2.position = -150,random.randint(0,height)
                elif randomInt == 1:
                   Eship2.position = width+150,random.randint(0,height)
                elif randomInt == 2:
                   Eship2.position = random.randint(0,width),-50
                else:
                   Eship2.position = random.randint(0,width),height + 10
        if wave == 0:
            trishot = False
            speedShot = False
            gameM.stop()
            ship.salvage += 10
            for l in lazerGroup:
                l.kill()
            stage -= 1
            stageActual += 1
            wave = stageActual*10
            screen = "upgrade"
            speedShot = False
            inter.play()
            edge = True
    elif screen == "upgrade":
        trishot = False
        SCREEN.fill((0,0,0))
        text7 = font3.render("Salvage " + str(ship.salvage),1,green)
        SCREEN.blit(text7,(640,755))
        SCREEN.blit(text16,(440,100))
        pygame.draw.rect(SCREEN,blue,(0,0,200,150),0)
        pygame.draw.rect(SCREEN,red,(width-200,0,200,150),0)
        pygame.draw.rect(SCREEN,red,(width-200,300,200,150),0)
        SCREEN.blit(text6,(25,65))
        text17 = font2.render("Cost: "+str(int(cost2)),1,white)
        text18 = font2.render("Lazer Spread",1,white)
        text19 = font2.render("("+str(int(numShots))+")",1,white)
        SCREEN.blit(text17,(width-150,320))
        SCREEN.blit(text18,(width-190,360))
        SCREEN.blit(text19,(width-110,400))
        text12 = font2.render("Cost: "+str(int(cost1)),1,white)
        SCREEN.blit(text12,(width-150,20))
        SCREEN.blit(text13,(width-190,60))
        text14 = font2.render("("+str(int(shootSpeed))+")",1,white)
        SCREEN.blit(text14,(width-110,100))
        if(ship.X < 180 and ship.Y < 120):
            gameM.play()
            screen = "game"
            trishot = True
            edge = True
            inter.stop()
        for l in lazerGroup:
            if l.X > width-200 and l.Y < 150:
                l.kill()
                if ship.salvage >= cost1:
                    ship.salvage -= cost1
                    cost1+= 5
                    if(shootSpeed < 7):
                        shootSpeed += 3
                    elif(shootSpeed < 18):
                        shootSpeed += 2
                    elif(shootSpeed < 30):
                        shootSpeed += 1
                        
                    
            if l.X > width-200 and l.Y > 300 and l.Y < 450:
                l.kill()
                if ship.salvage >= cost2 and numShots < 25:
                    ship.salvage -= cost2
                    cost2+= 100
                    numShots += 2

    shipGroup.update(ticks,50)
    lazerGroup.update(ticks,50)
    lazerGroup.draw(SCREEN)
    EshipGroup.update(ticks,50)
    EshipGroup.draw(SCREEN)
    wrenchGroup.update(ticks,50)
    wrenchGroup.draw(SCREEN)
####################################################  Collision Detection
    for l in lazerGroup:
        attacker = None
        attacker = pygame.sprite.spritecollideany(l, EshipGroup)
        if attacker != None:
            if pygame.sprite.collide_rect(l,attacker):
                l.kill()
                l.remove()
                attacker.health -= stage
    
    shipRect = Rect(ship.X,ship.Y,150,150)
    for e in EshipGroup:
        if shipRect.contains(e.rect):
            e.health = 0
            ship.health -= 1
            if ship.health < 1:
                gameM.stop()
                count = 1600
                count2 = 0
                numShots = 1
                back = pygame.image.load("spaceBackground.png")
                screen = "title"
                titleS.play()
                wave = 10
                stage = 3
                stageActual = 1
                ship.salvage = 0
                shootSpeed = 0
                ship.health = 2
                cost1 = 20
                cost2 = 100

    for e in wrenchGroup:
        if shipRect.contains(e.rect):
            e.kill()
            ship.salvage += 10

    if(stage < 1):
        stage = 1
    for e in EshipGroup:
        e.speed = 5
        if e.health == 3:
            e.frame = 0 + ((stage-1)*3)
            e.first_frame = 0 + ((stage-1)*3)
            e.last_frame = 0 + ((stage-1)*3)
        elif e.health == 2:
            e.frame = 1 + ((stage-1)*3)
            e.first_frame = 1 + ((stage-1)*3)
            e.last_frame = 1 + ((stage-1)*3)
        elif e.health == 1:
            e.frame = 2 + ((stage-1)*3)
            e.first_frame = 2 + ((stage-1)*3)
            e.last_frame = 2 + ((stage-1)*3)
        elif e.health <= 0:
            wrench = SpriteSheetImage(SCREEN)
            wrench.load("wrench.png",14,40,2)##picture,width,height,cols
            wrenchGroup.add(wrench)
            wrench.position = (e.position[0]+50,e.position[1]+5)
            wrench.frame = 1
            wrench.first_frame = 1
            wrench.last_frame = 1
            wave -= 1
            clok.play()
            e.kill()
            
####################################################   Movement
    if(xS > -maxSpeed and keyLeft):
        xS -= acceleration
    elif keyLeft:
        xS = -maxSpeed
    if(xS < maxSpeed and keyRight):
        xS += acceleration
    elif keyRight:
        xS = maxSpeed
    if(yS > -maxSpeed and keyUp):
        yS -= acceleration
    elif keyUp:
        yS = -maxSpeed
    if(yS < maxSpeed and keyDown):
        yS += acceleration
    elif keyDown:
        yS = maxSpeed

        
    if(xS != 0 and xS > 0 and not keyRight):
        xS -= spaceAccel
    if(xS != 0 and xS < 0 and not keyLeft):
        xS += spaceAccel
    if(yS != 0 and yS > 0 and not keyDown):
        yS -= spaceAccel
    if(yS != 0 and yS < 0 and not keyUp):
        yS += spaceAccel
    ship.X += xS
    ship.Y += yS

    if(ship.Y < -20):
        yS *= -1
    if(ship.Y > height - 120):
        yS *= -1
    if(ship.X > width - 120):
        xS *= -1
    if(ship.X < -20):
        xS *= -1

    if(screen == "game"):
        for e in EshipGroup:
            angle3 = 180+math.atan2(ship.X-e.X,ship.Y+50-e.Y)*180/math.pi
            e.xS = -math.sin(angle3*math.pi/180)*4
            e.yS = -math.cos(angle3*math.pi/180)*3
##            if(e.xS > -maxSpeed and e.xS):
##                xS -= acceleration
##            elif keyLeft:
##                xS = -maxSpeed
##            if(e.xS < maxSpeed and keyRight):
##                xS += acceleration
##            elif keyRight:
##                xS = maxSpeed
##            if(e.yS > -maxSpeed and keyUp):
##                yS -= acceleration
##            elif keyUp:
##                yS = -maxSpeed
##            if(e.yS < maxSpeed and keyDown):
##                yS += acceleration
##            elif keyDown:
##                yS = maxSpeed            
    
    pos = pygame.mouse.get_pos()
    angle = 180+math.atan2(pos[0]-ship.X-75,pos[1]-ship.Y-75)*180/math.pi
    rotimage = rot_center(ship.getImage(),angle)
    SCREEN.blit(rotimage,(ship.X,ship.Y))
###############################################################################
##    attacker = None
##    attacker = pygame.sprite.spritecollideany(ship, evilGroup)
##    if attacker != None:
##        if pygame.sprite.collide_rect_ratio(0.5)(player,attacker):
##            print("hit")
##            attacker.kill()

    for l in lazerGroup:
        if(l.position[0] > width):
            l.kill()
        if(l.position[1] > height):
            l.kill()
        if(l.position[0] < -50):
            l.kill()
        if(l.position[1] < -50):
            l.kill()

###############################################################################    for event in pygame.event.get():
    temp2 = shootSpeed
    if(not speedShot):
        shootSpeed = 10
    if shootYes:
        if(shooterCounter > 30-shootSpeed):
            shooterCounter = 0
            temp = numShots
            e = []
            x = 0
            if(not trishot):
                numShots = 1
            while x < numShots:
                PLazer = Projectile(SCREEN)
                PLazer.load("lazer.png",10,20,1)
                PLazer.position = ship.X+70,ship.Y+75
                PLazer.speed = 20
                PLazer.frame = 0
                PLazer.first_frame = 0
                PLazer.last_frame = 0
                e.append(PLazer)
                x += 1
            lazerGroup.add(e)
            m_pos = pygame.mouse.get_pos()
            angle5 = 180+math.atan2(m_pos[0]-e[0].X+5,m_pos[1]-e[0].Y+10)*180/math.pi
            y = 0
            while y < numShots:
                e[y].angle = angle5 + oddOffset[y]
                e[y].xS = -math.sin(e[y].angle*math.pi/180)*e[y].speed
                e[y].yS = -math.cos(e[y].angle*math.pi/180)*e[y].speed
                y+= 1
            pew.play()
            numShots = temp
    shootSpeed = temp2
    if(easter >6 and easterB):
        easterComplete = True

    if easterComplete:
        shootSpeed = 9001
            
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(pygame.mouse.get_pressed()[0] == True):
                shootYes = True
        if event.type == pygame.MOUSEBUTTONUP:
            shootYes = False
        if event.type == pygame.KEYDOWN:
            if(event.key == K_a or event.key == K_LEFT):
                keyLeft = True
            elif(event.key == K_d or event.key == K_RIGHT):
                keyRight = True
            elif(event.key == K_w or event.key == K_UP):
                keyUp = True
            elif(event.key == K_s or event.key == K_DOWN):
                keyDown = True
            elif(event.key == K_p):
                pewS = True
            if(event.key == K_KP8 and easter == 1):
                easterB = True
            elif(easter == 1):
                easterB = False
            elif(event.key == K_KP8 and easter != 0):
                easter = 0
                easterB = True
            if(event.key == K_KP2 and easter == 2):
                easterB = True
            elif(easter == 2):
                easterB = False
            if(event.key == K_KP2 and easter == 3):
                easterB = True
            elif(easter == 3):
                easterB = False
            if(event.key == K_KP4 and easter == 4):
                easterB = True
            elif(easter == 4):
                easterB = False
            if(event.key == K_KP6 and easter == 5):
                easterB = True
            elif(easter == 5):
                easterB = False
            if(event.key == K_KP4 and easter == 6):
                easterB = True
            elif(easter == 6):
                easterB = False
            if(event.key == K_KP6 and easter == 7):
                easterB = True
            elif(easter == 7):
                easterB = False
            easter += 1
            if(event.key == K_t):
                shootSpeed += 1
        elif(event.type == pygame.KEYUP):
            if(event.key == K_a or event.key == K_LEFT):
                keyLeft = False
            elif(event.key == K_d or event.key == K_RIGHT):
                keyRight = False
            elif(event.key == K_w or event.key == K_UP):
                keyUp = False
            elif(event.key == K_s or event.key == K_DOWN):
                keyDown = False
            elif(event.key == K_p):
                pewS = False
       


    clock.tick(60)
    ticks = pygame.time.get_ticks()
    pygame.display.update()
