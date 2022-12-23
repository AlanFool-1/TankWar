import pygame
class Explode(pygame.sprite.Sprite):
    def __init__(self,tank):
        self.rect=tank.rect
        self.time=24
        self.kind=0
        self.images=[
            pygame.image.load("./images/explode/explode1.png"),
            pygame.image.load("./images/explode/explode2.png"),
            pygame.image.load("./images/explode/explode3.png"),
            pygame.image.load("./images/explode/explode4.png"),
            pygame.image.load("./images/explode/explode5.png"),
            pygame.image.load("./images/explode/explode6.png"),
            pygame.image.load("./images/explode/explode7.png"),
            pygame.image.load("./images/explode/explode8.png"),
            pygame.image.load("./images/explode/explode9.png"),
        ]
        self.step=0
        self.image=self.images[self.step]
        self.live=True

class big_explode(Explode,pygame.sprite.Sprite):
    def __init__(self,tank):
        super().__init__(tank)
        self.time=30
        self.kind=1
        self.images=[]
        for i in range(1,31):
            st="./images/explode/big"+str(i)+".png"
            self.images.append(pygame.image.load(st))
        