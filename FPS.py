import pygame,random
from pygame.locals import *
import pyganim
from math import *
pygame.init()
window=pygame.display.set_mode((600,400))
isRunning=True
clock=pygame.time.Clock()

def count_fps():
    global FPS
    global delta
    FPS=clock.get_fps()
    if FPS>0:
        delta=1/FPS

def posfinder():
    x,y=pygame.mouse.get_pos()
    return x,y

def EnemyPos():
    x=random.choice([320,398,502,636])
    return (x,400)

class Timer:
    def __init__(self):
        self.start=int(pygame.time.get_ticks())
        self.seconds=0
    def timing(self):
        self.seconds=int((pygame.time.get_ticks()-self.start)/1000)
        return self.seconds
    def reset(self):
        self.start=int(pygame.time.get_ticks())

myTimer=Timer()
font=pygame.font.SysFont("Verdana.ttf", 20)
pos = []
bitmap=pygame.image.load("forest.png").convert_alpha()
bitmap=pygame.transform.scale(bitmap,(1000,800))
window.blit(bitmap,(-200,-200))
gun=pygame.image.load("pistol.png").convert_alpha()
gun=pygame.transform.scale(gun,(108,127))
guny=300
fire=pyganim.PygAnimation([("pistolfire/frame_1.gif",200),("pistolfire/frame_2.gif",100),("pistolfire/frame_3.gif",100),("pistolfire/frame_4.gif",200),("pistolfire/frame_5.gif",200)])
fire.loop=False
#pygame.mouse.set_visible(False)
pistolsound=pygame.mixer.Sound("sounds/pistolsound.wav")
enemy=pyganim.PygAnimation([("enemy/0.png",150),("enemy/1.png",150),('enemy/2.png',150),('enemy/3.png',150),('enemy/4.png',150),('enemy/5.png',150),('enemy/6.png',150),('enemy/7.png',150),('enemy/8.png',150)])
origsize=[50,80]
size=[50,80]
WalkTime=Timer()
enemy.loop=False
def Walking(sze,factor):
    if WalkTime.timing()==1:
        sze[0]+=factor
        sze[1]+=factor
        WalkTime.reset()
enmyspawn=False
enplist=set()
spawn=False
spawned=[]
keepblit=True
shot=pygame.Surface((18,20))
enemies = [enemy, enemy, enemy, enemy]
shot.fill((0,0,0))
shotx=453
shoty=280
while isRunning:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: # Checks if Quit Pressed
            isRunning=False
            break
        if event.type==pygame.MOUSEMOTION: #Checks Mouse movement
            pos=posfinder() #  Finds Cursor Position
            if pos[0]<300 : #Sets Background Blit Position
                scrposx = -pos[0]+110
                shotx=ceil((pos[0]*0.55)+287.5)
            elif pos[0]==300:   # "
                scrposx = -200
            elif pos[0]>300 :   # "
                scrposx = (-pos[0]+100)-10
            if pos[1]>200 : # "
                scrposy = -pos[1]-10
            elif pos[1]==200:   # "
                scrposy = -200
            elif pos[1]<200 :   # "
                scrposy = -pos[1] + 10
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
        if event.type==pygame.MOUSEBUTTONDOWN: # Gets Mouse Clicks
            print(posfinder())
            gunx,guny = posfinder()
            for i in range(0,len(spawned)):
                enemyCurrentW,enemyCurrentH = size#[0] - origsize[0],size[1] - origsize[1]
                xLB = spawned[i][0]
                xHB = spawned[i][0]+enemyCurrentW
                yLB = spawned[i][1]
                yHB = spawned[i][1]+enemyCurrentH
                if xLB<gunx<xHB and yLB<guny<yHB:
                    del spawned[i]
                    del enemies[i]
                    #enemies.append(enemy)
            fire.stop()
            fire.play() # Pistol firing Anim
            pistolsound.play()
            pygame.display.update()
        if pygame.mouse.get_focused(): # Gets if Cursor in Screen
            scrnout=False
        elif not pygame.mouse.get_focused(): #Gets if Cursor out of screen
            scrnout=True
            fire.stop()
    if pos[0]<10:                           #Sets Mouse Cursor Boundaries
        pygame.mouse.set_pos(10,pos[1])
    elif pos[0]>590:                        # "
        pygame.mouse.set_pos(590,pos[1])
    if pos[1]<10:                           # "
        pygame.mouse.set_pos(pos[0],10)
    elif pos[1]>390:                        # "
        pygame.mouse.set_pos(pos[0],390)
    if scrposx<-400:               #Camera Move Effect Boundaries
        scrposx=-400
    elif scrposx>0:                 # "
        scrposx=0
    if scrposy<-400:                # "
        scrposy=-400
    elif scrposy>0:                 # "
        scrposy=0
    myTimer.timing() # Timer Ticks
    WalkTime.timing()  #Timing the Walk
    ensurf=pygame.Surface((1000,800),HWSURFACE|SRCALPHA) # Creates Surface To blit Enemy Onto
    window.blit(bitmap,(scrposx,scrposy))
    Walking(size,4)
    print("This is size",size)
    if not enmyspawn : # returns list of random enemy pos
        enpos=EnemyPos()
        enplist.add(enpos)
        if len(enplist)>=4: # Checks if Enemy Positions are Four
            enmyspawn=True
            spawn=True
    if spawn: #checks if enemies need to be spawned
        if len(enplist)>0 and myTimer.timing() % 5 == 0 and len(spawned)<4:
            elem=enplist.pop()
            spawned.append(elem)
            print(elem)
            print (spawned)
        if len(enplist)==0:
            enmyspawn=False
            spawn=False
    if keepblit and len(spawned)>0: #Checks if Enemies need to Be blit
        if len(spawned)== 4 :
            enemies[0].smoothscale((size[0],size[1]))
            enemies[1].smoothscale((size[0], size[1]))
            enemies[2].smoothscale((size[0], size[1]))
            enemies[3].smoothscale((size[0], size[1]))
            enemies[0].blit(ensurf,spawned[0])
            enemies[1].blit(ensurf,spawned[1])
            enemies[2].blit(ensurf,spawned[2])
            enemies[3].blit(ensurf,spawned[3])
            enemies[0].play()
            enemies[1].play()
            enemies[2].play()
            enemies[3].play()
        elif len(spawned)==3:
            enemies[0].smoothscale((size[0], size[1]))
            enemies[1].smoothscale((size[0], size[1]))
            enemies[2].smoothscale((size[0], size[1]))
            enemies[0].blit(ensurf,spawned[0])
            enemies[1].blit(ensurf,spawned[1])
            enemies[2].blit(ensurf,spawned[2])
            enemies[0].play()
            enemies[1].play()
            enemies[2].play()
        elif len(spawned)==2:
            enemies[0].smoothscale((size[0], size[1]))
            enemies[1].smoothscale((size[0], size[1]))
            enemies[0].blit(ensurf,spawned[0])
            enemies[1].blit(ensurf,spawned[1])
            enemies[0].play()
            enemies[1].play()
        elif len(spawned)==1:
            enemies[0].smoothscale((size[0], size[1]))
            enemies[0].blit(ensurf,spawned[0])
            enemies[0].play()
    ensurf.blit(shot, (shotx, shoty))
    window.blit(gun, (248, guny))
    window.blit(ensurf,(scrposx,scrposy))

    fire.blit(window, (230, 240))
    del ensurf
    if scrnout:
        guny+=1
    elif not scrnout:
        guny-=1
    if guny<275:
        guny=275
    elif guny>400:
        guny=400
    count_fps()
    Fps=font.render(str(FPS),True,(255,255,255))
    window.blit(Fps,(0,0))
    clock.tick(200)
    pygame.display.update()
pygame.quit()

