# 子弹类
import pygame
from math import *
SCREEN_HIGHT=720
SCREEN_WIDTH=1200
shoot_delay=2500
last_shoot_time=0
# 子弹类
class Bullet(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		# 子弹四个方向(上下左右)
		self.bullets = ['images/bullet/bullet_up.png', 'images/bullet/bullet_down.png', 'images/bullet/bullet_left.png', 'images/bullet/bullet_right.png']
		# 子弹方向(默认向上)
		self.direction_x, self.direction_y = 0, -1
		self.bullet = pygame.image.load(self.bullets[0])
		self.rect = self.bullet.get_rect()
		# 在坦克类中再赋实际值
		self.rect.left, self.rect.right = 0, 0
		# 速度
		self.speed = 6
		# 是否存活
		self.being = False
		# 是否为加强版子弹(可碎钢板)
		self.stronger = False
	# 改变子弹方向
	def turn(self, direction_x, direction_y):
		self.direction_x, self.direction_y = direction_x, direction_y
		if self.direction_x == 0 and self.direction_y == -1:
			self.bullet = pygame.image.load(self.bullets[0])
		elif self.direction_x == 0 and self.direction_y == 1:
			self.bullet = pygame.image.load(self.bullets[1])
		elif self.direction_x == -1 and self.direction_y == 0:
			self.bullet = pygame.image.load(self.bullets[2])
		elif self.direction_x == 1 and self.direction_y == 0:
			self.bullet = pygame.image.load(self.bullets[3])
		else:
			raise ValueError('Bullet class -> direction value error.')
	# 移动
	def move(self):
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		# 到地图边缘后消失
		if (self.rect.top < 3) or (self.rect.bottom > SCREEN_HIGHT - 3) or (self.rect.left < 3) or (self.rect.right > SCREEN_WIDTH - 3):
			self.being = False
	
class Cannon(Bullet,pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		# 子弹四个方向(上下左右)
		self.num=0
		self.kind=0
		self.being=True
		self.bullets = ['images/bullet/cannon2.png', 'images/bullet/cannon4.png', 'images/bullet//cannon1.png', 'images/bullet/cannon3.png']
		self.x1,self.y1=1000,700
		self.velocity=3000            #导弹速度
		self.time1=1/1000             #每个时间片的长度
		self.A=()
		self.B=()
		self.C=()
		self.missile=pygame.image.load(self.bullets[3])
		self.height=self.missile.get_height()
		self.width=self.missile.get_width()
		self.tank=None
	def bullet_track(self,player):
			x,y=player.rect.left,player.rect.bottom
			# 两点距离公式
			distance=sqrt(pow(self.x1-x,2)+pow(self.y1-y,2))
			# 每个时间片需要移动的距离
			section=self.velocity*self.time1
			sina=(self.y1-y)/distance
			cosa=(x-self.x1)/distance
			# 两点间线段的弧度值
			angle=atan2(y-self.y1,x-self.x1)
			# 弧度转角度
			fangle=degrees(angle)
			self.x1,self.y1=(self.x1+section*cosa,self.y1-section*sina)
			self.missiled=pygame.transform.rotate(self.missile,-(fangle))
			if 0<=-fangle<=90:
				self.A=(self.width*cosa+self.x1-self.width,self.y1-self.height/2)
				self.B=(self.A[0]+self.height*sina,self.A[1]+self.height*cosa)
		
			if 90<-fangle<=180:
				self.A = (self.x1 - self.width, self.y1 - self.height/2+self.height*(-cosa))
				self.B = (self.x1 - self.width+self.height*sina, self.y1 - self.height/2)
		
			if -90<=-fangle<0:
				self.A = (self.x1 - self.width+self.missiled.get_width(), self.y1 - self.height/2+self.missiled.get_height()-self.height*cosa)
				self.B = (self.A[0]+self.height*sina, self.y1 - self.height/2+self.missiled.get_height())
		
			if -180<-fangle<-90:
				self.A = (self.x1-self.width-self.height*sina, self.y1 - self.height/2+self.missiled.get_height())
				self.B = (self.x1 -self. width,self.A[1]+self.height*cosa )
		
			self.C = ((self.A[0] + self.B[0]) / 2, (self.A[1] + self.B[1]) / 2)
			self.rect.left,self.rect.bottom = self.x1-self.width+(self.x1-self.C[0]),self.y1-self.height/2+(self.y1-self.C[1])
			if (self.rect.top < 3) or (self.rect.bottom > SCREEN_HIGHT - 3) or (self.rect.left < 3) or (self.rect.right > SCREEN_WIDTH - 3):
				self.being = False
			
			
			
		
	