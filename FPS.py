import pygame,random
from pygame.locals import *
import pyganim
from Weapon import *
from Enemy import *
from math import *
from Timer import *

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
gun=pygame.image.load("weapons/pistol.png").convert_alpha()
gun=pygame.transform.scale(gun,(108,127))
guny=300
fire=pyganim.PygAnimation([("weapons/frame_1.gif",200),("weapons/frame_2.gif",100),("weapons/frame_3.gif",100),("weapons/frame_4.gif",200),("weapons/frame_5.gif",200)])
fire.loop=False
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

pistolsound=pygame.mixer.Sound("sounds/pistolsound.wav")
old_size=[0,0]
WalkTime=Timer()

def Walking(sze,factor):
    if WalkTime.timing()>=3:
        sze[0]+=factor
        sze[1]+=factor
        WalkTime.reset()
    return sze

enmyspawn=False
enplist=set()
spawn=True
spawned=[]
delta_pos = [0,0]
keepblit=True
enemies = [Enemy(), Enemy(), Enemy(), Enemy()]
size=[50,80]
oldpos=[]
MouseMovementTimer = Timer()
FireRateTimer = Timer()
scale = -2
global gun_collider
gun_collider = pygame.Rect(299, 275, 5, 5)
gun_fire_rate = 625
gun_firing_already = False
while isRunning:
    try:
        for event in pygame.event.get(): #Checking Event Queue
            #Event Queue Code Starts Here ---------------------------------------------------------------
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
                
            if event.type==pygame.MOUSEBUTTONDOWN and not gun_firing_already: # Gets Mouse Clicks
                gun_firing_already = True
                fire.stop()
                fire.play() # Pistol firing Anim
                pistolsound.play()
                pygame.display.update()
                for i in range(len(enemies)):
                    if enemies[i].collider.colliderect(gun_collider):
                        del enemies[i]
                        break
                    
                
            
            #Event Queue Code Ends Here -----------------------------------------------------------------
            
        if scrposx<-400:               #Camera Move Effect Boundaries
            scrposx=-400
        elif scrposx>0:                 # "
            scrposx=0
        if scrposy<-400:                # "
            scrposy=-400
        elif scrposy>0:                 # "
            scrposy=0

        if FireRateTimer.timing_with_precision() >= gun_fire_rate: #setting fire rate for gun
            gun_firing_already = False
            FireRateTimer.reset()

        myTimer.timing() # Timer Ticks
        #WalkTime.timing()  #Timing the Walk
        pos=pygame.mouse.get_pos() #  Finds Cursor Position
        if pos==oldpos and not gun_firing_already:
            if MouseMovementTimer.timing() == 3:
                scrnout = True
        else:
            MouseMovementTimer.reset()
            scrnout = False
        oldpos=pos
        ensurf=pygame.Surface((1000,800),HWSURFACE|SRCALPHA) # Creates Surface To blit Enemy Onto
        window.blit(bitmap,(scrposx,scrposy))
        size = Walking(size,4)
        if size != old_size:
            old_size = [size[0], size[1]]
        
        if len(enemies)>0: #Checks if Enemies need to Be blit
            for i in range(len(enemies)):
                enemies[i].render_sprite(size, [scrposx, scrposy], ensurf) #blits the sprite to screen, and handles scaling for walk anim and collider update
                #enemies[i].anim.smoothscale(size)
                #enemies[i].anim.blit(ensurf,enemies[i].pos)
                #enemies[i].update_collider([scrposx,scrposy])
                pygame.draw.rect(window, (255, 0, 0), enemies[i].collider, 2)
                
        window.blit(ensurf,(scrposx,scrposy))
        window.blit(gun, (248, guny))
        gun_collider.y = guny
        pygame.draw.rect(window, (255, 255, 255), gun_collider, 2)

        fire.blit(window, (248, guny))
        
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

