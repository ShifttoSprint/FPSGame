import pygame,random
from pygame.locals import *
import pyganim
from Enemy import *
from math import *

pygame.init()
window=pygame.display.set_mode((600,400))
isRunning=True
clock=pygame.time.Clock()
#TODO
#1. Clean up the code, and put stuff into objects
#2. Figure out translation of enemies - Done
#3. Maybe add a menu and health bar and stuff

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
    def timing_with_precision(self, precision):
        self.seconds=int((pygame.time.get_ticks()-self.start)/precision)
        return self.seconds
    def reset(self):
        self.start=int(pygame.time.get_ticks())

myTimer=Timer()
font=pygame.font.SysFont("Verdana.ttf", 20)
pos = []
screen_size = window.get_size()
scrposx = -200
scrposy = -200
pygame.mouse.set_pos([screen_size[0]/2, screen_size[1]/2])
bitmap=pygame.image.load("forest.png").convert_alpha()
bitmap=pygame.transform.scale(bitmap,(1000,800))
window.blit(bitmap,(-200,-200))
gun=pygame.image.load("pistol.png").convert_alpha()
gun=pygame.transform.scale(gun,(108,127))
guny=300
fire=pyganim.PygAnimation([("pistolfire/frame_1.gif",200),("pistolfire/frame_2.gif",100),("pistolfire/frame_3.gif",100),("pistolfire/frame_4.gif",200),("pistolfire/frame_5.gif",200)])
fire.loop=False
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

pistolsound=pygame.mixer.Sound("sounds/pistolsound.wav")
origsize=[50,80]
size=[50,80]
WalkTime=Timer()

def Walking(sze,factor):
    if WalkTime.timing()==1:
        sze[0]+=factor
        sze[1]+=factor
        WalkTime.reset()

enmyspawn=False
enplist=set()
spawn=True
spawned=[]
delta_pos = [0,0]
keepblit=True
shot=pygame.Surface((18,20))
enemies = [Enemy(), Enemy(), Enemy(), Enemy()]
shot.fill((0,0,0))
shotx=453
shoty=280
oldpos=[]
MouseMovementTimer = Timer()
enemy_colliders = list()
scale = -2
global gun_collider
gun_collider = pygame.Rect(299, 275, 5, 5)
while isRunning:
    try:
        for event in pygame.event.get():
            if event.type==pygame.QUIT: # Checks if Quit Pressed
                isRunning=False
                break
            if event.type==pygame.MOUSEMOTION: #Checks Mouse movement
                
                delta_pos = pygame.mouse.get_rel() #Get Direction of mouse movement
                delta_pos = [float(delta_pos[0]), float(delta_pos[1])] #Floating the values for precision
                scrposx+=delta_pos[0]*scale #Setting screen X axis movement
                scrposy+=delta_pos[1]*scale #Setting screen Y axis movement
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                isRunning = False
            if event.type==pygame.MOUSEBUTTONDOWN: # Gets Mouse Clicks
                for i in range(len(enemy_colliders)):
                    if enemy_colliders[i].colliderect(gun_collider):
                        del enemy_colliders[i]
                        del enemies[i]
                        break
                        
                """for i in range(0,len(spawned)):
                    enemyCurrentW,enemyCurrentH = size#[0] - origsize[0],size[1] - origsize[1]
                    xLB = spawned[i][0]
                    xHB = spawned[i][0]+enemyCurrentW
                    yLB = spawned[i][1]
                    yHB = spawned[i][1]+enemyCurrentH
                    if xLB<gunx<xHB and yLB<guny<yHB:
                        del spawned[i]
                        del enemies[i]
                        #enemies.append(enemy)"""
                fire.stop()
                fire.play() # Pistol firing Anim
                pistolsound.play()
                pygame.display.update()
            if pygame.mouse.get_focused(): # Gets if Cursor in Screen
                scrnout=False
            elif not pygame.mouse.get_focused(): #Gets if Cursor out of screen
                scrnout=True
        enemy_colliders.clear()    
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
        pos=posfinder() #  Finds Cursor Position
        if pos==oldpos:
            if MouseMovementTimer.timing() == 3:
                scrnout = True
        else:
            MouseMovementTimer.reset()
            scrnout = False
        oldpos=pos
        ensurf=pygame.Surface((1000,800),HWSURFACE|SRCALPHA) # Creates Surface To blit Enemy Onto
        window.blit(bitmap,(scrposx,scrposy))
        Walking(size,4)
        #print("This is size",size)
        
        if len(enemies)>0: #Checks if Enemies need to Be blit
            for i in range(len(enemies)):
                enemies[i].anim.smoothscale((size[0],size[1]))
                enemies[i].anim.blit(ensurf,enemies[i].pos)
                enemies[i].update_collider(scrposx,scrposy)
                pygame.draw.rect(window, (255, 0, 0), enemies[i].collider, 2)
                enemy_colliders.append(enemies[i].collider)
                enemies[i].anim.play()
                
        ensurf.blit(shot, (shotx, shoty))
        window.blit(ensurf,(scrposx,scrposy))
        window.blit(gun, (248, guny))
        pygame.draw.rect(window, (255, 255, 255), gun_collider, 2)

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
    except Exception as e:
        print(e)
        if str(e) == "video system not initialized":
            exit()
        pygame.quit()
pygame.event.set_grab(False)
pygame.quit()

