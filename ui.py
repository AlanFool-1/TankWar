import sys
import pygame,time,random
# 开始界面显示
import scene, tank, food,explode,display,bullet
SCREEN_WIDTH=1200
SCREEN_HIGHT=720
TEXT_COLOR=pygame.Color(255,0,0)
BG_COLOR=pygame.Color(240,255,240)
class Ui(pygame.sprite.Sprite):
    def __init__(self):
        self.reset = pygame.image.load(r"images\ui\reset.png")
        self.reset_2 = pygame.image.load(r"images\ui\reset2.png")
    def display(self,screen):
        screen.blit(self.reset,(360,230))
        
    def display_2(self,screen):
        screen.blit(self.reset_2,(360,230))
    
    def getTextSurface(self,text,fontsize=22,bg=0):
        pygame.font.init()
        font=pygame.font.SysFont("kaiti",fontsize)
        if not bg:
            textSurface=font.render(text,True,TEXT_COLOR)
        else:
             textSurface=font.render(text,True,TEXT_COLOR,BG_COLOR)
        return textSurface