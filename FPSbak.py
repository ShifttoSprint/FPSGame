import pygame,random
from pygame.locals import *
import pyganim
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
    x=random.randrange(0,1000)
    return (x,265)

class Timer:
    def __init__(self):
        self.start=int(pygame.time.get_ticks())
        self.seconds=0
    def timing(self):
        self.seconds=int((pygame.time.get_ticks()-self.start)/1000)
        return self.seconds
    def reset(self):
        self.start=int(pygame.time.get_ticks())
    
font=pygame.font.SysFont("Verdana.ttf", 20)
pos = []
bitmap=pygame.image.load("forest.png").convert_alpha()
bitmap=pygame.transform.scale(bitmap,(1000,800))
window.blit(bitmap,(-200,-200))
gun=pygame.image.load("pistol.png").convert_alpha()
gun=pygame.transform.scale(gun,(160,160))
guny=300
fire=pyganim.PygAnimation([("pistolfire/frame_1.gif",200),("pistolfire/frame_2.gif",100),("pistolfire/frame_3.gif",100),("pistolfire/frame_4.gif",200),("pistolfire/frame_5.gif",200)])
fire.loop=False
pygame.mouse.set_visible(False)
enemy=pyganim.PygAnimation([("enemy/0.png",150),("enemy/1.png",150),('enemy/2.png',150),('enemy/3.png',150),('enemy/4.png',150),('enemy/5.png',150),('enemy/6.png',150),('enemy/7.png',150),('enemy/8.png',150)])
enmyspawn=False
enplist=[]
enemiesspawned=[]
enpos=0
while isRunning:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            isRunning=False
            break
        elif event.type==pygame.MOUSEMOTION:
            pos=posfinder()
            if pos[0]<300 :
                scrposx = -pos[0]+110
            elif pos[0]==300:
                scrposx = -200
            elif pos[0]>300 :
                scrposx = (-pos[0]+100)-10
            if pos[1]>200 :
                scrposy = -pos[1]-10
            elif pos[1]==200:
                scrposy = -200
            elif pos[1]<200 :
                scrposy = -pos[1] + 10
        if event.type==pygame.MOUSEBUTTONDOWN:
            fire.play()
            pygame.display.update()
        if pygame.mouse.get_focused():
            scrnout=False
        elif not pygame.mouse.get_focused():
            scrnout=True
            fire.stop()
    if pos[0]<10:
        pygame.mouse.set_pos(10,pos[1])
    elif pos[0]>590:
        pygame.mouse.set_pos(590,pos[1])
    if pos[1]<10:
        pygame.mouse.set_pos(pos[0],10)
    elif pos[1]>390:
        pygame.mouse.set_pos(pos[0],390)
    if scrposx<-400:
        scrposx=-400
    elif scrposx>0:
        scrposx=0
    if scrposy<-400:
        scrposy=-400
    elif scrposy>0:
        scrposy=0
    if not enmyspawn:
        enp=EnemyPos()
        enplist.append(enp)
        if len(enplist)==4:
            enmyspawn=True
    if len(enplist)>1:
        Index=random.randrange(0,(len(enplist)-1))
        enpos=enplist[Index]
    ensurf=pygame.Surface((1000,800),HWSURFACE|SRCALPHA)
    window.blit(bitmap,(scrposx,scrposy))
    enemy.blit(ensurf,enpos)
    enemiesspawned.append(enpos)
    del enplist[Index]
    if len(enplist)==0:
        enmyspawn=False
    window.blit(ensurf,(scrposx,scrposy))
    enemy.play()
    window.blit(gun,(230,guny))
    fire.blit(window, (230, 240))
    del ensurf
    if scrnout:
        guny+=1
    elif not scrnout:
        guny-=1
    if guny<240:
        guny=240
    elif guny>400:
        guny=400
    count_fps()
    Fps=font.render(str(FPS),True,(255,255,255))
    window.blit(Fps,(0,0))
    clock.tick(200)
    pygame.display.update()
pygame.quit()

